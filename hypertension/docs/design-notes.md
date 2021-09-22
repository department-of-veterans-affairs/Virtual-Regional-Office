# Python Environment

> This section was originally written on 6/9/2021 by Aaron Houlihan (aaron@amida.com; Aaron.Houlihan@va.gov)

`py-root/poetry.toml` is set to cause the poetry virtualenv of the project to be located in `py-root/.venv` rather than the default poetry location of `~/Library/Caches/pypoetry/virtualenvs`.

As a result, when you open VS Code to `py-root/` it will automatically see and activate the virtualenv.

This lets you:
- Run tests using vscode test integration
- Run linters and auto-formatters
- Run individual functions right from the editor

(You can do all of this in VS Code by clicking the debug icon - the settings.json and launch.json config files enable this setup.)

If the virtualenv was not located in `py-root/.venv`, then when you open VS Code to `py-root/`, VS Code would pop up an error messge:

> No Python interpreter is selected. You need to select a Python interpreter to enable featuresr such as IntelliSense, linting, and debugging.

# SAM (CloudFormation) Circular Dependencies

> This section was originally written on 6/14/2021 by Aaron Houlihan (aaron@amida.com; Aaron.Houlihan@va.gov)

## Problem

There are several interconnected loops of circular dependencies.

- The Lambda Function is dependent on the SM Secret and the Execution Role
- The Execution Role (has an AssumeRolePolicyDocument that) is dependent on the Lambda (rather, it will be dependent, after the "TODO" to narrow down the AssumeRolePolicy document's Principal (for security reasons) is complete).
- The Policy is dependent on the Execution Role and the SM Secret.
- The KMS Key (really, its policy) is dependent on the Execution Role.
- The SM Secret is dependent on the KMS Key.

## Solution

SAM and CloudFormation offers mechanisms for resolving circlar dependenies. However, they are not the best solution for us.

### Suggestion 1 From AWS Docs

The two solutions offered [here](https://aws.amazon.com/blogs/infrastructure-and-automation/handling-circular-dependency-errors-in-aws-cloudformation/) will not work for us because both of these are dependent on a system where one of the resources in the link _could_ be provisioned first becuase that resources is actually not strictly dependent on others. (In other words, the alleged circular dependencies listed in this article are not real circular dependencies in the resources; they just operate that way at stack creation time because of the way the SAM/CF template is structured.) Unfortunately, we do not have this situation.

### Suggestion 2 From AWS Docs

The one solution [here](https://aws.amazon.com/blogs/mt/resolving-circular-dependency-in-provisioning-of-amazon-s3-buckets-with-aws-lambda-event-notifications/) is (unfortunately) _far_ more complex than we want.

It will be _much_ quicker and easier for
1. A new developer to get up to speed with the repo...
2. Any developer to maintain the repo...
3. A system administrator to deploy the system...

...if we simply use the manual instructions I've included in the [README.md](../README.md).

# Secret Management

Design decision: We are using AWS Secrets Manager to encrypt the various secrets, rather than just using Lambda's built-in encryption of environment variables (both of these, of course, use AWS KMS, by the way), because using Lambda's built-in encrypts _all_ env vars, and thus prevents all values from being read by folks who don't have sufficient permissions on the KMS key used to encrypt them all. This could be cumbersome (e.g. difficult deal with when debugging). We want all the non-secret env vars to be readable by everyone working on the project, and only secrets need to have their visibility limited to the owner of the secret value.

# Environment Variables and Parameter Passing

Some of our environment variables (which are also SAM parameters) have characters that shells and/or the AWS SAM CLI handle specially.

- The Lighthouse OAuth JWT scopes (`LighthouseJwtScope`) has spaces and forward slashes in it.
- The private RSA needed to authenticate to Lighthouse is in PEM format, and it thus contains newline characters.

Also, SAM CLI has quirks and limitations related to how it accepts values for the `--parameter-overrides` CLI option.

Thus, we have the following list of constraints:

1. With SAM CLI, You cannot specify a file URL (i.e. you can't do `--parameter-overrides file://path/to/my-params-file.env.or.json`)
    - See https://github.com/aws/aws-sam-cli/issues/2054
2. This works: SAM CLI `--parameter-overrides "MyLongList=\"Of parameters with special characters\" WorksForThe="\CLI, but this is unwieldly due to the number of parameters"\"`. Also, doing things this way would mean you would have to specify params on the command line for AWS deployment, and simultaneously  maintain a `.env` file for Pytest and individual script purposes.
3. If you use SAM CLI `--parameter-overrides $(cat my-params-file.env)` and any of your variables have spaces or slashes, the `cat` command or `$()` or something about SAM CLI causes SAM CLI to choke.
4. In `samconfig.toml` the `parameter_overrides` list is as unwieldy as item 2 above.
5. We want to specify configuration values in _one_ place
    - And have them work for all of our use cases
      - Running Pytest
      - Running a few of our Python scripts as scripts (such as our Lighthouse authentication script)
      - `sam build` and `sam deploy`
    - `samconfig.toml` can't support this the Pytest and script use cases. Also, an environment variable file is the a very idiomatic way to doing this.
6. The first time you deploy a stack, you must use `sam deploy --guided`, or else use `sam deploy` and specify the S3 bucket. We must use `sam deploy --guided` on the first deploy because we want AWS to auto-generate the S3 bucket.
7. The RSA key, of course, has to be a SAM parameter that has option `NoEcho: true` set for security. Unfortunately, with this set, `sam deploy --guided` has a bug where it will not accept the value you place in `samconfig.toml` and instead will _force_ you to specify the value via its interactive CLI UI. When you try to specify a multi-line value (i.e. the RSA key in PEM format), it breaks.
8. CloudFormation (SAM) only accepts parameters that are less than 4096 bytes. base64 encoding the PEM fixes the multi-line problem, but even this is more than 4096 bytes.

## Our Solution

- We removed the RSA key from the set of environment variables. It must be set into AWS Secrets Manager via the AWS Console. Limitation numbers 7 and 8 above forces this unfortunate conclusion.
- Environment variables are to be specified in one authoritative place: `cf-template-params.env`
  - This makes Pytest and running individual scripts work.
- Python script `set_parameter_overrides.py` copies the values from `cf-template-params.env` into `samconfig.toml` in a format friendly to that file. Run that script before you deploy to AWS.
  - This makes AWS deployment work.
- Set your Lighthouse authentication RSA key in AWS Secrets Manager via the AWS CLI. (See [the README](../README.md#Upload-Your-Lighthouse-Private-RSA-Key-to-Secrets-Manager)) The AWS CLI needs the key in single-line format (PEM is multi-line). base64 encode it to make it single line and upload it. The VRO code will base64 decode it.

## Note

The regex in `set_parameter_overrides.py` only works if your `samconfig.toml` has a line like `parameter_overrides = "SOME_STRING_VALUE___EVEN_A_DUMMY"`

# CI Setup

We use Circle CI.

Circle CI default behavior is to run (i.e. to run your Circle CI workflow(s)) every time a commit is made on any branch.

We don't want every commit on every branch to trigger a Circle CI workflow because doing so is not needed and costs money.

In the Circle CI project for this git repo, we have the Circle CI project setting "Only build pull requests" enabled. This setting also always builds all commits on our default branch (which is `develop`) and all commits that get a git tag created on them.

Limitation: It doesn't build every commit on the `master` branch.

Workaround, part 1: Whenever we want to create a release (i.e. whenever we want to merge `develop` into `master`), we can create a PR to do so. This will of course trigger a Circle CI workflow, which we want.

Workaround, part 2: If we ever have hotfixes, we cannot use standard "gitflow" workflow of making hotfix commits directly to `master`. We must branch off of `master`; commit the hotfix commits to that new branch; and then create a PR to merge the hotfix branch into `master`.

Alternative workaround we can consider later: Some way of using git tags on `master`, perhaps to supplement or replace the above two workarounds.

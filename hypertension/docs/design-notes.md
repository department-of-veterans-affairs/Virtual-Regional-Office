# Python Environment

> This section was originally written on 6/9/2021 by Aaron Houlihan (aaron@amida.com; Aaron.Houlihan@va.gov)

`vro-main/poetry.toml` is set to cause the poetry virtualenv of the project to be located in `vro-main/.venv` rather than the default poetry location of `~/Library/Caches/pypoetry/virtualenvs`.

As a result, when you open VS Code to `vro-main/` it will automatically see and activate the virtualenv.

This lets you:
- Run tests using vscode test integration
- Run linters and auto-formatters
- Run individual functions right from the editor

(You can do all of this in VS Code by clicking the debug icon - the settings.json and launch.json config files enable this setup.)

If the virtualenv was not located in `vro-main/.venv`, then when you open VS Code to `vro-main/`, VS Code would pop up an error messge:

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

# Hypertension Fast-Track System

# Tools

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- Python
- [pyenv](https://github.com/pyenv/pyenv): Manage Python versions, can be used with poetry to create isolated environments
- [Poetry](https://python-poetry.org/): Manage all your Python package dependencies
- [wkhtmltopdf](https://wkhtmltopdf.org/): The PDF generation command line tool and one of our system dependencies

# Technologies

The Hypertension Fast-Track System is built in these technologies:

- [AWS Lambda](https://aws.amazon.com/lambda/) : language-agnostic single-purpose microservices run without a dedicated server

# Development

Create and fill out our cloud formation template variables
```sh
cp cf-template-params-example.env cf-template-params.env
```

Note: For deployment to AWS, you'll need to get the `KmsCmkId` from the [Initial Deployment](#initial-deployment) section below.

## Develop and Test the Python Functions Locally

This workflow is for locally developing the individual Python functions and locally running their automated tests, via Python, pytest, and pytest-watch on your machine.

Install the following [tools](#Tools):
- Python
- pyenv
- Poetry
- wkhtmltopdf

To build Python locally:
```sh
make build.local
```

To build Python locally and run pytest unit tests locally:
```sh
make pytest
```

To build the lambda package locally and run the function in a container:
```sh
make invoke.sam.local
```

:exclamation:***Note*** *You will need to deploy the lambda layers to AWS before you can invoke the stack locally with the above command. AWS SAM lacks support for local invocation of a function that utilizes lambda layers from another stack without being able to reference the layer ARNs, which will only be defined once they're deployed in the relevant AWS environment. If they are already deployed to the environment you're referencing locally, you can update configuration with those layer ARNs by running:*
```sh
make update.function.template.layers
```

## Deploy Everything to AWS

Install the following [tools](#Tools):
- AWS CLI
- AWS SAM CLI
- Python
- pyenv

Recommended: Learn [AWS tutorial number 2](#AWS-Tutorials).

### Initial Deployment

#### Prep `samconfig.toml` to Receive `parameter_overrides` Values

`cp samconfig-default.toml samconfig.toml`

#### Manually Create the AWS KMS Customer Managed Key (CMK).

This is ideal for two reasons:

- Our SAM stack has circular dependencies that cannot be cleanly resolved. See [design-notes.md](docs/design-notes.md).
- We don't want to accidentally create a KMS key having a policy that lacks proper administrators with proper permissions. If a key were to get created without the proper policy, it's possible we would not be able to use or delete the key. We would have to contact AWS to delete it. This manual process is the safest way to create the key policy.

1. Log into the AWS Console for AWS KMS.

2. Create a symmetric CMK with these options:
- Key type >> `Symmetric`
- Advanced options >> Key material origin >> `KMS`
- Alias >> `VroKmsCmk`
- Description >> `VBA Virtual Regional Office. For encrypting secret configuration values.`
- Tags >> `None required by VRO application software. Thus, the only potential tags are those that might be required by system administrators.`
- Key administrators >> `Choose the VRO application developer as well as any other users who need privileges to administer the key.`
- Key users >> `Choose the VRO application developer.`

Note: The key policy will be changed in step 5 below. Therefore, the only strict requirement for the selection of key administrators and key users is that the user who will perform step 5 below must be among the group of key administrators selected above.

3. After the CMK is created, plug the key's ID into your `cf-template-params.env`.

4. Retrieve and export temporary AWS MFA session credentials. See [AWS MFA Authentication](#aws-mfa-authentication) for help with this.

5. Deploy the SAM stack to AWS via `make deploy.stack`.

6. Edit the CMK's policy via the AWS console. Set the key policy to the contents of file `kms-key-policy-statements.json` in this repo, including the ARN of the Lambda execution role created in step 4.

### Subsequent Deployment

You'll always need to retrieve and export AWS MFA session credentials before deployment.
See [AWS MFA Authentication](#aws-mfa-authentication) for more.

If the deployment environment already has instances of the lambda and layers deployed:

- If you make changes to the lambda function but have no additions or updates to dependencies, you can deploy with:

    ```sh
    make deploy.sam
    ```

- If additions or updates are made to the dependencies layer (or, rarely, the wkhtmltopodf layer), you can deploy everything, including the lambda function with the updated layer version arns listed in its configuration, by running:

```sh
make deploy.stack
```

### Upload Your Lighthouse Private RSA Key to Secrets Manager

Base64 encode your PEM.
(_See [design-notes.md](docs/design-notes.md#Our-Solution) for rationale._)
```sh
base64 /PATH/TO/YOUR_RSA_PEM_KEY_FILE
```

Get the ARN of your Secrets Manager secret:
```sh
aws cloudformation describe-stack-resources --stack-name houli-vro
```

Get the name of the secret:
```sh
aws secretsmanager describe-secret --secret-id THE_SECRET_ARN_FROM_THE_LAST_STEP
```

```sh
aws secretsmanager put-secret-value --secret-id THE_SECRET_NAME_FROM_THE_LAST_STEP --secret-string YOUR_BASE_64_ENCODED_SECRET
```

You should also upload the Lighthouse Client ID, because the private key can only be used in conjunction with its matching client ID, and storing the client ID in AWS Secrets Manager is preferable to passing it around via other means.

The name for the client ID in AWS Secrets Manager is expected to be in the parameter `LighthousePrivateClientIdArn`. This is expected to be a string with the value of the client ID.

The Lighthouse Private RSA Key and the Lighthouse Client ID must both be associated with the same key in Key Management Service.

# AWS Tutorials

## 1. Learn Lambda

Learn a little Lambda if you think you need it. Just creating one via the AWS console should be plenty of knowledge for this step
- https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html

## 2. Learn AWS SAM CLI

Learn how to use AWS SAM CLI. (The CloudFormation and Lambda stack parts are applicable; the Step Functions state machine and a DynamoDB table are not.)
- https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-state-machine-using-sam.html

# AWS MFA Authentication
VA AWS environments have multi-factor authentication set up for every IAM user. Therefore, in order to run AWS CLI commands for these environments, we have to retrieve temporary session credentials based on our MFA serial/token codes, and then set those temporary credentials as AWS environment variables.

We have a helper script for exporting session credentials to your shell environment. You can run this script by running:

```bash
cd stack_deployment; poetry install
source export_aws_mfa_credentials.sh
```

# Git Workflow
We use the [Gitflow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow); in summary, this means that we write code primarily in feature branches that are then merged to `develop`, and only push to the primary branch from there.

Pull requests are submitted on Github and require review in order to be merged. Our process is that reviewers approve and the submitter of the PR then merges to `develop`.

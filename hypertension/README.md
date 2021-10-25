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

To view description of Makefile commands:
```sh
make help
```

Create and fill out our cloud formation template variables:
```sh
cp env-example.env .env
```

Note: For deployment to AWS, you'll need to get the `KmsCmkId` from the [Initial Deployment](#initial-deployment) section below.

Set your environment variables per the [Environment Variables](#environment-variables) section.

## Develop and Test Locally

This workflow is for locally developing the individual Python functions 
- Running their automated tests, via Python, pytest, and pytest-watch
- Testing also with `sam local invoke`

Install the following [tools](#Tools):
- pyenv
- Python
- Poetry
- wkhtmltopdf

Poetry install py-root/, lint, and pytest with watch enabled:
```sh
make test
```

To build the lambda package locally and run the function in a container:

:exclamation:***Note*** *You will need to deploy the lambda layers to AWS before you can invoke the stack locally with the below commands. AWS SAM lacks support for local invocation of a function that utilizes lambda layers from another stack without being able to reference the layer ARNs, which will only be defined once they're deployed in the relevant AWS environment.

Add Lambda Layer ARNs to template.yaml of main SAM/CF stack:
```sh
make add-layers-to-main-template
```

```sh
make invoke-sam-local
```

## Deploy

Install the following [tools](#Tools):
- pyenv
- Python
- AWS CLI
- AWS SAM CLI

Recommended: Learn [AWS tutorial number 2](#AWS-Tutorials).

### Initial Deployment

#### 1. Prep `samconfig.toml` to Receive `parameter_overrides` Values

```sh
cp samconfig-default.toml samconfig.toml
```

#### 2. Manually Create the AWS KMS Customer Managed Key (CMK)

This is ideal for two reasons:

- The main SAM stack has circular dependencies that cannot be cleanly resolved. See [design-notes.md](docs/design-notes.md).
- We don't want to accidentally create a KMS key having a policy that lacks proper administrators with proper permissions. If a key were to get created without the proper policy, it's possible we would not be able to use or delete the key. We would have to contact AWS to delete it. This manual process is the safest way to create the key policy.

2.1. Log into the AWS Console for AWS KMS.

2.2. Create a symmetric CMK with these options:
- Key type >> `Symmetric`
- Advanced options >> Key material origin >> `KMS`
- Alias >> `VroKmsCmk`
- Description >> `VBA Virtual Regional Office. For encrypting secret configuration values.`
- Tags >> `None required by VRO application software. Thus, the only potential tags are those that might be required by system administrators.`
- Key administrators >> `Choose the VRO application developer as well as any other users who need privileges to administer the key.`
- Key users >> `Choose the VRO application developer.`

Note: The key policy will be changed in step 6 below. Therefore, the only strict requirement for the selection of key administrators and key users is that the user who will perform step 6 below must be among the group of key administrators selected above.

#### 3. Use the CMK

After the CMK is created, plug the key's ID into your `.env`.

#### 4. Authenticate to AWS

See [AWS MFA Authentication](#aws-mfa-authentication).

#### 5. Deploy Both the Main SAM/CF Stack and the Layers SAM/CF Stack to AWS

Note: You must run this command for your first deployment!

```sh
make deploy-all-guided
```

#### 6. Set Your CMK's Policy

Edit the CMK's policy via the AWS console. Set the key policy to the contents of file `kms-key-policy-statements.json` in this repo, including the ARN of the Lambda execution role created in step 5.

#### 7. Set Your Secret Values in AWS SecretsManager

Base64 encode your Lightouse private RSA key PEM. This will be your secret value.
(_See [design-notes.md](docs/design-notes.md#Our-Solution) for rationale._)
```sh
base64 /PATH/TO/YOUR_RSA_PEM_KEY_FILE
```

Via either the AWS console or CLI (see commands below), upload
- The Base64 encoded Lighthouse private RSA key PEM to the `VroLhPrivateRsaKey` secret
- The Lighthouse OAuth client ID to the `VroLhAssertionClientId` secret

##### Generic Secret Upload Commands

Get the ARNs of your Secrets Manager secrets
```sh
aws cloudformation describe-stack-resources --stack-name STACK_NAME
```

Get the name of each secret
```sh
aws secretsmanager describe-secret --secret-id EACH_SECRET_ARN_FROM_THE_LAST_STEP
```

Upload the secret values
```sh
aws secretsmanager put-secret-value --secret-id THE_SECRET_NAME_FROM_THE_LAST_STEP --secret-string SECRET_VALUE
```

### Subsequent Deployment

You'll always need to retrieve and export AWS MFA session credentials before deployment.
See [AWS MFA Authentication](#aws-mfa-authentication) for more.

If the deployment environment already has instances of the lambda and layers deployed:

- If you make changes to the lambda function but have no additions or updates to dependencies, you can deploy with:

    ```sh
    make deploy-main
    ```

- If additions or updates are made to the dependencies layer (or, rarely, the `wkhtmltopodf` layer), you can deploy everything, including the lambda function with the updated layer version arns listed in its configuration, by running:

    ```sh
    make deploy-all-guided
    ```

# Environment Variables

Variables are listed below in this format:

VARIABLE_NAME (Required (if it actually is)) [the default value]
A description of what the variable is or does.

A description of what to set the variable to, whether that be an example, or what to set it to in development or production, or how to figure out how to set it, etc.
Perhaps another example value, etc.

### `LighthouseTokenUrl`

URL to fetch a JWT to authenticate to [Lighthouse](https://developer.va.gov).

### `LighthouseJwtAudUrl`

URL to set as the AUD value of Lighthouse JWTs.

### `LighthouseJwtScope`

Lighthouse authentication scope, which is a part of your JWT assertions, which you use to request a lighthouse JWT.

The [Lighthouse scopes documentation](https://developer.va.gov/explore/authorization?api=fhir#scopes) can point you in the right direction.

- For Lighthouse Veterans Health API queries for blood pressure and medication data, you can use `"launch/patient patient/Patient.read patient/Observation.read patient/Medication.read"`.

### `LighthouseOAuthClientId`

The client ID issued to you. It's based on the public RSA key you provided to the lighthouse auth team. This must match the RSA key specified by `LighthousePrivateRsaKeyFilePath` and `LighthousePublicRsaKeyFilePath`.

### `LighthouseOAuthGrantType`

- We always use Lighthouse's system-to-system implementation of OAuth. Thus, always set this to `client_credentials`.

### `LighthouseOAuthAssertionType`

- `"urn:ietf:params:oauth:client-assertion-type:jwt-bearer"`. This value is specified by the OAuth spec, and it was provided by the Lighthouse auth team.

### `LighthousePrivateRsaKeyFilePath`

Path on your local machine to the private half of your RSA key pair that was used to generated your lighthouse OAuth "Client Credentials" grant type credentials. Goes with your corresponding `LighthousePublicRsaKeyFilePath` (of course) and your corresponding `LighthouseOAuthClientId`.

### `LighthousePublicRsaKeyFilePath`

Path on your local machine to the public half of your RSA key pair that was used to generated your lighthouse OAuth "Client Credentials" grant type credentials. Goes with your corresponding `LighthousePrivateRsaKeyFilePath` (of course) and your corresponding `LighthouseOAuthClientId`.

### `KmsCmkId`

Key ID of your AWS Key Management Service symmetric key, which you setup to be used to encrypt the SAM/CF stack's AWS Secrets Manager secrets.

### `LighthouseObservationUrl`

URL of the Lighthouse Veterans Health API (which is a FHIR API) Observation resource.

- For development and testing: `https://sandbox-api.va.gov/services/fhir/v0/r4/Observation`

### `LighthouseObservationCategory`

- `"vital-signs"`. This is the category of FHIR observations that blood pressure readings fall under.

### `LighthouseObservationLoincCode`

- `"85354-9"`. This is the LOINC code under which the Lighthouse Veterans Health API (which is a FHIR API) lists all blood pressure data.

### `TestVeteranIcn`

When deployed in AWS, the ICN is provided an HTTP body param to the Lambda function.

This is the ICN of a Veteran to use in automated unit tests.

We choose to use an ICN of a fake Veteran in the Lighthouse sandbox--though the unit tests mock calls to the Lighthouse sandbox and thus don't actually connect to it.

- Set to `"32000225"`

### `PdfGeneratorLayerArn` This Is Populated Automatically During Stack Deployment.

ARN of the AWS Lambda Layer that contains the PDF generation tools.

This is auto-set during initial deployment.

### `PythonDependenciesLayerArn` Same As Above. See README Local Invoke Section For More Info

ARN of the AWS Lambda Layer that contains the Python dependencies.

This is auto-set during initial deployment.

# AWS Tutorials

## 1. Learn Lambda

Learn a little Lambda if you think you need it. Just creating one via the AWS console should be plenty of knowledge for this step
- https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html

## 2. Learn AWS SAM CLI

Learn how to use AWS SAM CLI. (The CloudFormation and Lambda stack parts are applicable; the Step Functions state machine and a DynamoDB table are not.)
- https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-state-machine-using-sam.html

# AWS MFA Authentication

VA AWS environments have multi-factor authentication setup for every IAM user. Therefore, in order to run AWS CLI commands for these environments, we have to retrieve session credentials based on our MFA serial/token codes, and then set those credentials as AWS environment variables.

We have a helper script for exporting session credentials to your shell environment. You can run this script by running:

```bash
cd stack_deployment; poetry install; source export_aws_mfa_credentials.sh; cd ..
```

# Git Workflow

We use the [Gitflow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow); in summary, this means that we write code primarily in feature branches that are then merged to `develop`, and only push to the primary branch from there.

Pull requests are submitted on GitHub and require review in order to be merged. Our process is that reviewers approve and the submitter of the PR then merges to `develop`.

# CI Setup

See [docs/design-notes.md](docs/design-notes.md#CI-Setup)

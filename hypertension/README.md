# Hypertension Fast-Track System

# Tools

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- Python
- [pyenv](https://github.com/pyenv/pyenv): Manage Python versions, can be used with poetry to create isolated environments
- [Poetry](https://python-poetry.org/): Manage all your Python package dependencies

# Technologies

The Hypertension Fast-Track System is built in these technologies:

- [AWS Lambda](https://aws.amazon.com/lambda/) : language-agnostic single-purpose microservices run without a dedicated server

# Development

**WARNING!! Dont use your (or any) real private RSA key here until we fix the code to make it stop returning the RSA key in the lambda response body!!**

Create and fill out our cloud formation template variables
```sh
cp cf-template-params-example.env cf-template-params.env
```

Note: For deployment to AWS, you'll to get the `KmsCmkId` from the [Initial Deployment](#initial-deployment) section below.

**WARNING!! Dont use your (or any) real private RSA key here until we fix the code to make it stop returning the RSA key in the lambda response body!!**

## Develop and Test the Python Functions Locally

This workflow is for locally developing the individual Python functions and locally running the their automated tests, via Python, pytest, and pytest-watch on your machine.

Install the following [tools](#Tools):
- Python
- pyenv
- Poetry

To build Python locally:
```sh
make build.python
```

To build Python locally and run pytest unit tests locally:
```sh
make pytest
```

## Deploy Everything to AWS

Install the following [tools](#Tools):
- AWS CLI
- AWS SAM CLI
- Python
- pyenv

Recommended: Learn [AWS tutorial number 2](#AWS-Tutorials).

### Initial Deployment

Manually Create the AWS KMS Customer Managed Key (CMK). This is ideal for two reasons:

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

4. Deploy the SAM stack to AWS via `make deploy.sam.guided`.

5. Edit the CMK's policy via the AWS console. Set the key policy to the contents of file `kms-key-policy-statements.json` in this repo, including the ARN of the Lambda execution role created in step 4.

### Deployment

```sh
make deploy.sam
```

# AWS Tutorials

## 1. Learn Lambda

Learn a little Lambda if you think you need it. Just creating one via the AWS console should be plenty of knowledge for this step
- https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html

## 2. Learn AWS SAM CLI

Learn how to use AWS SAM CLI. (The CloudFormation and Lambda stack parts are applicable; the Step Functions state machine and a DynamoDB table are not.)
- https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-state-machine-using-sam.html

# Git Workflow
We use the [Gitflow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow); in summary, this means that we write code primarily in feature branches that are then merged to `develop`, and only push to the primary branch from there.

Pull requests are submitted on Github and require review in order to be merged. Our process is that reviewers approve and the submitter of the PR then merges to `develop`.

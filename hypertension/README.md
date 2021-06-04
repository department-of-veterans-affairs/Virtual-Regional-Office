# Hypertension Fast-Track System


## Tools

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- Python
- [pyenv](https://github.com/pyenv/pyenv): Manage Python versions, can be used with poetry to create isolated environments
- [Poetry](https://python-poetry.org/): Manage all your Python package dependencies

## Technologies

The Hypertension Fast-Track System is built in these technologies:

- [AWS Lambda](https://aws.amazon.com/lambda/) : language-agnostic single-purpose microservices run without a dedicated server

## Development

### Python Environment Background Info

`vro-main/poetry.toml` is set to cause the poetry virtualenv of the project to be located in `vro-main/.venv` rather than the default poetry location of `~/Library/Caches/pypoetry/virtualenvs`.

As a result, when you open VS Code to `vro-main/` it will automatically see and activate the virtualenv.

This lets you:
- Run tests using vscode test integration
- Run linters and auto-formatters
- Run individual functions right from the editor

(You can do all of this in VS Code by clicking the debug icon - the settings.json and launch.json config files enable this setup.)

If the virtualenv was not located in `vro-main/.venv`, then when you open VS Code to `vro-main/`, VS Code would pop up an error messge:

> No Python interpreter is selected. You need to select a Python interpreter to enable featuresr such as IntelliSense, linting, and debugging.

### Develop and Test the Python Functions Locally

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

### Deploy Everything to AWS

Install the following [tools](#Tools):
- AWS CLI
- AWS SAM CLI
- Python
- pyenv

Recommended: Learn [AWS tutorial number 2](#AWS-Tutorials)

Deploy to AWS:
```sh
# First time
make deploy.sam.guided

# Subsequent times
make deploy.sam
```

Note: These commands do a `sam build` as a part of their process.

## AWS Tutorials

### 1. Learn Lambda

Learn a little Lambda if you think you need it. Just creating one via the AWS console should be plenty of knowledge for this step
- https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html

### 2. Learn AWS SAM CLI

Learn how to use AWS SAM CLI. (The CloudFormation and Lambda stack parts are applicable; the Step Functions state machine and a DynamoDB table are not.)
- https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-state-machine-using-sam.html

## Git Workflow
We use the [Gitflow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow); in summary, this means that we write code primarily in feature branches that are then merged to `develop`, and only push to the primary branch from there.

Pull requests are submitted on Github and require review in order to be merged. Our process is that reviewers approve and the submitter of the PR then merges to `develop`.

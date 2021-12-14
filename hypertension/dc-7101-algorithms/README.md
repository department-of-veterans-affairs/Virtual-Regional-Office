# Mini VRO

# Tools

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- Python
- [pyenv](https://github.com/pyenv/pyenv): Manage Python versions, can be used with poetry to create isolated environments
- [Poetry](https://python-poetry.org/): We use this rather than rather than traditional Python tools such as `pip` and `venv` to manage dependencies and virtual environments. `poetry` commands download your dependencies and automatically create and activate your virtual env for you. This repo's Makefile commands contain the `poetry` commands that do everything you need to install, activate your virtual environment, and run your Python code.

# Technologies

The Hypertension Fast-Track System is built in these technologies:

- [AWS Lambda](https://aws.amazon.com/lambda/) : language-agnostic single-purpose microservices run without a dedicated server

# Development and Deployment

The Makefile commands have everything you need.

To view description of Makefile commands:
```sh
make help
```

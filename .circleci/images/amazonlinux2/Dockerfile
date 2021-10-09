# syntax=docker/dockerfile:1
FROM amazonlinux:latest

ENV STAGE=dev \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.11

RUN yum update -y
# CIRCLECI Needs the following
RUN yum install git-all -y
RUN yum install openssh-server -y
RUN yum install openssh-clients -y
RUN yum install tar -y

RUN amazon-linux-extras install python3.8
RUN curl https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox-0.12.6-1.amazonlinux2.x86_64.rpm -O -J -L
RUN yum localinstall wkhtmltox-0.12.6-1.amazonlinux2.x86_64.rpm -y
RUN yum install which -y

# System deps:
RUN yum install pip -y
RUN pip install "poetry==$POETRY_VERSION"

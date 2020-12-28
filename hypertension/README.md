# Hypertension Identification

## Background

This project uses [AWS step functions](https://aws.amazon.com/step-functions/) to manage the flow of information through a hypertension identification system.

It is currently a proof of concept, and uses a set of predefined data to mimic calls and responses from various external systems. It should not be too much extra work to make this real.

## System setup

Below is a diagram of the setup of the services:
![AWS Diagram](docs/AWS_Step_Function_Diagram.png)

Note that this setup has so far only been deployed locally, it is necessary to deploy to Lighthouse AWS to see this live. Please work with Andy Parcel and Bryan Schofield to do this.

## Running Locally

You can set it up yourself via the downloadable version of AWS step functions. To do so, see instructions [here](https://docs.aws.amazon.com/step-functions/latest/dg/sfn-local-docker.html):

1. Follow [this](https://docs.aws.amazon.com/step-functions/latest/dg/sfn-local-lambda.html) guide to setup local SAM lambdas, and deploy. take note of ARN files.

2. Pull the AWS Step functions docker image:

   ```sh
   docker pull amazon/aws-stepfunctions-local
   ```

3. Create config file by copying `aws-stepfunctions-local-credentials-sample.txt` and setup according to [this](https://docs.aws.amazon.com/step-functions/latest/dg/sfn-local-config-options.html#docker-credentials) link

4. Run the image:

   ```sh
   docker run -p 8083:8083 --env-file aws-stepfunctions-local-credentials.txt amazon/aws-stepfunctions-local
   ```

5. Create the local state machine according to the `ASL_Definition.json` file:

   ```sh
       aws stepfunctions --endpoint-url http://localhost:8083 create-state-machine --definition "$(cat ASL_Definition.json)" --name "Hypertension" --role-arn "arn:aws:iam::012345678901:role/DummyRole"
   ```

   Note the ARN of the returned response, for example:

   ```json
   {
     "stateMachineArn": "arn:aws:states:us-east-1:123456789012:stateMachine:Hypertension",
     "creationDate": "2020-12-28T11:13:46.746000-05:00"
   }
   ```

6. In a new Terminal window, start local execution using the returned ARN value:

   ```sh
   aws stepfunctions --endpoint-url http://localhost:8083 start-execution --state-machine-arn arn:aws:states:us-east-1:123456789012:stateMachine:Hypertension --input "$(cat sample_input.json)"
   ```

7. Review logs in the original terminal tab to see results

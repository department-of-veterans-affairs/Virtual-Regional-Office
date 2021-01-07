# Hypertension Identification

## Background

This project uses [AWS step functions](https://aws.amazon.com/step-functions/) to manage the flow of information through a hypertension identification system.

It is currently a proof of concept, and uses a set of predefined data to mimic calls and responses from various external systems. It should not be too much extra work to make this real.

## System setup

Below is a diagram of the setup of the services:
![AWS Diagram](docs/AWS_Step_Function_Diagram.png)

Note that this setup has so far only been deployed locally, it is necessary to deploy to Lighthouse AWS to see this live. Please work with Andy Parcel and Bryan Schofield to do this.

## Helpful Tutorials

This system was setup by referencing the below tutorials:

- [AWS: Create a Serverless Workflow with Step Functions](https://aws.amazon.com/getting-started/hands-on/create-a-serverless-workflow-step-functions-lambda/) - how to orchestrate lambda functions using AWS StepFunctions
- [Create a Step Functions State Machine Using AWS SAM](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-state-machine-using-sam.html) - The above has you manually copying ARN numbers. This tutorial uses the terraform-like SAM to make this easier. The "Stock Functions" demo referenced here was the basis for this project
- [Setting Up Step Functions Local (Downloadable Version)](https://docs.aws.amazon.com/step-functions/latest/dg/sfn-local.html) - setting up lambdas and step functions to be run locally

## Building

This app uses the following tech:

- [Poetry](https://python-poetry.org/) : manage local test dependencies, run tests
- [pyenv](https://github.com/pyenv/pyenv) : manage python versions, can be used with poetry to create isolated environments
- AWS:
  - [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) : CLI that allows you to create and manage serverless applications
  - [AWS Lambda functions](https://aws.amazon.com/lambda/) : language-agnostic single-purpose microservices run without a dedicated server
  - [AWS Step Functions](https://aws.amazon.com/step-functions/) : Serverless orchestrator for creating state machines comprised of lambdas

## Deploying to AWS

Simply setup your local AWS environment as described [here](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html), then run `make deploy.guided` the first time, or `make deploy` subsequent times, to deploy to AWS.

## Running Locally

(This section is under construction - building and deploying to a personal AWS should work for now, but I have not yet gotten a full local SAM CLI-accessed Step Functions instance to work just yet, though the below has some pieces of this)

You can set it up yourself via the downloadable version of AWS step functions. To do so, see instructions [here](https://docs.aws.amazon.com/step-functions/latest/dg/sfn-local-docker.html):

1. Follow [this](https://docs.aws.amazon.com/step-functions/latest/dg/sfn-local-lambda.html) guide to setup local SAM lambdas. For each, do `sam local start-lambda` to start it running on localhost.

2. Pull the AWS Step functions docker image:

   ```sh
   docker pull amazon/aws-stepfunctions-local
   ```

3. Create config file by copying `aws-stepfunctions-local-credentials-sample.txt` and setup according to [this](https://docs.aws.amazon.com/step-functions/latest/dg/sfn-local-config-options.html#docker-credentials) link. NOTE: leave the `LAMBDA_ENDPOINT` variable as-is in order to use locally-running lambda functions

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

## Open questions

This section covers the various open questions about this API:

- Hosting - Where and how will this be hosted within the VA infrastructure? As this stands, I (Nat) have been running it on my personal AWS instance. Options we have discussed:
  - Lighthouse : They host other existing APIs at developer.va.gov
  - VSP : Host infrastructure for va.gov
  - New hosting platform: A hosting platform is in the works, could this project be a pilot project?
- Inputs - what will the inputs to this system look like, and where and how will they be passed into it?
  - Currently the `Applicability Determiner` function assumes that we will have access to `claim type` and `claim subtype`, but we have not fleshed out how to get this information. We have discussed getting it directly from va.gov in some way, and/or getting the disability rating history for a given user by means of some API
- Identity association: currently the `Medical Record Locator` function hardcodes fake values for `PVID` and `icn`. We need some means of determining the `icn` number associated with the current claim ID. There is a service called the `Master Patient Index` that can be used to correlate these IDs, but we need to know:
  - What IDs are available at the time of claim submission? I've used `pvid` as a placeholder, but it is likely this is actually some other ID
  - How can we call into the MPI? Would it be possible for [`vets-api`](https://github.com/department-of-veterans-affairs/vets-api/blob/master/app/models/mpi_data.rb) to provide access somehow?
- Outputs - what will the output of this system be? The current `Record Updater` function does nothing, but would ideally do something with the data that is passed in. Some options we've discussed:
  - A PDF in the veteran's eFolder on VBMS?
  - Flipping the "Ready for review" switch on the veteran's file in CorpDB? We'll need to talk to NWQ about the best way to do this

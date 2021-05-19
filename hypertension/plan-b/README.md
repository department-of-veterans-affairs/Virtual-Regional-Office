## WARNING

DO NOT ENTER YOUR REAL LIGHTHOUSE RSA PRIVATE KEY INTO THE ENVIRONMENT VARIABLE! The Pthon code currently prints it to the logs and also returns it in the body of the Lambda response.

## Develop

### Step 1
Create and fill out our cloud formation template variables
```sh
cp cf-template-params-example.env cf-template-params.env
```

## Run in the Cloud

Do Develop >>> Step 1

```sh
make build.sam.cloud
sam deploy --guided --capabilities CAPABILITY_NAMED_IAM --parameter-overrides $(cat cf-template-params.env)
```

## Run Locally

Build:
```sh
make build.sam.local
```

Invocation Options:
```sh
sam local invoke --event lambda-invoke-test.json
# OR
sam local start-api --template template-local.yaml
```

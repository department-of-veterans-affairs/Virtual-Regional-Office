## Run in the Cloud

```sh
make build.sam.cloud
sam deploy --guided
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

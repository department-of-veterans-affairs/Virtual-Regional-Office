## Run Lambda locally

### Build
```sh
make build.requirements.txt

make build.plan.b
```

### Invocation Options

```sh
sam local invoke --event lambda-invoke-test.json
```

```sh
sam local start-api --template template-local.yaml
```

## Develop

Create and fill out our cloud formation template variables
```sh
cp cf-template-params-example.env cf-template-params.env
```

Build and deploy
```sh
sam build; sam deploy --parameter-overrides $(cat cf-template-params.env)
```

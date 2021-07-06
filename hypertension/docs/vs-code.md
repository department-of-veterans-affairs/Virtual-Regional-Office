# VS Code Helpers

Add the following custom tags to `settings.json`:

```json
"yaml.customTags": [
        "!Ref",
        "!GetAtt"
    ]
```

Add the following launch configurations to `launch.json` to help with debugging within VS Code:

```json
"configurations": [
        {
            "type": "aws-sam",
            "request": "direct-invoke",
            "name": "hypertension:VroMainFunction",
            "invokeTarget": {
                "target": "template",
                "templatePath": "${workspaceFolder}/template.yaml",
                "logicalId": "VroMainFunction"
            },
            "lambda": {
                "payload": {
                    "path": "hypertension/vro-main/pdf-event.json"
                },
                "environmentVariables": {
                    "WKHTMLTOPDF_PATH": "/opt/bin/wkhtmltopdf",
                    "FONTCONFIG_PATH": "/opt/fonts",
                    "STAGE": "dev",
                    "LighthouseTokenUrl": "!Ref LighthouseTokenUrl",
                    "LighthouseClientId": "!Ref LighthouseClientId",
                    "LighthouseJwtAud": "!Ref LighthouseJwtAud",
                    "LighthousePrivateRsaKeySecretArn": "!Ref VroLhPrivateRsaKey"
                }
            }
        }
]
```

from flasgger import Swagger
from flask import Flask, request
from lib.main import main  # pragma: no cover (main is tested elsewhere)

app = Flask(__name__)

swagger_config = Swagger.DEFAULT_CONFIG
swagger_config["swagger"] = "2.0"
swagger_config["title"] = "Rapid Ready for Decision API"
swagger_config["uiversion"] = 3

Swagger(
    app,
    template={
        "info": {
            "title": "",
            "description": "",
            "version": "1.0.2",
        },
        "host": "localhost:5000",
        "schemes": ["http"],
    },
    config=swagger_config,
)


@app.route("/calculate", methods=['POST'])
def handler():
    """
    file: dc7343-1.0.2-resolved.yaml

    """
    return main(request.json)  # pragma: no cover



from flask import Flask, request

from lib.main import main  # pragma: no cover (main is tested elsewhere)

app = Flask(__name__)


@app.route("/calculate", methods=['POST'])
def handler():
    return main(request.json)  # pragma: no cover

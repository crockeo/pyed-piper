from flask import Flask

flask_app = Flask(__name__)


@flask_app.route("/")
def hello_world():
    return "hello world"


# TODO: Configure Flask

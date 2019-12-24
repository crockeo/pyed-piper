from flask import Flask
from flask import Response
from flask import request
from flask_api import status
from flask_cors import CORS

from lib.db import Database
from lib.db.models.synth_button_setting import SynthButtonSetting
from lib.db.models.wav_file import WavFile
from lib.http.controllers import synth_button_setting_controller


def generate_flask_app() -> Flask:
    """
    Generates a Flask application on demand. In a function, rather than a
    global objcet, to avoid the use of global variables.
    """
    db = Database.get()
    db.create_tables([SynthButtonSetting, WavFile])

    app = Flask(__name__)
    CORS(app)

    @app.route("/button/count", methods=["GET"])
    def get_button_count():
        return synth_button_setting_controller.get_synth_button_count()

    @app.route("/button/<int:index>", methods=["GET"])
    def get_synth_button_setting_controller(index: int):
        setting = synth_button_setting_controller.get_synth_button_setting(index)
        if setting is None:
            return "", status.HTTP_404_NOT_FOUND

        response = Response(setting.to_json(), content_type="application/json")
        return response

    @app.route("/button/<int:index>", methods=["PUT"])
    def put_synth_button_setting(index: int):
        json = request.get_json()
        if json is None:
            return "", status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        setting = synth_button_setting_controller.put_synth_button_setting(index, json)

        response = Response(setting.to_json(), content_type="application/json")
        return response

    @app.route("/sample/<uuid:id>", methods=["GET"])
    def get_sample(id):
        query = WavFile.select().where(WavFile.id == id)
        if len(query) == 0:
            return "", status.HTTP_404_NOT_FOUND

        # TODO: Send .wav file with correct mimetype
        pass

    @app.route("/sample", methods=["POST"])
    def add_sample():
        # TODO
        pass

    return app

from flask import Flask
from flask import Response
from flask import request
from flask_api import status
from flask_cors import CORS
import json

from lib.db import Database
from lib.db.models.synth_button_setting import SynthButtonSetting
from lib.db.models.wav_file import WavFile
from lib.http.controllers import synth_button_setting_controller
from lib.http.controllers import wav_file_controller
from lib.synth import AudioManager


def generate_flask_app(audio_manager: AudioManager) -> Flask:
    """
    Generates a Flask application on demand. In a function, rather than a
    global objcet, to avoid the use of global variables.
    """
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

        return Response(setting.to_json(), content_type="application/json")

    @app.route("/button/<int:index>", methods=["PUT"])
    def put_synth_button_setting(index: int):
        json = request.get_json()
        if json is None:
            return "", status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

        setting = synth_button_setting_controller.put_synth_button_setting(
            index, json, audio_manager
        )
        if setting is None:
            return "", status.HTTP_400_BAD_REQUEST

        return Response(setting.to_json(), content_type="application/json")

    @app.route("/samples", methods=["GET"])
    def get_samples():
        wav_files = wav_file_controller.get_samples()
        return Response(
            json.dumps([wav_file.to_json() for wav_file in wav_files]),
            content_type="application/json",
        )

    @app.route("/sample/<id>", methods=["GET"])
    def get_sample(id: str):
        wav_file = wav_file_controller.get_sample(id)
        if wav_file is None:
            return "", status.HTTP_404_NOT_FOUND
        _, data = wav_file

        return Response(data, content_type="audio/wav")

    @app.route("/sample", methods=["POST"])
    def post_sample():
        file_name = "sampleFile"
        if file_name not in request.files or request.files[file_name].filename == "":
            return "", status.HTTP_400_BAD_REQUEST
        file = request.files[file_name]

        wav_file = wav_file_controller.post_sample(file.filename, file.read())

        return Response(
            json.dumps({"id": wav_file.id}), content_type="application/json"
        )

    return app

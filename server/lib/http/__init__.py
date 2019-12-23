from flask import Flask

from lib.db import Database
from lib.db.models.synth_button_setting import SynthButtonSetting
from lib.db.models.wav_file import WavFile


def generate_flask_app() -> Flask:
    db = Database.get()
    db.create_tables([SynthButtonSetting, WavFile])

    app = Flask(__name__)

    @app.route("/button/<int:index>", methods=["GET"])
    def get_synth_button_setting(index):
        query = SynthButtonSetting.select().where(SynthButtonSetting.index == index)

        print(len(query))
        for setting in query:
            print(setting)

        return "asdf"

    @app.route("/button/<int:index>", methods=["PUT"])
    def set_synth_button_setting(index):
        pass

    @app.route("/sample/<uuid:id>", methods=["GET"])
    def get_sample(id):
        pass

    @app.route("/sample", methods=["POST"])
    def add_sample():
        pass

    return app

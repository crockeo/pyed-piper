from flask import Flask

from lib.db import Database
from lib.db.models.synth_button_setting import SynthButtonSetting
from lib.db.models.wav_file import WavFile


def generate_flask_app() -> Flask:
    """
    Generates a Flask application on demand. In a function, rather than a
    global objcet, to avoid the use of global variables.
    """
    db = Database.get()
    db.create_tables([SynthButtonSetting, WavFile])

    app = Flask(__name__)

    @app.route("/button/count", methods=["GET"])
    def get_button_count():
        return 15

    @app.route("/button/<int:index>", methods=["GET"])
    def get_synth_button_setting(index):
        """
        Retrieves the settings for a synth button at a given index. Although it
        goes against GET's supposed idempotence, this method creates a setting
        object when one does not already exist. This allows the web UI to
        be dumb, and always assume there are buttons 0-15, inclusive.
        """
        if index < 0 or index > get_button_count():
            # TODO: Respond with 404, since we only support 15 buttons
            pass
        query = SynthButtonSetting.select().where(SynthButtonSetting.index == index)

        if len(query) > 0:
            for entry in query:
                setting = entry
                break
        else:
            setting = SynthButtonSetting.from_index(index)
            setting.save()

        return setting.to_json()

    @app.route("/button/<int:index>", methods=["PUT"])
    def set_synth_button_setting(index):
        # TODO
        pass

    @app.route("/sample/<uuid:id>", methods=["GET"])
    def get_sample(id):
        query = WavFile.select().where(WavFile.id == id)
        if len(query) == 0:
            # TODO: Return 404?
            pass

        # TODO: Send .wav file with correct mimetype
        pass

    @app.route("/sample", methods=["POST"])
    def add_sample():
        # TODO
        pass

    return app

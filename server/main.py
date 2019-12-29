from gevent.pywsgi import WSGIServer
import keyboard
import signal

from lib.common import config
from lib.common.initialization import load_drivers
from lib.db.models.synth_button_setting import SynthButtonSetting
from lib.db.models.wav_file import WavFile
from lib.db import Database
from lib.http import generate_flask_app
from lib.synth import AudioManager


def main():
    db = Database.get()
    db.create_tables([SynthButtonSetting, WavFile])

    drivers = load_drivers(config.SAMPLE_RATE)
    with AudioManager(drivers) as audio_manager:
        app = generate_flask_app(audio_manager)
        http_server = WSGIServer(("", 3001), app)
        signal.signal(signal.SIGINT, lambda *args, **kwargs: http_server.stop())
        http_server.serve_forever()


if __name__ == "__main__":
    main()

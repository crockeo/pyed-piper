from gevent.pywsgi import WSGIServer
import keyboard
import signal

from lib.http import flask_app
from lib.synth import AudioManager


def main():
    with AudioManager():
        http_server = WSGIServer(("", 3001), flask_app)
        signal.signal(signal.SIGINT, lambda *args, **kwargs: http_server.stop())
        http_server.serve_forever()


if __name__ == "__main__":
    main()

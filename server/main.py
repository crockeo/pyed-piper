import keyboard
import pyaudio
import numpy as np
import time
from typing import List

from lib.synth.driver import LingeringDriver
from lib.synth.driver import OverToneDriver
from lib.synth.driver import WaveDriver
from lib.synth.input import InputAction
from lib.synth.input import KeyboardInput
from lib.synth.notes import notes

VOLUME = 0.5
SAMPLE_RATE = 44100
DURATION = 1
LINGER_TIME = 1.0


class AudioManager:
    def __init__(self):
        self.volume = 0.05
        self.sample_rate = 44100
        self.linger_time = 1.0

        self.frame_start = 0
        self.keyboard_input = KeyboardInput()

        self.drivers = {
            "1": LingeringDriver(
                SAMPLE_RATE,
                LINGER_TIME,
                WaveDriver(SAMPLE_RATE, "server/res/sample.wav"),
            ),
            "2": LingeringDriver(
                SAMPLE_RATE,
                LINGER_TIME,
                WaveDriver(SAMPLE_RATE, "server/res/guitar.wav"),
            ),
            "3": LingeringDriver(
                SAMPLE_RATE,
                LINGER_TIME,
                OverToneDriver(SAMPLE_RATE, notes["C4"], 1, 8),
            ),
            "4": LingeringDriver(
                SAMPLE_RATE,
                LINGER_TIME,
                OverToneDriver(SAMPLE_RATE, notes["D4"], 1, 8),
            ),
            "5": LingeringDriver(
                SAMPLE_RATE,
                LINGER_TIME,
                OverToneDriver(SAMPLE_RATE, notes["E4"], 1, 8),
            ),
            "6": LingeringDriver(
                SAMPLE_RATE,
                LINGER_TIME,
                OverToneDriver(SAMPLE_RATE, notes["F4"], 1, 8),
            ),
            "7": LingeringDriver(
                SAMPLE_RATE,
                LINGER_TIME,
                OverToneDriver(SAMPLE_RATE, notes["G4"], 1, 8),
            ),
            "8": LingeringDriver(
                SAMPLE_RATE,
                LINGER_TIME,
                OverToneDriver(SAMPLE_RATE, notes["A4"], 1, 8),
            ),
        }

    def __enter__(self):
        """
        Shim for start method so that it can be used in with statements.
        """
        self.start()

    def __exit__(self, type, value, traceback):
        """
        Shim for stop method so that it can be used in with statements.
        """
        self.stop()

    def start(self):
        """
        Building and beginning audio resources.
        """
        self.audio_instance = pyaudio.PyAudio()
        self.stream = self.audio_instance.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=SAMPLE_RATE,
            output=True,
            stream_callback=self.audio_callback,
        )
        self.stream.start_stream()

    def stop(self):
        """
        Stoping and tearing down audio resources.
        """
        self.stream.stop_stream()
        self.stream.close()
        self.audio_instance.terminate()

    def audio_callback(self, in_data, frame_count, time_info, status):
        """
        Generates audio data for the audio stream. Called at each instant the
        audio stream requires more frames.
        """
        time = self.frame_start / self.sample_rate

        wave = np.zeros(frame_count)
        for (key, driver) in self.drivers.items():
            action = self.keyboard_input.just_actioned(key)
            if action == InputAction.Pressed:
                driver.start(time)
            elif action == InputAction.Released:
                driver.stop(time)

            wave += driver.generate_frame(time, frame_count)

        self.frame_start += frame_count

        return (
            (wave * VOLUME).astype(np.float32),
            pyaudio.paContinue,
        )


def main():
    with AudioManager():
        try:
            keyboard.wait()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()

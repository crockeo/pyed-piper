import keyboard
import pyaudio
import numpy as np
import time
from typing import List

from lib.common import config
from lib.synth.driver import BaseDriver
from lib.synth.driver import DriverState
from lib.synth.driver.lingering_driver import LingeringDriver
from lib.synth.driver.over_tone_driver import OverToneDriver
from lib.synth.driver.wave_driver import WaveDriver
from lib.synth.input import InputAction
from lib.synth.input.keyboard import KeyboardInput
from lib.synth.notes import notes


class AudioManager:
    def __init__(self, drivers: List[BaseDriver] = []):
        self.drivers = drivers

        self.frame_start = 0
        self.keyboard_input = KeyboardInput()

    def __enter__(self):
        """
        Shim for start method so that it can be used in with statements.
        """
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        """
        Shim for stop method so that it can be used in with statements.
        """
        self.stop()

    def _load_drivers(self):
        pass

    def start(self):
        """
        Building and beginning audio resources.
        """
        self.audio_instance = pyaudio.PyAudio()
        self.stream = self.audio_instance.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=config.SAMPLE_RATE,
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
        time = self.frame_start / config.SAMPLE_RATE

        wave = np.zeros(frame_count)
        for (key, driver) in enumerate(self.drivers):
            action = self.keyboard_input.just_actioned(key)
            if action == InputAction.Pressed:
                driver.start(time)
            elif action == InputAction.Released:
                driver.stop(time)

            wave += driver.generate_frame(time, frame_count)

        self.frame_start += frame_count

        return (
            (wave * config.VOLUME).astype(np.float32),
            pyaudio.paContinue,
        )

    def set_driver(self, button: int, driver: BaseDriver):
        """
        Assigns the driver at a given button index to a given driver. Used to
        update the AudioManager while running.
        """
        if button < 0 or button > self.keyboard_input.get_button_count():
            raise IndexError(
                "Button must be within [0,{}], was {}".format(
                    self.keyboard_input.get_button_count(), button
                )
            )

        old_driver = self.drivers[button]
        if old_driver.get_state() == DriverState.Running:
            old_driver.stop(self.frame_start / config.SAMPLE_RATE)
        self.drivers[button] = driver

import keyboard
import pyaudio
import numpy as np
import time
from typing import List

from lib.driver import LingeringToneDriver
from lib.driver import OverToneDriver
from lib.notes import notes

VOLUME = 0.05
SAMPLE_RATE = 44100
DURATION = 1
LINGER_TIME = 0.25


drivers = {
    "1": LingeringToneDriver(
        SAMPLE_RATE, OverToneDriver(SAMPLE_RATE, notes["A3"], 1, 8), LINGER_TIME,
    ),
    "2": LingeringToneDriver(
        SAMPLE_RATE, OverToneDriver(SAMPLE_RATE, notes["B3"], 1, 8), LINGER_TIME,
    ),
    "3": LingeringToneDriver(
        SAMPLE_RATE, OverToneDriver(SAMPLE_RATE, notes["C4"], 1, 8), LINGER_TIME,
    ),
    "4": LingeringToneDriver(
        SAMPLE_RATE, OverToneDriver(SAMPLE_RATE, notes["D4"], 1, 8), LINGER_TIME,
    ),
    "5": LingeringToneDriver(
        SAMPLE_RATE, OverToneDriver(SAMPLE_RATE, notes["E4"], 1, 8), LINGER_TIME,
    ),
    "6": LingeringToneDriver(
        SAMPLE_RATE, OverToneDriver(SAMPLE_RATE, notes["F4"], 1, 8), LINGER_TIME,
    ),
    "7": LingeringToneDriver(
        SAMPLE_RATE, OverToneDriver(SAMPLE_RATE, notes["G4"], 1, 8), LINGER_TIME,
    ),
    "8": LingeringToneDriver(
        SAMPLE_RATE, OverToneDriver(SAMPLE_RATE, notes["A4"], 1, 8), LINGER_TIME,
    ),
}

frame_start = 0


def audio_callback(in_data, frame_count, time_info, status):
    global drivers
    global frame_start

    time = frame_start / SAMPLE_RATE

    wave = np.zeros(frame_count)
    for (key, driver) in drivers.items():
        if keyboard.is_pressed(key) and not driver.is_running():
            driver.start(time)
        if not keyboard.is_pressed(key) and driver.is_running():
            driver.stop(time)

        wave += driver.generate_frame(time, frame_count)

    frame_start += frame_count

    return (
        (wave * VOLUME).astype(np.float32),
        pyaudio.paContinue,
    )


def main():
    # Starting audio
    audio_instance = pyaudio.PyAudio()
    stream = audio_instance.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=SAMPLE_RATE,
        output=True,
        stream_callback=audio_callback,
    )

    stream.start_stream()

    # Waiting for user input
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        pass

    # Tearing down audio
    stream.stop_stream()
    stream.close()
    audio_instance.terminate()


if __name__ == "__main__":
    main()

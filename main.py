import keyboard
import pyaudio
import numpy as np
import time
from typing import List

from lib.driver import OverToneDriver
from lib.notes import notes
from lib.wave_generators import generate_overtone_sine_wave_frame

VOLUME = 0.5
SAMPLE_RATE = 44100
DURATION = 1


drivers = {
    "1": OverToneDriver(SAMPLE_RATE, notes["A3"], 1, 8),
    "2": OverToneDriver(SAMPLE_RATE, notes["B3"], 1, 8),
    "3": OverToneDriver(SAMPLE_RATE, notes["C4"], 1, 8),
    "4": OverToneDriver(SAMPLE_RATE, notes["D4"], 1, 8),
    "5": OverToneDriver(SAMPLE_RATE, notes["E4"], 1, 8),
    "6": OverToneDriver(SAMPLE_RATE, notes["F4"], 1, 8),
    "7": OverToneDriver(SAMPLE_RATE, notes["G4"], 1, 8),
    "8": OverToneDriver(SAMPLE_RATE, notes["A4"], 1, 8),
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
            driver.stop()

        wave += driver.generate_frame(time, frame_count)

    frame_start += frame_count

    return (
        wave.astype(np.float32),
        pyaudio.paContinue,
    )


def main():
    audio_instance = pyaudio.PyAudio()
    stream = audio_instance.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=SAMPLE_RATE,
        output=True,
        stream_callback=audio_callback,
    )

    stream.start_stream()

    try:
        keyboard.wait()
    except KeyboardInterrupt:
        pass

    stream.stop_stream()
    stream.close()
    audio_instance.terminate()


if __name__ == "__main__":
    main()

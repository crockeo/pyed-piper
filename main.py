import keyboard
import pyaudio
import time
from typing import List

from lib.notes import notes
from lib.wave_generators import generate_sine_wave
from lib.wave_generators import generate_sine_wave_frame

VOLUME = 0.5
SAMPLE_RATE = 44100
DURATION = 1


hotkeys = {
    "1": "A3",
    "2": "B3",
    "3": "C4",
    "4": "D4",
    "5": "E4",
    "6": "F4",
    "7": "G4",
    "8": "A4",
}

frame_start = 0

def audio_callback(in_data, frame_count, time_info, status):
    global frame_start

    sine_wave = generate_sine_wave_frame(
        frame_start,
        frame_start + frame_count,
        SAMPLE_RATE,
        440.0,
        0.1,
    )

    frame_start += frame_count

    return (
        sine_wave,
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

    while stream.is_active():
        keyboard.wait()

    stream.stop_stream()
    stream.close()
    audio_instance.terminate()


if __name__ == "__main__":
    main()

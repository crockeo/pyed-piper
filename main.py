import keyboard
import pyaudio
from typing import List

from lib.notes import notes
from lib.wave_generators import generate_sine_wave

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


def main():
    audio_instance = pyaudio.PyAudio()
    stream = audio_instance.open(
        format=pyaudio.paFloat32, channels=1, rate=SAMPLE_RATE, output=True
    )

    samples = {}
    for key in hotkeys:
        samples[key] = generate_sine_wave(
            DURATION, SAMPLE_RATE, notes[hotkeys[key]], 1.0
        )

        keyboard.add_hotkey(key, lambda k: stream.write(samples[k]), args=(key), suppress=True)

    try:
        keyboard.wait()
    except KeyboardInterrupt:
        pass

    stream.stop_stream()
    stream.close()
    audio_instance.terminate()


if __name__ == "__main__":
    main()

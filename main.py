import pyaudio
from typing import List

from lib.notes import notes
from lib.wave_generators import generate_sine_wave

VOLUME = 0.5
SAMPLE_RATE = 44100
DURATION = 4


def main():
    sample = generate_sine_wave(
        DURATION, SAMPLE_RATE, notes["A3"], 1.0,
    ) + generate_sine_wave(
        DURATION, SAMPLE_RATE, notes["C4"], 1.0,
    )

    audio_instance = pyaudio.PyAudio()
    stream = audio_instance.open(
        format=pyaudio.paFloat32, channels=1, rate=SAMPLE_RATE, output=True
    )
    stream.write(VOLUME * sample)
    stream.stop_stream()
    stream.close()
    audio_instance.terminate()


if __name__ == "__main__":
    main()

import pyaudio
import numpy as np
from typing import List

VOLUME = 0.5
SAMPLE_RATE = 44100
DURATION = 5


class ToneGenerator:
    def __init__(self, frequency: float):
        self.frequency = frequency

    def generate_tone(self):  # TODO: Find numpy type
        return np.sin(
            2 * np.pi * np.arange(SAMPLE_RATE * DURATION) * self.frequency / SAMPLE_RATE
        ).astype(np.float32)


class CompositeToneGenerator:
    def __init__(self, tone_generators: List[ToneGenerator]):
        self.tone_generators = tone_generators

    def generate_tone(self):  # TODO: Find numpy type
        sample = np.zeros(int(SAMPLE_RATE * DURATION))
        for tone_generator in self.tone_generators:
            tone = tone_generator.generate_tone()
            sample += tone
        sample /= len(self.tone_generators)
        return sample.astype(np.float32)


def main():
    chord = CompositeToneGenerator(
        [
            ToneGenerator(440),  # A4
            ToneGenerator(493.88),  # B4
            ToneGenerator(523.25),  # C5
        ]
    )

    sample = chord.generate_tone()

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

import pyaudio
import numpy as np
from typing import List

VOLUME = 0.5
SAMPLE_RATE = 44100
DURATION = 5


class ToneGenerator:
    def __init__(self, frequency: float):
        self.frequency = frequency

    def generate_tone(self) -> np.ndarray:
        return np.sin(
            2 * np.pi * np.arange(SAMPLE_RATE * DURATION) * self.frequency / SAMPLE_RATE
        ).astype(np.float32)


class CompositeToneGenerator:
    def __init__(self, tone_generators: List[ToneGenerator]):
        self.tone_generators = tone_generators

    def generate_tone(self) -> np.ndarray:
        sample = np.zeros(int(SAMPLE_RATE * DURATION))
        for tone_generator in self.tone_generators:
            tone = tone_generator.generate_tone()
            sample += tone
        sample /= len(self.tone_generators)
        return sample.astype(np.float32)


class OverToneGenerator:
    def  __init__(self, base_frequency: float):
        self.composite = CompositeToneGenerator([
            ToneGenerator(base_frequency * (1 + overtone))
            for overtone in range(7)
        ])

    def generate_tone(self) -> np.ndarray:
        return self.composite.generate_tone()


def main():
    chord = CompositeToneGenerator(
        [
            OverToneGenerator(440),  # A4
            OverToneGenerator(493.88),  # B4
            OverToneGenerator(523.25),  # C5
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

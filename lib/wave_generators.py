import numpy as np


def generate_sine_wave(
    duration: float, sample_rate: float, frequency: float, amplitude: float
) -> np.ndarray:
    """
    Generates a sine wave of a given duration, sample_rate, frequency, and amplitude.
    """
    return amplitude * np.sin(
        np.arange(duration * sample_rate) * 2 * np.pi * frequency / sample_rate
    ).astype(np.float32)

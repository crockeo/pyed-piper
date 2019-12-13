import numpy as np


def generate_sine_wave(
    duration: float, sample_rate: float, frequency: float, amplitude: float
) -> np.ndarray:
    """
    Generates a sine wave of a given duration, sample_rate, frequency, and amplitude.
    """
    return amplitude * np.sin(
        np.arange(duration * sample_rate) / sample_rate * 2 * np.pi * frequency
    ).astype(np.float32)


def generate_sine_wave_frame(
    start_frame, end_frame: int, sample_rate: float, frequency: float, amplitude: float,
) -> np.ndarray:
    """
    Produces a single frame of a sine wave of a given frequency and amplitude.
    """
    return amplitude * np.sin(
        np.arange(start_frame, end_frame) / sample_rate * 2 * np.pi * frequency
    ).astype(np.float32)

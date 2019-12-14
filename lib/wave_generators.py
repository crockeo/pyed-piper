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
    start_frame: int,
    end_frame: int,
    sample_rate: float,
    frequency: float,
    amplitude: float,
) -> np.ndarray:
    """
    Produces a single frame of a sine wave of a given frequency and amplitude.
    """
    return amplitude * np.sin(
        np.arange(start_frame, end_frame) / sample_rate * 2 * np.pi * frequency
    ).astype(np.float32)


def generate_overtone_sine_wave(
    duration: float,
    sample_rate: float,
    frequency: float,
    amplitude: float,
    degree: int,
) -> np.ndarray:
    """
    Produces a sine wave of a given length with overtones of the given degree.
    No overtones corresponds to generate_overtone_sine_wave of degree 1.
    """

    base_wave = generate_sine_wave(duration, sample_rate, frequency, amplitude)
    for d in range(1, degree):
        base_wave += generate_sine_wave(
            duration, sample_rate, frequency * (d + 1), amplitude / (d + 1)
        )
    return base_wave.astype(np.float32)


def generate_overtone_sine_wave_frame(
    start_frame: int,
    end_frame: int,
    sample_rate: float,
    frequency: float,
    amplitude: float,
    degree: int,
) -> np.ndarray:
    """
    Produces a sine wave for a given frame with overtones of the given degree.
    No overtones corresponds to generate_overtone_sine_wave of degree 1.
    """

    base_wave = generate_sine_wave_frame(
        start_frame, end_frame, sample_rate, frequency, amplitude
    )
    for d in range(1, degree):
        base_wave += generate_sine_wave_frame(
            start_frame,
            end_frame,
            sample_rate,
            frequency * (d + 1),
            amplitude / (d + 1),
        )
    return base_wave.astype(np.float32)

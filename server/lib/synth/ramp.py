import numpy as np
from typing import Tuple


def _get_ramp_positions(
    sample_rate: float,
    start_time: float,
    end_time: float,
    current_time: float,
    frame_count: int,
) -> Tuple[float, float]:
    """
    Gets the positions of the start and end time of a given frame in its
    position in a ramp. Returned as a percentage of its completion, with the
    exception that if the frame count is too large, the end time may exceed 1.0
    """
    return (
        (current_time - start_time) / (end_time - start_time),
        ((current_time + frame_count / sample_rate) - start_time)
        / (end_time - start_time),
    )


def linear_ramp(
    sample_rate: float,
    start_time: float,
    end_time: float,
    current_time: float,
    frame_count: int,
) -> np.ndarray:
    """
    Generates a linear ramp between the start time and the end time. Linearly
    decreases from 1.0 to 0.0 across the provided times.

    If generated during a frame that would exceed the end_time, it clamps the
    ramp to 0.0.
    """
    start, end = _get_ramp_positions(
        sample_rate, start_time, end_time, current_time, frame_count
    )

    return np.maximum(np.linspace(1 - start, 1 - end, frame_count), 0)


def exponential_ramp(
    sample_rate: float,
    start_time: float,
    end_time: float,
    current_time: float,
    frame_count: int,
) -> np.ndarray:
    """
    Generates an exponential ramp between the start time and the end time.
    """
    start, end = _get_ramp_positions(
        sample_rate, start_time, end_time, current_time, frame_count,
    )

    return np.maximum(1 / (np.linspace(start + 1, end + 1, frame_count) ** 8), 0)

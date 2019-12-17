from enum import Enum
import numpy as np
import os
from typing import Union
import wave

from lib import ramp


class DriverState(Enum):
    Stopped = 0
    Stopping = 1
    Running = 2

    def __le__(self, other: DriverState):
        return self <= other


class BaseDriver:
    """
    Root class that defines the required interface for an audio driver.
    """

    def start(self, time: float):
        raise NotImplementedError(
            "BaseDriver.start not implemented in {}".format(self.__class__.__name__)
        )

    def stop(self, time: float):
        raise NotImplementedError(
            "BaseDriver.stop not implemented in {}".format(self.__class__.__name__)
        )

    def get_state(self) -> DriverState:
        raise NotImplementedError(
            "BaseDriver.get_state not implemented in {}".format(self.__class__.__name__)
        )

    def generate_frame(self, time: float, frame_count: int) -> np.ndarray:
        raise NotImplementedError(
            "BaseDriver.generate_frame not implemented in {}".format(
                self.__class__.__name__
            )
        )


class ToneDriver(BaseDriver):
    """
    An audio driver that plays a smooth tone at a given frequency. Does not
    implement any kind of overtone. Implements smart stopping to prevent audio
    pops.
    """

    def __init__(
        self, sample_rate: float, frequency: float, amplitude: float,
    ):
        self.sample_rate = sample_rate
        self.frequency = frequency
        self.amplitude = amplitude

        self.start_time = 0.0
        self.state = DriverState.Stopped

    def start(self, time: float):
        self.start_time = time
        self.state = DriverState.Running

    def stop(self, time: float):
        self.state = DriverState.Stopping

    def get_state(self) -> DriverState:
        return self.state

    def generate_frame(self, time: float, frame_count: int) -> np.ndarray:
        if self.state == DriverState.Stopped:
            return np.zeros(frame_count).astype(np.float32)

        frame_begin_time = time - self.start_time
        wave = self.amplitude * np.sin(
            2
            * np.pi
            * self.frequency
            * (frame_begin_time + (np.arange(frame_count)) / self.sample_rate)
        )

        # TODO: Find out how to zero without having to loop through the entire
        #       wave. It's only ever 1024 frames wide, but still not great.
        if self.state == DriverState.Stopping:
            # If we're trying to stop, first we need to generate enough of the
            # tone to zero out the wave. Otherwise you hear a pop when you
            # release a button.
            boundary = -1
            for i in range(len(wave) - 1):
                if (wave[i] <= 0 and wave[i + 1] > 0) or (
                    wave[i] >= 0 and wave[i + 1] < 0
                ):
                    boundary = i
                    break

            if boundary > 0:
                wave[boundary + 1 :] = np.zeros(len(wave) - boundary - 1)
                self.state = DriverState.Stopped

        return wave.astype(np.float32)


class OverToneDriver(BaseDriver):
    """
    An audio driver that plays a frequency with degrees of overtone. The
    overtones are automatically scaled down in volume to maintain true-to-life
    conservation of energy.
    """

    def __init__(
        self, sample_rate: float, frequency: float, amplitude: float, degree: int
    ):
        self.sub_drivers = [
            ToneDriver(sample_rate, frequency, amplitude / (d + 1))
            for d in range(degree)
        ]

    def start(self, time: float):
        for sub_driver in self.sub_drivers:
            sub_driver.start(time)

    def stop(self, time: float):
        for sub_driver in self.sub_drivers:
            sub_driver.stop(time)

    def get_state(self) -> DriverState:
        return max([sub_driver.get_state() for sub_driver in self.sub_drivers])

    def generate_frame(self, time: float, frame_count: int) -> np.ndarray:
        wave = np.zeros(frame_count)
        for sub_driver in self.sub_drivers:
            wave += sub_driver.generate_frame(time, frame_count)
        return wave.astype(np.float32)


class LingeringDriver(BaseDriver):
    """
    An audio driver that lingers for a set period of time after being stopped.
    Used to simulate how stringed instruments will continue to emit sound, even
    after a string is released.
    """

    def __init__(self, sample_rate: float, linger_time: float, driver: BaseDriver):
        self.sample_rate = sample_rate
        self.driver = driver
        self.linger_time = linger_time

        self.state = DriverState.Stopped
        self.stop_time = 0.0

    def start(self, time: float):
        self.driver.start(time)
        self.state = DriverState.Running

    def stop(self, time: float):
        self.state = DriverState.Stopping
        self.stop_time = time

    def is_running(self):
        return not self.state == DriverState.Stopped

    def generate_frame(self, time: float, frame_count: int) -> np.ndarray:
        if not self.is_running():
            return np.zeros(frame_count).astype(np.float32)

        wave = self.driver.generate_frame(time, frame_count)
        if self.state == DriverState.Stopping:
            wave *= ramp.exponential_ramp(
                self.sample_rate,
                self.stop_time,
                self.stop_time + self.linger_time,
                time,
                frame_count,
            )

            if (
                time + frame_count / self.sample_rate
                >= self.stop_time + self.linger_time
            ):
                self.state = DriverState.Stopped
                self.driver.stop(time)

        return wave.astype(np.float32)

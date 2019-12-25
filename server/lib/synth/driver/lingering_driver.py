import numpy as np

from lib.synth.driver import BaseDriver
from lib.synth.driver import DriverState
from lib.synth.ramp import exponential_ramp


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

    def get_state(self) -> DriverState:
        return self.state

    def generate_frame(self, time: float, frame_count: int) -> np.ndarray:
        if self.get_state() == DriverState.Stopped:
            return np.zeros(frame_count).astype(np.float32)

        wave = self.driver.generate_frame(time, frame_count)
        if self.state == DriverState.Stopping:
            wave *= exponential_ramp(
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

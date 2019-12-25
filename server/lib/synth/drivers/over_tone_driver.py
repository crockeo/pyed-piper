import numpy as np

from lib.synth.drivers import BaseDriver
from lib.synth.drivers import DriverState
from lib.synth.drivers.tone_driver import ToneDriver


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

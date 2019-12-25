import numpy as np

from lib.synth.driver import BaseDriver
from lib.synth.driver import DriverState


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

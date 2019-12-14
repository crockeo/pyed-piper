import numpy as np


class BaseDriver:
    def start(self, time: float):
        raise NotImplementedError(
            "BaseDriver.start not implemented in {}".format(self.__class__.__name__)
        )

    def stop(self):
        raise NotImplementedError(
            "BaseDriver.stop not implemented in {}".format(self.__class__.__name__)
        )

    def is_running(self) -> bool:
        raise NotImplementedError(
            "BaseDriver.is_running not implemented in {}".format(
                self.__class__.__name__
            )
        )

    def generate_frame(self, time: float, frame_count: int) -> np.ndarray:
        raise NotImplementedError(
            "BaseDriver.generate_frame not implemented in {}".format(
                self.__class__.__name__
            )
        )


class ToneDriver(BaseDriver):
    def __init__(
        self, sample_rate: float, frequency: float, amplitude: float,
    ):
        self.sample_rate = sample_rate
        self.frequency = frequency
        self.amplitude = amplitude

        self.start_time = 0
        self.running = False

    def start(self, time: float):
        self.start_time = time
        self.running = True

    def stop(self):
        self.running = False

    def is_running(self):
        return self.running

    def generate_frame(self, time: float, frame_count: int) -> np.ndarray:
        if not self.is_running():
            return np.zeros(frame_count).astype(np.float32)

        frame_begin_time = time - self.start_time
        return self.amplitude * np.sin(
            2
            * np.pi
            * self.frequency
            * (frame_begin_time + (np.arange(frame_count)) / self.sample_rate),
        ).astype(np.float32)

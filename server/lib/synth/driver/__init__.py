from enum import Enum
import numpy as np


class DriverState(Enum):
    Stopped = 0
    Stopping = 1
    Running = 2

    def __le__(self, other: "DriverState"):
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

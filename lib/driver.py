import numpy as np


class BaseDriver:
    def start(self, time: float):
        raise NotImplementedError(
            "BaseDriver.start not implemented in {}".format(self.__class__.__name__)
        )

    def stop(self, time: float):
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
        self.zeroed = True

    def start(self, time: float):
        self.start_time = time
        self.running = True
        self.zeroed = False

    def stop(self, time: float):
        self.running = False

    def is_running(self):
        return self.running or not self.zeroed

    def generate_frame(self, time: float, frame_count: int) -> np.ndarray:
        if not self.is_running():
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
        if not self.running and not self.zeroed:
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
                self.zeroed = True

        return wave.astype(np.float32)


class OverToneDriver(BaseDriver):
    def __init__(
        self, sample_rate: float, frequency: float, amplitude: float, degree: float
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

    def is_running(self):
        for sub_driver in self.sub_drivers:
            if sub_driver.is_running():
                return True
        return False

    def generate_frame(self, time: float, frame_width: int) -> np.ndarray:
        wave = np.zeros(frame_width)
        for sub_driver in self.sub_drivers:
            wave += sub_driver.generate_frame(time, frame_width)
        return wave.astype(np.float32)


class LingeringToneDriver(BaseDriver):
    def __init__(self, sample_rate: float, driver: BaseDriver, linger_time: float):
        self.sample_rate = sample_rate
        self.driver = driver
        self.linger_time = linger_time

        self.stopping = False
        self.stop_time = 0

    def start(self, time: float):
        self.driver.start(time)
        self.stopping = False

    def stop(self, time: float):
        self.stopping = True
        self.stop_time = time

    def is_running(self):
        return self.driver.is_running() and not self.stopping

    def generate_frame(self, time: float, frame_width: int) -> np.ndarray:
        wave = self.driver.generate_frame(time, frame_width)
        if self.stopping:
            start_gradient = 1 - ((time - self.stop_time) / self.linger_time)
            end_gradient = 1 - (
                (time - self.stop_time + frame_width / self.sample_rate)
                / self.linger_time
            )

            wave *= np.maximum(
                np.linspace(start_gradient, end_gradient, frame_width), 0,
            )

            if start_gradient < 0:
                self.driver.stop(time)
                self.stopping = False

        return wave.astype(np.float32)

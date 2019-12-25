import numpy as np
import struct
import wave

from lib.synth.driver import BaseDriver
from lib.synth.driver import DriverState


class WaveDriver(BaseDriver):
    """
    An audio driver that plays a sample from a .wav file.
    """

    def __init__(
        self, sample_rate: float, path: str, channel_preference: int = 0,
    ):
        self.wave_read = wave.open(path, "rb")
        if self.wave_read.getsampwidth() not in {1, 2, 4}:
            raise ValueError(".wav file must be 8-, 16-, or 32-bit depth")

        self.sample_rate = sample_rate
        self.channel_preference = channel_preference

        self.state = DriverState.Stopped

    def start(self, time: float):
        self.wave_read.rewind()
        self.state = DriverState.Running

    def stop(self, time: float):
        self.state = DriverState.Stopping

    def get_state(self) -> DriverState:
        return self.state

    def generate_frame(self, time: float, frame_count: int) -> np.ndarray:
        if self.get_state() == DriverState.Stopped:
            return np.zeros(frame_count).astype(np.float32)

        if self.state == DriverState.Stopping:
            # TODO: Actually stop smoothly
            self.state = DriverState.Stopped

        return self._convert_wave_data(self.wave_read.readframes(frame_count)).astype(
            np.float32
        )

    def _convert_wave_data(self, wave_data: bytes) -> np.ndarray:
        frame_width = self.wave_read.getsampwidth()
        format_chars = {
            1: "c",  # 8-bit depth -> char
            2: "h",  # 16-bit depth -> short
            4: "i",  # 32-bit depth -> int
        }

        # Retrieving usable data from the wave_data bytes object.
        base_wave = np.array(
            struct.unpack(
                "{}{}".format(
                    len(wave_data) // frame_width, format_chars[frame_width],
                ),
                wave_data,
            ),
            dtype="float",
        )

        # Selecting only the channel we prefer
        channel_count = self.wave_read.getnchannels()
        wave = np.zeros(len(wave_data) // frame_width // channel_count)
        for channel in range(channel_count):
            wave += base_wave[channel::channel_count]
        wave /= channel_count

        # Scaling from integer format to float format
        wave /= np.power(2, self.wave_read.getsampwidth() * 8 - 1)

        return wave

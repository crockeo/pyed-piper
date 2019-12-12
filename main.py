import pyaudio
import numpy as np

volume = 0.5
fs = 44100
duration = 3.0
f = 440.0

def main():
    samples = (
        np.sin(
            2 * np.pi * np.arange(
                fs * duration,
            ) * f / fs,
        )
    ).astype(np.float32)

    audio_instance = pyaudio.PyAudio()
    stream = audio_instance.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=True)
    stream.write(volume * samples)
    stream.stop_stream()
    stream.close()
    audio_instance.terminate()

if __name__ == '__main__':
    main()

import numpy as np


class TestModule:
    """
    stand in for Sound Module class

    generates wave data from input midi data
    """

    def __init__(self) -> None:
        self.phase = 0

    def play(self, note):
        """
        work in progress

        still trying to solve issue where sound waves do not align
        from one loop to the next (which causes the clipping effect)

        """
        print(f"play {note}")

        fs = 48000  # sampling rate, Hz, must be integer
        duration = 0.1  # in seconds, may be float
        f = 440.0  # sine frequency, Hz, may be float
        f = (f / 32) * (2 ** ((note - 9) / 12))  # converts midi note to hz

        # samples = (np.sin((2*np.pi*np.arange(fs*duration)*f/fs))+self.wave_delta_arcsin)
        length = fs * duration
        factor = (np.pi * 2) * float(f) / fs
        self.phase += factor
        samples = np.sin(np.arange(length) * factor)
        np.append(samples, np.sin(self.phase))

        return samples.astype(np.float32)

    def stop(self, note):
        print(f"stop {note}")

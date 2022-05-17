import numpy as np

class TestModule:

    def play(self, note):
        print(f"play {note}")

        fs = 48000       # sampling rate, Hz, must be integer
        duration = .3   # in seconds, may be float
        f = 440.0        # sine frequency, Hz, may be float
        f = (f/32) * (2 ** ((note - 9) / 12))

        samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
        return samples



    def stop(self, note):
        print(f"stop {note}")
    
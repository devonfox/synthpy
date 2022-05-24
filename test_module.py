import numpy as np

class TestModule:

    def play(self, note):
        print(f"play {note}")

        fs = 48000       # sampling rate, Hz, must be integer
        f = 440.0        # sine frequency, Hz, may be float
        f = (f) * (2 ** ((note - 69) / 12))
        duration = (2*np.pi)/f # in seconds, may be float
        # need to adjust this duration to fit the period of the wave, or
        # maybe a chunk of samples slightly larger might sound better to account for any latency adding to stream

        # possibly change 

        samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
        return samples



    def stop(self, note):
        print(f"stop {note}")
    
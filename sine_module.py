import numpy as np

class SineModule:

    def play(self, note, chunk):
        print(f"play {note}")

        fs = 48000       # sampling rate, Hz, must be integer
        f = 440 * 2**((note - 69) / 12)
        period = 2 * np.pi * f / fs 
        # duration = .3 # in seconds, may be float

        # do not need a duration, we want to keep creating this as long as the note is held, and
        # then return the full samples, and stream it chunk by chunk to the audio callback, with
        # minimal delay
        
        # possibly change 
        t = np.linspace(0, chunk, chunk , False)
        wave = np.sin(f * t * 2 * np.pi)
        # samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
        return wave



    def stop(self, note):
        print(f"stop {note}")
    
import numpy as np
import math

ii16 = np.iinfo(np.int16)  # global max/min int16 values

# I'm thinking it may be best to simply change this to be in the synth class
# and then we make a math module for each type, and that just runs in so we
# don't end up repeating a bunch of code


class SineModule:
    def __init__(self, arg) -> None:
        self.arg = arg  # arguments from main
        self.fs = 48000
        self.index = 0

    def play(self, note):
        if note:
            f = 440 * 2**((note - 69) / 12)
            # increment sample framces by this
            inc = 1 / (self.fs / self.arg.chunk)
            # print(f)
            if self.index < inc:  # prints note for debugging just once after key is pressed
                print("Debug Note: ", note)

            # creates a sine chunk for just a 'chunk' of samples the size of the buffer argument
            t = np.linspace(self.index, self.index +
                            inc, self.arg.chunk, False)
            wave = np.sin(f * t * 2 * np.pi)  # float calculation
            wave *= ii16.max * \
                self.getAmp(self.arg.volume) / max(abs(wave))  # normalizing
            wave = wave.astype(np.int16)  # converts back to int16
            self.index += inc  # increments current endpoint for sine calc
        else:
            self.index = 0  # starts calc back over for sine

            # sends chunks of silence to play call, sending silence to sounddevice
            wave = np.zeros(self.arg.chunk).astype(np.int16)

        return wave

    # Function takes volume arguments and returns equivalent 0.0 - 1.0 ratio
    def getAmp(self, vol):
        exp = ((-6 * (10 - vol)) / 20)
        amp = math.pow(10, exp)
        return amp

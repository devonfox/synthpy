import numpy as np
import math
from adsr import ADSR

ii16 = np.iinfo(np.int16)  # global max/min int16 values

# I'm thinking it may be best to simply change this to be in the synth class
# and then we make a math module for each type, and that just runs in so we
# don't end up repeating a bunch of code


class SoundModule:
    def __init__(self, arg) -> None:
        self.arg = arg  # arguments from main
        self.fs = 48000
        self.index = 0
        self.samples = 0
        self.asdr = ADSR()
        self.inc = 1 / (self.fs / self.arg.chunk)

        self.current_note = None
        self.previous_note = None

    def play(self, note):
        self.previous_note = self.current_note
        self.current_note = note
        if note:

            # creates a sine chunk for just a 'chunk' of samples the size of the buffer argument
            wave = self.calculate_wave_data()
            # reset for new note
            if self.current_note != self.previous_note:
                self.samples = 0
            wave = self.asdr.apply_envelope(wave, self.samples)

            wave = wave.astype(np.int16)  # converts back to int16
            self.index += self.inc  # increments current endpoint for sine calc
            self.samples += self.arg.chunk
        else:
            self.index = 0  # starts calc back over for sine
            self.samples = 0

            # sends chunks of silence to play call, sending silence to sounddevice
            wave = np.zeros(self.arg.chunk).astype(np.int16)

        return wave

    # Function takes volume arguments and returns equivalent 0.0 - 1.0 ratio
    def getAmp(self, vol):
        exp = (-6 * (10 - vol)) / 20
        amp = math.pow(10, exp)
        return amp

    def calculate_wave_data(self):
        f = 440 * 2 ** ((self.current_note - 69) / 12)
        if (
            self.index < self.inc
        ):  # prints note for debugging just once after key is pressed
            print("Debug Note: ", self.current_note)
        t = np.linspace(self.index, self.index + self.inc, self.arg.chunk, False)
        wave = np.sin(f * t * 2 * np.pi)  # float calculation
        wave *= ii16.max * self.getAmp(self.arg.volume) / max(abs(wave))  # normalizing

        return wave

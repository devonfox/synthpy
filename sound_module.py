import numpy as np
import math
from adsr import ADSR

class SoundModule:
    def __init__(self, arg, wavetype) -> None:

        self.wavetype = wavetype
        self.arg = arg  # arguments from main
        self.fs = 48000
        self.index = 0
        self.samples = 1
        self.asdr = ADSR(arg)
        self.inc = self.arg.chunk / self.fs

        self.current_note = None
        self.previous_note = None
        
        

    def play(self, note):
        self.previous_note = self.current_note
        self.current_note = note
        if note:
            if self.wavetype == 1:
                wave = self.square()
            elif self.wavetype == 2:
                wave = self.sine()
            
            # reset for new note
            if self.current_note != self.previous_note:
                self.samples = 1
            
            wave = self.asdr.apply_envelope(wave, self.samples)

            wave = wave.astype(np.float32)  # converts back to f32 from f64
            self.index += self.inc  # increments current endpoint for sine calc
            self.samples += self.arg.chunk
        else:
            self.index = 0  # starts calc back over for sine
            self.samples = 1

            # sends chunks of silence to play call, sending silence to sounddevice
            wave = np.zeros(self.arg.chunk).astype(np.float32)

        return wave

    # Function takes volume arguments and returns equivalent 0.0 - 1.0 ratio
    def getAmp(self, vol):
        exp = (-6 * (10 - vol)) / 20
        amp = math.pow(10, exp)
        return amp

    def sine(self):
        f = 440 * 2 ** ((self.current_note - 69) / 12)
        if (
            self.index < self.inc
        ):  # prints note for debugging just once after key is pressed
            print("Debug Note: ", self.current_note)
        t = np.linspace(self.index, self.index + self.inc, self.arg.chunk, False)
        wave = np.sin(f * t * 2 * np.pi) * self.getAmp(self.arg.volume)  # float calculation

        return wave
    
    def square(self):
        f = 440 * 2 ** ((self.current_note - 69) / 12)
        if (
            self.index < self.inc
        ):  # prints note for debugging just once after key is pressed
            print("Debug Note: ", self.current_note)
        t = np.linspace(self.index, self.index + self.inc, self.arg.chunk, False)
        wave = 4 * np.floor(f * t) - 2 * np.floor(2*f * t) + 1  # float calculation
        wave *= self.getAmp(self.arg.volume)

        return wave

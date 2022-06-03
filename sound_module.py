import numpy as np
import math
from adsr import ADSR
from scipy import signal

class SoundModule:
    def __init__(self, arg) -> None:

        self.wavetype = arg.wave
        self.arg = arg  # arguments from main
        self.fs = 48000
        self.index = 0
        self.samples = 0
        self.asdr = ADSR(arg)
        self.inc = self.arg.chunk / self.fs
        self.attidx = 0
        self.relidx = self.asdr.release
        self.relswitch = False
        # self.endpoint = 0

        self.current_note = None
        self.previous_note = None
        
        

    def play(self, note):
        
        if note:
            self.previous_note = self.current_note
            self.current_note = note
            wave = self.compute_wave()
            # reset for new note
            if self.current_note != self.previous_note:
                self.samples = 0
                # self.endpoint = 0
                # self.relidx = self.asdr.release
            
            wave = self.asdr.apply_envelope(wave, self.samples)

            wave = wave.astype(np.float32)  # converts back to f32 from f64
            self.index += self.inc  # increments current endpoint for sine call
            self.samples += self.arg.chunk
            # self.endpoint = self.samples
            # if self.samples < self.asdr.attack:
            #     self.relidx = self.samples
            # else:
            #     self.relidx = self.asdr.release
            # print(self.relidx)
            
        else:
            
            # print(self.relidx)
            if self.samples > 0 and self.relidx >= 0:
                if self.relswitch is False:
                    if self.samples < self.asdr.attack:
                        self.relidx = self.samples
                    self.relswitch = True
                wave = self.compute_wave()
                wave = self.asdr.apply_release(wave, self.relidx)
                wave = wave.astype(np.float32)  # converts back to f32 from f64
                self.relidx -= self.arg.chunk
                self.samples += self.arg.chunk
                self.index += self.inc
                
            else:
                self.index = 0  # starts calc back over for sine
                self.samples = 0
                # self.endpoint = 0
                self.relidx = self.asdr.release
                self.relswitch = False
            # sends chunks of silence to play call, sending silence to sounddevice
                wave = np.zeros(self.arg.chunk).astype(np.float32)

        return wave

    # Function takes volume arguments and returns equivalent 0.0 - 1.0 ratio
    def getAmp(self, vol):
        exp = (-6 * (10 - vol)) / 20
        amp = math.pow(10, exp)
        return amp

    def compute_wave(self):
        f = 440 * 2 ** ((self.current_note - 69) / 12) 
        t = np.linspace(self.index, self.index + self.inc, self.arg.chunk, False)
        if self.wavetype == 'square':
            wave = self.square(t, f)
        elif self.wavetype == 'sine':
            wave = self.sine(t, f)
        elif self.wavetype == 'tri':
            wave = self.triangle(t, f)
            
        wave *= self.getAmp(self.arg.volume)

        return wave
    
    def sine(self, t, f):
        return np.sin(f * t * 2 * np.pi)


    def square(self, t, f):
        return 4 * np.floor(f * t) - 2 * np.floor(2*f * t) + 1  # float calculation
        
    def triangle(self, t, f):
        return 2 * np.abs(2 * (t/f) - np.floor((t/f) + 0.5)) - 1
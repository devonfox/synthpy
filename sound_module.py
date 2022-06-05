import numpy as np
import math
from adsr import ADSR


class SoundModule:
    def __init__(self, arg) -> None:

        self.wavetype = arg.wave
        self.arg = arg  # arguments from main
        self.fs = 48000
        self.asdr = ADSR(arg)
        self.inc = self.arg.chunk / self.fs
        
        self.current_note = 0
        self.previous_note = 0

    def play(self, note):
        
        if note.state == True:
            self.previous_note = self.current_note
            self.current_note = note.key
            wave = self.compute_wave(note)

            # still need to account for this, but in a different way

                # reset for new note
                # if self.current_note != self.previous_note:
                #     note.samples = 0
                #     note.relidx = self.asdr.release
                #     note.index = 0
                #     note.relswitch = False
            
            wave = self.asdr.apply_envelope(wave, note.samples, note)

            wave = wave.astype(np.float32)  # converts back to f32 from f64
            note.index += self.inc  # increments current endpoint for sine call
            note.samples += self.arg.chunk
    
            
        else:
            
            # print(f"Note: {note.key} -> Relidx: {note.relidx}")
            if note.samples > 0 and note.relidx >= 0:
                if note.relswitch is False:
                    note.relswitch = True
                wave = self.compute_wave(note)
                wave = self.asdr.apply_release(wave, note.relidx)
                wave = wave.astype(np.float32)  # converts back to f32 from f64
                note.relidx -= self.arg.chunk
                note.samples += self.arg.chunk
                note.index += self.inc
                
            else:
                if note.relswitch is True:
                    wave = self.round(note)
                note.relswitch = False
                note.index = 0  # starts calc back over for sine
                note.samples = 0
                note.relidx = self.asdr.release
                note.level = 1.0
            # sends chunks of silence to play call, sending silence to sounddevice
                wave = np.zeros(self.arg.chunk).astype(np.float32)

        return wave

    # Function takes volume arguments and returns equivalent 0.0 - 1.0 ratio
    def getAmp(self, vol):
        exp = (-6 * (10 - vol)) / 20
        amp = math.pow(10, exp)
        return amp

    def compute_wave(self, note):
        f = 440 * 2 ** ((note.key - 69) / 12) 
        t = np.linspace(note.index, note.index + self.inc, self.arg.chunk, False)
        if self.wavetype == 'square':
            wave = self.square(t, f)
        elif self.wavetype == 'sine':
            wave = self.sine(t, f)
        elif self.wavetype == 'tri':
            wave = self.triangle(t, f)
        
        if note.relswitch is True:
            wave *= self.getAmp(self.arg.volume)
            wave *= note.level
        else:
            wave *= self.getAmp(self.arg.volume)

        return wave
    
    def round(self, note):
        wave = self.compute_wave(note)
        length = len(wave)
        for index, _ in enumerate(wave):
            wave[index] *= self.getAmp(10 * ((length - index) / length))
            wave *= note.level
        wave = wave.astype(np.float32)

        return wave

    
    def sine(self, t, f):
        return np.sin(f * t * 2 * np.pi)


    def square(self, t, f):
        return 4 * np.floor(f * t) - 2 * np.floor(2*f * t) + 1  # float calculation
        
    def triangle(self, t, f):
        return 2 * np.abs(2 * (t/f) - np.floor((t/f) + 0.5)) - 1
    

class Note:
        def __init__(self, k, arg) -> None:
            self.state = False
            self.key = k 
            self.index = 0
            self.samples = 0
            self.relidx = arg.release * 48000
            self.relswitch = False
            self.level = 1.0
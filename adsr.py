import math

class ADSR:
    def __init__(self) -> None:
        self.fs = 48000
        self.attack = self.fs * 1
        self.decay = 0.25
        self.sustain = 0.25
        self.release = 0.25

    def set_attack(self, attack: float):
        self.attack = attack

    def set_decay(self, decay: float):
        self.decay = decay

    def set_sustain(self, sustain):
        self.sustain = sustain

    def set_release(self, release):
        self.release = release
    
    def getAmp(self, vol):
        exp = (-6 * (10 - vol)) / 20
        amp = math.pow(10, exp)
        return amp

    def apply_envelope(self, wave_data: list, samples: int) -> list:

        if samples < self.attack:
            wave_data = self.apply_attack(wave_data, samples)

        return wave_data

    def apply_attack(self, wave_data: list, samples: int) -> list:
        for index, _ in enumerate(wave_data):

            #  TODO: Fix small click at end of attack 
            att = 10 * ((samples+index+1)/self.attack)
            wave_data[index] *= self.getAmp(att)
            # wave_data[index] *= ((samples+index+1)/self.attack)

        return wave_data

import math


class ADSR:
    def __init__(self, arg) -> None:
        self.fs = 48000
        self.attack = self.fs * arg.attack + 0.001
        self.decay = self.fs * arg.decay
        self.sustain = arg.sustain + 0.0001
        self.release = self.fs * arg.release + 0.001
        self.ddec = self.set_ddec(self.decay)
        self.arg = arg

    def set_ddec(self, decay: float):
        if decay != 0:
            return (1 - self.sustain) / decay
        return 0

    def apply_envelope(self, wave_data: list, samples: int, note) -> list:

        if samples <= self.attack:
            wave_data = self.apply_attack(wave_data, samples, note)
        elif samples > self.attack and samples < (self.attack + self.decay):
            wave_data = self.apply_decay(wave_data, note)
        elif samples > (self.attack + self.decay):
            wave_data *= self.sustain
            note.level = self.sustain
        return wave_data

    def apply_attack(self, wave_data: list, samples: int, note) -> list:
        for index, _ in enumerate(wave_data):

            wave_data[index] *= ((samples+index+1)/self.attack)
            note.level = ((samples+index+1)/self.attack)

        return wave_data

    def apply_decay(self, wave_data: list, note) -> list:
        for index, _ in enumerate(wave_data):
            wave_data[index] *= note.declevel
            note.level = note.declevel
            note.declevel -= self.ddec

        return wave_data

    def apply_release(self, wave_data: list, rel: int) -> list:
        for index, _ in enumerate(wave_data):
            wave_data[index] *= ((rel - index) / self.release)

        return wave_data

    def getAmp(self, vol):
        exp = (-6 * (10 - vol)) / 20
        amp = math.pow(10, exp)
        return amp

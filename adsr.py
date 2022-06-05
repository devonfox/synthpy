import math


class ADSR:
    def __init__(self, arg) -> None:
        self.fs = 48000
        self.attack = self.fs * arg.attack
        self.decay = 0.25
        self.sustain = 0.25
        self.release = self.fs * arg.release
        self.arg = arg

    def set_attack(self, attack: float):
        self.attack = attack

    def set_decay(self, decay: float):
        self.decay = decay

    def set_sustain(self, sustain): # todo Sunday
        self.sustain = sustain

    def set_release(self, release): # todo Sunday
        self.release = release

    def apply_envelope(self, wave_data: list, samples: int, note) -> list:

        if samples < self.attack:
            wave_data = self.apply_attack(wave_data, samples, note)
        # add decay
        # then add sustain
        return wave_data

    def apply_attack(self, wave_data: list, samples: int, note) -> list:
        for index, _ in enumerate(wave_data):

            wave_data[index] *= ((samples+index+1)/self.attack)
            note.level = ((samples+index+1)/self.attack)

        return wave_data

    def apply_release(self, wave_data: list, rel: int) -> list:
        for index, _ in enumerate(wave_data):
            wave_data[index] *= ((rel - index) / self.release)

        return wave_data

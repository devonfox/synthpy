class ADSR:
    def __init__(self) -> None:
        self.fs = 48000
        self.attack = self.fs * 2
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

    def apply_envelope(self, wave_data: list, samples: int) -> list:
        if samples < self.attack:
            wave_data = self.apply_attack(wave_data, samples)

        return wave_data

    def apply_attack(self, wave_data: list, samples: int) -> list:
        for index, _ in enumerate(wave_data):
            wave_data[index] *= samples / self.attack

        return wave_data

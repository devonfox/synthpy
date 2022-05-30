

class ADSR:
    def __init__(self) -> None:
        self.attack = 5
        self.decay = 0.25
        self.sustain = 0.25
        self.release = 0.25
        self.previous_note = None
        self.current_note = None
        self.note_time = 0.0
        self.attack_increment = 0.0
        self.chunk_count = 1

    def set_attack(self, attack: float):
        self.attack = attack

    def set_decay(self, decay: float):
        self.decay = decay

    def set_sustain(self, sustain):
        self.sustain = sustain

    def set_release(self, release):
        self.release = release

    def apply_envelope(self, wave_data: list, note) -> list:
        self.previous_note = self.current_note
        self.current_note = note
        if self.previous_note != self.current_note:
            self.chunk_count = round(512 / self.attack, 0)
            self.note_time = 0.0
            self.attack_increment = 0.01
        if self.note_time <= self.attack:
            for frame in wave_data:
                frame *= (self.note_time/self.attack)
                self.note_time += self.chunk_count / 512

        return wave_data

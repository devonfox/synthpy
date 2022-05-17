from midi_interface import MidiInterface
from test_module import TestModule
import pyaudio


class Synth:
    def __init__(self, sound_moudle=TestModule()) -> None:
        self.p = pyaudio.PyAudio()
        self.volume = 0.5  # range [0.0, 1.0]
        self.fs = 48000  # sampling rate, Hz, must be integer
        self.midi_interface = MidiInterface(self.process_midi)
        self.sound_module = sound_moudle
        self.note = None
        self.stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.fs,
            output=True,
        )

    def play(self):
        self.stream.start_stream()
        while True:
            if self.note:
                self.stream.write(self.volume * self.sound_module.play(self.note))

    def process_midi(self, message):
        msg = message
        if msg.type == "note_on":
            self.note = msg.note
        elif msg.type == "note_off":
            if msg.note == self.note:
                self.note = None
                print(f"stop")

from midi_interface import MidiInterface
from test_module import TestModule
from effects import Toaster
import pyaudio
import sounddevice as sd


class Synth:
    def __init__(self, sound_moudle=TestModule(), effect=None) -> None:
        # self.p = pyaudio.PyAudio()
        self.volume = 0.5  # range [0.0, 1.0]
        self.fs = 48000  # sampling rate, Hz, must be integer
        self.midi_interface = MidiInterface(self.process_midi)
        self.sound_module = sound_moudle
        self.effect = effect
        self.note = None
        # self.stream = self.p.open(
        #     format=pyaudio.paFloat32,
        #     channels=1,
        #     rate=self.fs,
        #     output=True,
        # )
    def callback(self, indata, outdata, frames, time, status):
        if self.note:
            outdata[:] = self.output_data()


    def play(self):
        # self.stream.start_stream()

        with sd.Stream(channels=1, callback=self.callback):
            while True:
                pass
                # if self.note:
                    # self.stream.write(self.output_data())
                    # indata = self.output_data()

    def process_midi(self, message):
        msg = message
        if msg.type == "note_on":
            # self.stream.start_stream()
            self.note = msg.note
        elif msg.type == "note_off":
            if msg.note == self.note:
                # self.stream.stop_stream()
                self.note = None
                print(f"stop")

    def output_data(self):
        data = self.volume * self.sound_module.play(self.note)
        if self.effect:
            data = self.effect.apply_effect(data)
        return data

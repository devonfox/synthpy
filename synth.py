# from xml.sax import parseString
from effects import Toaster
from sound_module import SoundModule, Note
import sounddevice as sd
import numpy as np
import mido

# setting up default sounddevice settings
sd.default.channels = 1
sd.default.samplerate = 48000


class Synth:
    def __init__(self, arg, effect=None) -> None:
        self.arg = arg
        self.volume = arg.volume
        self.fs = 48000
        self.midi_interface = MidiInterface(self.process_midi, arg)
        self.sound_module = SoundModule(arg)
        self.effect = effect
        self.stream = sd.OutputStream(blocksize=arg.chunk, dtype=np.float32)
        self.notes = [Note(i, arg) for i in range(0, 128)]

    def run(self):
        self.stream.start()  # start sounddevice stream
        try:
            while True:
                # write to stream
                self.stream.write(self.poly())

        except KeyboardInterrupt:
            self.stream.stop()
            self.stream.close()

    def poly(self):
        poly = np.zeros(self.arg.chunk).astype(np.float32)
        active = sum(map(lambda x: x.state != False, self.notes))
        # print(active)

        for note in self.notes:
            poly += self.sound_module.play(note)
        if active:
            for sample in poly:
                sample /= active
        return poly

    def process_midi(self, message):
        msg = message
        if msg.is_cc():
            if msg.control == 64:
                if msg.value == 127:
                    self.sound_module.hold = True
                    for note in self.notes:
                        if note.state:
                            note.holdstate = True
                elif msg.value == 0:
                    self.sound_module.hold = False
                    for note in self.notes:
                        if not note.state:
                            note.holdstate = False
        else:
            if msg.type == "note_on":
                self.notes[msg.note].state = True
            elif msg.type == "note_off":
                self.notes[msg.note].state = False

class MidiInterface:
    
    def __init__(self, callback, arg) -> None:
        self.ports = mido.get_output_names()
        self.inport = mido.open_input(
            self.ports[arg.port], callback=callback)


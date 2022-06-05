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
        self.midi_interface = MidiInterface(self.process_midi)
        self.sound_module = SoundModule(arg)
        self.effect = effect
        self.note = None
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
        print(active)

        for note in self.notes:
            poly += self.sound_module.play(note)
        if active:
            for sample in poly:
                sample /= active
        return poly

    def process_midi(self, message):
        msg = message
        if msg.type == "note_on":
            self.notes[msg.note].state = True
        elif msg.type == "note_off":
            self.notes[msg.note].state = False


# moved midi_interface.py stuff here to consolidate
# - we can add functionality as needed
class MidiInterface:
    def __init__(self, callback) -> None:

        # comment this out to change back to default
        self.inport = mido.open_input(
            'Rev2:Rev2 MIDI 1 36:0', callback=callback)

        # uncomment this to change back to default
        # self.inport = mido.open_input(callback=callback)


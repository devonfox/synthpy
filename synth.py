# from xml.sax import parseString
from effects import Toaster
from sound_module import SoundModule
from adsr import ADSR
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
        self.adsr = ADSR()
        self.note = None
        self.stream = sd.OutputStream(blocksize=arg.chunk, dtype=np.int16)

    def play(self):
        self.stream.start() # start sounddevice stream
        try:
            while True:
                # write to stream
                self.stream.write(self.outstream_data())

        except KeyboardInterrupt:
            self.stream.stop()
            self.stream.close()

    def process_midi(self, message):
        msg = message
        if msg.type == "note_on":
            # print(f"start")
            self.note = msg.note
        elif msg.type == "note_off":
            if msg.note == self.note:
                self.note = None
                # print(f"stop")

    def outstream_data(self):
        data = self.sound_module.play(self.note)
        # data = self.adsr.apply_envelope(data, self.note)
        # data = self.effect.apply_effect(data) if self.effect else data
        return data

# moved midi_interface.py stuff here to consolidate
# - we can add functionality as needed
class MidiInterface:
    def __init__(self, callback) -> None:

        # comment this out to change back to default
        # self.inport = mido.open_input(
        #     'Rev2:Rev2 MIDI 1 36:0', callback=callback)

        # uncomment this to change back to default
        self.inport = mido.open_input(callback=callback)

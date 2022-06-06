from effects import Effect
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
        self.effect = Effect(arg)
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

    # function sums all notes currently still sending samples
    def poly(self):
        poly = np.zeros(self.arg.chunk).astype(np.float32)
        active = sum(map(lambda x: x.state != False, self.notes))
        # print(active)

        for note in self.notes:
            poly += self.effect.apply_effect(self.sound_module.play(note))
        if active:
            for sample in poly:
                sample /= active
        return poly

    # mido callback function sends control changes from sustain
    # to change state of notes
    # also takes in new notes and updates state of note key on and off changes
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
                if self.sound_module.hold:
                    self.notes[msg.note].holdstate = True
            elif msg.type == "note_off":
                self.notes[msg.note].state = False

# Class that creates midi interface connection
# also at command line can decide to list ports, 
# or there is an option to simply connect to the port
# if you already know it 
class MidiInterface:

    def __init__(self, callback, arg) -> None:
        self.ports = mido.get_output_names()
        self.portlist = arg.portlist

        if self.portlist:
            print("MIDI Port Listing")
            for (i, port) in enumerate(self.ports):
                print(f"{i}: {port}")
            print()
            print("Please enter port number: ")
            port = input("Please enter a port number: ")
            port = int(port)
            if port < 0 or port > len(self.ports) - 1:
                print("Error: No port exists")
                exit()
            self.inport = mido.open_input(
                self.ports[port], callback=callback)
        else:
            # for windows, since port recognition is wonky
            if arg.port == 99:
                self.inport = mido.open_input(callback=callback)
            else:
                self.inport = mido.open_input(
                self.ports[arg.port], callback=callback)

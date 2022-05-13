from midi_interface import MidiInterface


class Synth:
    def __init__(self) -> None:
        self.midi_interface = MidiInterface()

    def activate(self):
        while True:
            msg = self.midi_interface.input.recieve()
            print(msg)

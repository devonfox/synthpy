import mido

# import rtmidi


class MidiInterface:
    def __init__(self, callback) -> None:

        self.inport = mido.open_input('Rev2:Rev2 MIDI 1 36:0', callback=callback)
        # self.inport = mido.open_input(callback=callback)


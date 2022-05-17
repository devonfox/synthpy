import mido

# import rtmidi


class MidiInterface:
    def __init__(self, callback) -> None:
        self.inport = mido.open_input(callback=callback)

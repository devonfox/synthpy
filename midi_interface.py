import mido
import rtmidi

"""
classes:
    midi interface

    sound generator


"""


class MidiInterface:
    def __init__(self) -> None:
        self.notes = []
        self.input = mido.open_input()
        pass

    # def activate_interface(self):
    #     print("yo")
    #     with mido.open_input() as midi_in:
    #         while True:
    #             for msg in midi_in:
    #                 self.notes.insert(msg)
    #                 # print(msg)

from midi_interface import MidiInterface
from test_module import TestModule
from effects import Toaster
import pyaudio


class Synth:
    """
    Manages all components that comprise a synth, including the audio stream, a sound generator,
    a midi interface, and an optional effect.
    """

    def __init__(self, sound_moudle=TestModule(), effect=None) -> None:

        self.p = pyaudio.PyAudio()
        self.volume = 0.5  # range [0.0, 1.0]
        self.fs = 48000  # sampling rate, Hz, must be integer
        self.midi_interface = MidiInterface(self.process_midi)
        self.sound_module = sound_moudle
        self.effect = effect
        self.note = None
        self.stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.fs,
            output=True,
        )

    def play(self):
        """
        Begins the audio stream, and continuously writes wave data to the output stream based
        on midi input.
        """
        self.stream.start_stream()
        while True:
            if self.note:
                self.stream.write(self.output_data())

    def output_data(self):
        """
        Applies volume and effects to final wave data
        """
        data = self.volume * self.sound_module.play(self.note)
        if self.effect:
            data = self.effect.apply_effect(data)
        return data

    def process_midi(self, message):
        """
        Runs on another thread as a callback from the midi interface. Runs every time
        a midi signal is recieved. Currently only handles "midi on" and "midi off".
        If midi on, the note value is saved to the synth's note member.
        """
        msg = message
        if msg.type == "note_on":
            # self.stream.start_stream()
            self.note = msg.note
        elif msg.type == "note_off":
            if msg.note == self.note:
                # self.stream.stop_stream()
                self.note = None
                print(f"stop")

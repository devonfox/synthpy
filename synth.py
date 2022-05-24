from xml.sax import parseString
from midi_interface import MidiInterface
from sine_module import SineModule
from effects import Toaster
import pyaudio
import numpy as np
import time
import queue

chunk = 128 # trying to decide on a chunk for audio callback

class Synth:
    def __init__(self, sound_module=SineModule(), effect=None) -> None:
        self.p = pyaudio.PyAudio()
        self.volume = 0.5  # range [0.0, 1.0]
        self.fs = 48000  # sampling rate, Hz, must be integer
        self.midi_interface = MidiInterface(self.process_midi)
        self.sound_module = sound_module
        self.effect = effect
        self.note = None
        self.stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.fs,
            output=True,
            frames_per_buffer=chunk, # 256
            stream_callback=self.pa_callback
        )

    def play(self):
        self.stream.start_stream()
        # print(self.midi_interface.inport)
        while True:
            if self.note:
                self.sound_module.play(self.note, chunk)
            
                # self.stream.write(self.output_data())
                # time.sleep(0.0001)
            # for msg in self.midi_interface.inport.iter_pending():
            # else:
                # self.stream.write(self.output_silence())
            

    def process_midi(self, message):
        msg = message
        # print(message)
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
    
    def output_silence(self):
        pass

    def pa_callback(self, out_data, frame_count, time_info, status):
        # print('ok')
        print(frame_count)
        # here take chunks of audio and play in chunks
        data = np.zeros((256, 1))
        return (data, pyaudio.paContinue)

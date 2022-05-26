from xml.sax import parseString
from midi_interface import MidiInterface
from effects import Toaster
import pyaudio
import sounddevice as sd
import numpy as np
import queue
import sys

chunkdata = queue.Queue(maxsize=1)
chunk = 512  # trying to decide on a chunk for audio callback

start_idx = 0
class SineModule:

    def play(self, note, s):
        if note:
            # print(f"play {note}: {s}")
            pass
        else:
            # print(f"none: {s}")
            pass
            s += chunk
            zeros = np.zeros(chunk)
            # print(zeros)
            # chunkdata.put(zeros)
            return 0
        # fs = 48000       # sampling rate, Hz, must be integer
        f = 440 * 2**((note - 69) / 12)
        # period = 2 * np.pi * f / fs

        # do not need a duration, we want to keep creating this as long as the note is held, and
        # then return the full samples, and stream it chunk by chunk to the audio callback, with
        # minimal delay

        # possibly change
        t = np.linspace(s, s + chunk, False).astype(np.float32)
        wave = np.sin(f * t * 2 * np.pi)
        # chunkdata.put(wave)
        # print(chunkdata)

        s += chunk
        return s

    def stop(self, note):
        print(f"stop {note}")


class Synth:
    def __init__(self, sound_module=SineModule(), effect=None) -> None:
        # self.p = pyaudio.PyAudio()
        self.volume = 0.5  # range [0.0, 1.0]
        self.fs = 48000  # sampling rate, Hz, must be integer
        self.midi_interface = MidiInterface(self.process_midi)
        self.sound_module = sound_module
        self.effect = effect
        self.note = None
        # self.index = 0
        self.stream = sd.OutputStream(
            samplerate=self.fs, channels=1, blocksize=1024, callback=sd_callback)

        # self.stream = self.p.open(
        #     format=pyaudio.paFloat32,
        #     channels=1,
        #     rate=self.fs,
        #     output=True,
        #     frames_per_buffer=chunk, # 512
        #     stream_callback=self.pa_callback

    def play(self):
        self.stream.start()
        try:
            # print(self.midi_interface.inport)
            num = 0
            while True:
                pass
                # num = self.sound_module.play(self.note, num)
                # print(chunkdata)
        except KeyboardInterrupt:
            exit()

    def process_midi(self, message):
        msg = message
        # print(message)
        if msg.type == "note_on":
            # self.stream.start_stream()
            print(f"start")
            self.note = msg.note
        elif msg.type == "note_off":
            if msg.note == self.note:
                # self.stream.stop_stream()
                self.note = None
                print(f"stop")

    # def output_data(self):
    #     data = self.volume * self.sound_module.play(self.note)
    #     if self.effect:
    #         data = self.effect.apply_effect(data)
    #     return data

def sd_callback(outdata, frame_count, time, status):
  
    global start_idx
    t = (start_idx + np.arange(frame_count)) / 48000
    t = t.reshape(-1, 1)
    # print(len(zeros))
    outdata[:] = 0.2 * np.sin(2 * np.pi * 440.0 * t)
    print(start_idx)
    start_idx += frame_count

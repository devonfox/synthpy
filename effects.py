import numpy as np
# from scipy.io import wavfile
# import scipy.io
# import wave
import pyaudio

class Effect:
    pass

class Toaster(Effect):

    def apply_effect(self, audio_data):
        amplitude = np.iinfo(np.int16).max
        maxamp = amplitude
        clipped_data = (amplitude*6/7) * audio_data

        for index, frame in enumerate(clipped_data):
            if frame > maxamp:
                clipped_data[index] = maxamp
            elif frame < -maxamp:
                clipped_data[index] = -maxamp
            
        return clipped_data

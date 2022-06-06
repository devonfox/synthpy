import numpy as np

class Effect:
    def __init__(self, args) -> None:
        self.args = args

    def apply_effect(self, audio_data):
        effects = {
            "toaster": self.toaster,
        }
        
        if self.args.effect: 
            return effects[self.args.effect](audio_data)
        return audio_data

    def toaster(self, audio_data):
        filter = np.zeros(len(audio_data))
        filter[0] = 1
        filter[len(audio_data)-1] = 0.7
        out = np.convolve(audio_data, filter, "same")
        return out

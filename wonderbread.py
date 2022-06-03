
from synth import Synth
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--volume', dest='volume', type=float, default=8.0,
                    help='note volume for the chosen synth module (default: 8.0)')
parser.add_argument('--buffer', dest='chunk', type=int, default=512,
                    help='buffer size for continuous audio playback (default: 512)')
parser.add_argument('--attack', dest='attack', type=float, default=0.05,
                    help='seconds of attack time (default: 0.05)')
parser.add_argument('--wave', dest='wave', type=str, default='square',
                    help='synth waveform module (default: square)')


arg = parser.parse_args()

if arg.wave == 'square':
    wavetype = 1
elif arg.wave == 'sine':
    wavetype = 2
else:
    print('Incorrect waveform type entered. see argument (--wave)')
    exit()

def main():
    synth = Synth(arg, wavetype)
    synth.play()


if __name__ == "__main__":
    main()


from synth import Synth
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--volume', dest='volume', type=float, default=8.0,
                    help='note volume for the chosen synth module (default: 8.0)')
parser.add_argument('--buffer', dest='chunk', type=int, default=512,
                    help='buffer size for continuous audio playback (default: 512)')
parser.add_argument('--attack', dest='attack', type=float, default=0.05,
                    help='seconds of attack time (default: 0.05)')
parser.add_argument('--release', dest='release', type=float, default=0.2,
                    help='seconds of release time (default: 0.2)')
parser.add_argument('--wave', dest='wave', type=str, default='square',
                    help='synth waveform module (default: square)')


arg = parser.parse_args()

modules = ['square', 'sine', 'tri']

if arg.wave not in modules:
    print('Incorrect waveform type entered. see argument (--wave)')
    exit()

def main():
    synth = Synth(arg)
    synth.play()


if __name__ == "__main__":
    main()

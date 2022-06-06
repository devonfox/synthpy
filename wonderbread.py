
from synth import Synth
import argparse
import mido

parser = argparse.ArgumentParser()

parser.add_argument('--volume', dest='volume', type=float, default=7.0,
                    help='note volume for the chosen synth module (default: 7.0)')
parser.add_argument('--buffer', dest='chunk', type=int, default=256,
                    help='sample buffer size (default: 256)')
parser.add_argument('--attack', dest='attack', type=float, default=0.05,
                    help='seconds of attack time (default: 0.05)')
parser.add_argument('--release', dest='release', type=float, default=0.25,
                    help='seconds of release time (default: 0.25)')
parser.add_argument('--decay', dest='decay', type=float, default=0.05,
                    help='seconds of attack time (default: 0.05)')
parser.add_argument('--sustain', dest='sustain', type=float, default=1.0,
                    help='sustain level with note hold (default: 1.0)')
parser.add_argument('--wave', dest='wave', type=str, default='square',
                    help='synth waveform module (default: square)')
parser.add_argument('--port', dest='port', type=int, default=0,
                    help='select midi port (default: 0)')
# parser.add_argument('--voice', dest='voice', type=int, default=8,
#                     help='voice count (default: 8)')


arg = parser.parse_args()

modules = ['square', 'sine']

if arg.wave not in modules:
    print('Incorrect waveform type entered. see argument (--wave)')
    exit()

def main():
    synth = Synth(arg)
    synth.run()

if __name__ == "__main__":
    main()

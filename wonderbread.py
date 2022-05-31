from synth import Synth
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--volume', dest='volume', type=float, default=8.0,
                    help='note volume for the chosen synth module (default: 8.0)')
parser.add_argument('--buffer', dest='chunk', type=int, default=512,
                    help='buffer size for continuous audio playback (default: 512)')

arg = parser.parse_args()


def main():
    synth = Synth(arg)
    synth.play()


if __name__ == "__main__":
    main()

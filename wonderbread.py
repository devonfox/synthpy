from synth import Synth
import argparse


# possibly use sounddevice?


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("mode", type=str, required=False)
    # args = parser.parse_args()
    synth = Synth()
    synth.activate()
    while True:
        print(synth.midi_interface.notes)
    return


if __name__ == "__main__":
    main()

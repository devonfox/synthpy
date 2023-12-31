## Synthpy

A simple CLI square synth with midi connectivity written in Python using sounddevice and mido.

*Devon Fox and Matt Stevenson 2022*

### Mac/Linux/Windows Build Instructions

Make sure the latest version of Python is installed.

1. First upgrade pip and setuptools:

`pip install --upgrade pip setuptools`

2. Then make sure the ALSA development dependencies are installed:

*MAC/WINDOWS USERS: can skip this step*

`sudo apt-get install -y python3-dev libasound2-dev`

3. Install Numpy (math library)

`pip install numpy`

4. Install Sounddevice (audio Library)

`pip install sounddevice`

5. Install Mido midi library

`pip install mido`

6. Install Python-rtmidi for use of midi ports

`pip install python-rtmidi`


### Windows Build Instructions

In addition to the above, windows users will need a midi loopback tool in order to connect a midi keyboard to the synth. The one provided below works well and is free:

loopMidi: https://www.tobias-erichsen.de/software/loopmidi.html

Also, you need to specify the --port arg to be 99 when using loopMidi on windows.


To run the program, in the same directory, type the following in the terminal:

`python3 synthpy.py`

You can customize many aspects of the resulting audio (or dare I say music) with the following commands:

*Without entering arguments, the defaults will be used. Give command `--h` to access help menu*

Ex. `--wave square` 
* allows us to choose the waveform of the synthesizer (Default: square)

Ex. `--buffer 256`
* set the sample buffer size *Warning: raising can increase latency* (Default: 256)

Ex. `--attack 0.05`
* set the amp envelope attack time (in seconds)' (Default: 0.05)

Ex. `--decay 0.05`
* set the amp envelope decay time (in seconds)' (Default: 0.05)

Ex. `--sustain 0.5`
* set the amp envelope sustain level (between 0 and 1) (Default: 1.0)

Ex. `--release 0.25`
* set the amp envelope decay time (in seconds) (Default: 0.25)

Ex. `--port 0`
* select which midi port to receive from (Default: 0)

Ex. `--portlist False`
* list all available midi ports, and select which one to connect to at startup - `--port` can be used instead if you already know portnumber or want to startup headlessly (Default: False)

Ex. `--effect toaster`
* enable the toaster effect

*to note: sustain will be held if using a sustain pedal via midi*


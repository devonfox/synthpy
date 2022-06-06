## CS410P Final Project

CS410P - Music, Sound, and Computers

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


### Winodws Build Instructions

In addition to the above, windows users will need a midi loopback tool in order to connect a midi keyboard to the synth. The one provided below works well and is free:

loopMidi: https://www.tobias-erichsen.de/software/loopmidi.html


To run the program, in the same directory, type the following in the terminal:

`python3 wonderbread.py`

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
* list all available midi ports, and select which one to connect to at startup - port can be used instead if you already know portnumber or want to startup headlessly (Default: False)

Ex. `--effect toaster`
* enable the toaster effect

*to note: sustain will be held if using a sustain pedal via midi*

### What Went Down

*todo!*

###  How It Went

Implementing a midi interface was straightforward, as the mido library made it very easy to recieve and parse midi data. Once the midi interface was implemented, it wasn't long before we were able to have a playable monosynth. Of course, there was still a lot left to do.

Work on effects modules wound up being a bit too much to handle. Unsurprisingly, interesting audio effects are hard to develop. Ultimately, we were only able to implement one effect, the "Toaster"; this was born of a failed attempt at an echo effect. The result is a blown out sound that sounds like you left your wonderbread in the oven for a bit too long. 

The effects module was designed to be easily extensible, though, so perhaps in the future we will be able to continue development and get some common effects like reverb or delay implemented.
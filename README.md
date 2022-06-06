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

The initial plan was to implement a monosynth with ADSR, multiple wave types, and some audio effects. With time permitting, we would implement polyphony, and any other interesting features we felt we could manage. We chose to use python due to the audio libraries available for it, and because we felt it would be the easiest for the two of us to work with.

With that in mind, we set up our project in a modular fashion: the initial design utilized a synth class which would manage the various components of our synth, including a sound module class, an effects module class, and an envelope generator class. Additionally, the synth class handles the audio stream. We aimed for modularity to make adding and removing different components easy while we were developing the synth, and to ensure we could easily extend our synth in the future.

As development progressed, we were able to implement polyphony, and even enabled support for sustain pedals. This required some changes to our initial design, however. A Note class was added to allow for tracking the state of notes; this helped with the implementation of release as well.

The end result is Wonderbread, a polyphonic synth with ADSR (and sustain pedal support), two wave types (sine and square), and a distortion effect called "Toaster".

###  How It Went

Implementing a midi interface was straightforward at first, as the mido library made it very easy to receive and parse midi data. Once the midi interface was implemented, it wasn't long before we were able to have a simple, playable monosynth. Of course, there was still a lot left to do.

One of the first hurdles was changing how we implemented our midi interface. The initial implementation used a callback and only wrote midi data to stream when a note was played; we soon discovered the flaws of this approach, and as a result we had to change our design so that data was constantly being written to the stream. To fix our issue, when no notes are being played, we simply write empty data out.

We also encountered a good deal of friction working with the pyaudio library, so much so that we eventually ditched it in favor of the sounddevice library. Once this was implemented, we had no issues with writing to stream on any of the three platforms we were developing for.

Work on effects modules wound up being a bit too much to handle. Unsurprisingly, interesting audio effects are hard to develop. Ultimately, we were only able to implement one effect, the "Toaster"; this was born of a failed attempt at an echo effect. The result is a blown out sound that sounds like you left your wonderbread in the oven for a bit too long. 

The effects module was designed to be easily extensible, though, so perhaps in the future we will be able to continue development and get some common effects like reverb or delay implemented.
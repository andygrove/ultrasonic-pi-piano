# Building an Ultrasonic Pi Piano

## Parts

In addition to a Raspberry Pi (model 3B or above recommended), you will need the following electronic components:

- 1 x [Octasonic Breakout for Raspberry Pi](https://www.tindie.com/products/andygrove73/octasonic-8-x-hc-sr04-breakout-for-raspberry-pi/)
- 8 x HC-SR04 Ultrasonic Sensors
- 8 x [2.54mm 0.1" Pitch 4-pin Jumper Cable - 20cm long](https://www.adafruit.com/product/4936)
- 7 Jumper Wires (female-female). I buy [these 20-pin wires](https://www.adafruit.com/product/1949) and split them but you can also use individual wires. 

## Assembly

First, use the 4-pin jumper cables to connect the ultrasonic sensors to the Octasonic board, being careful to check 
that the pin-out on the sensors matches the pin-out on the board.

Next, make sure the Raspberry Pi is powered off, and connect the Octasonic board to the Raspberry Pi, using the following
table and diagram as a reference.

*Please be careful not to confuse GPIO pin numbers with the physical pin numbers in the diagram. This is a common 
mistake! For example, GPIO pin 9 is physical pin 21 in the diagram.*

| Octasonic | Raspberry Pi  |
|-----------|---------------|
| 5V        | 5V            | 
| 3.3V      | 3.3V          |
| GND       | GND           |
| MISO | MISO (GPIO 9) |     
| MOSI      | MOSI (GPIO 10) |
| SCK | SCLK (GPIO 11) |
| SS | CE0 (GPIO 8)  |

![Raspberry Pi GPIO Pinout Diagram](GPIO-Pinout-Diagram-2.png)

## Installing Software on the Raspberry Pi

Power up the Raspberry Pi and follow these instructions to install the software.

First, we need to enable SPI on the Raspberry Pi. SPI is the method used to communicate between the Raspberry Pi 
and the Octasonic board.

You may need to Google how to do this depending on the operating system version you are running, but for recent 
versions, you can find the "Raspberry Pi Configuration" application under the "Preferences" menu. Under the "Interfaces"
tab there is a toggle switch to enable SPI. You will need to reboot after enabling this.

Next, we will install the [Octasonic Python Library](https://pypi.org/project/octasonic/) from PyPi:

```shell
pip install octasonic
```

We can now download the Python code for running the piano software. This will detect movement over the keys and translate
them into MIDI instructions, which will be written to the standard output stream.

```shell
git clone https://github.com/makersgrove/ultrasonic-pi-piano.git
cd ultrasonic-pi-piano/python
python piano.py
```

You should see output similar to the following:

```
Protocol v2; Firmware v1.1
Sensor count: 8
```

This demonstrates that communication between the Raspberry Pi and the Octasonic is working correctly. If you see 
zeroes instead of these values then it probably means that either SPI is not enabled, or there is a wiring mistake.

The output will then show some seemingly random instructions in a loop. You should see these numbers change as you move 
your hands over the sensors. If not, then it could indicate an error with the wiring between the sensors and the 
Octasonic board.

```
noteon 8 96 127
noteon 4 52 127
noteoff 8 96
...
```

You are seeing the MIDI instructions, but you will hear any sound yet. We now need to send these 
notes to a synthesizer.

# Install FluidSynth

Fluidsynth is an amazing free software MIDI synth. You can install it from the command-line with this command:

```shell
sudo apt-get install fluidsynth
```

Now we can run the piano.py Python script again, and pipe the output to fluidsynth. Note that Python usually buffers 
output, so we need to be sure to specify the `-u` flag to override this.

```shell
python -u piano.py | fluidsynth -a alsa -g 1.0 -l /usr/share/sounds/sf2/FluidR3_GM.sf2
```




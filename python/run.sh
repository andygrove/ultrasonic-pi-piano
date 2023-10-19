#!/bin/bash

# kill any pianos that are already running (perhaps from bootup)
#echo "Killing any already running pianos ..."
#sudo killall -9 ultrasonic_piano 2>/dev/null

# now run the piano, piping the output into fluidsynth
echo "Launching piano ..."
python -u piano.py | fluidsynth -a alsa -g 1.0 -l /usr/share/sounds/sf2/FluidR3_GM.sf2

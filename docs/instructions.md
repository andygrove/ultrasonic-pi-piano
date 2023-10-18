# Building an Ultrasonic Pi Piano

NOTE: This is a draft document. For the most up-to-date docs, please refer to the [Instructable](https://www.instructables.com/Ultrasonic-Pi-Piano-With-Gesture-Controls/).

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

We can now download a Python example that will check that the board and sensors are working correctly.

```shell
wget https://github.com/makersgrove/octasonic-python/blob/main/examples/demo.py
python demo.py
```

You should see output similar to the following:

```
Protocol v2; Firmware v1.1
Sensor count: 8
```

This demonstrates that communication between the Raspberry Pi and the Octasonic is working correctly. If you see 
zeroes instead of these values then it probably means that either SPI is not enabled, or there is a wiring mistake.

The output will then show some seemingly random numbers in a loop:

```
[ 8, 0, 0, 0, 0, 0, 0, 22 ]
[ 8, 0, 0, 0, 22, 34, 0, 22 ]
...
```

You should see these numbers change as you move your hands over the sensors. If not, then it could indicate an error 
with the wiring between the sensors and the Octasonic board.

# Running in headless mode

To have the code start up when you boot the Raspberry Pi (without needing keyboard, mouse, and monitor attached) add these lines to your `/etc/rc.local` file and reboot.

```
. /home/pi/.cargo/env
cd /home/pi/UltrasonicPiPiano
./run.sh > /var/log/ultrasonic-pi.log 2>&1

```

In my case, the full `/etc/rc.local` file looked like this after adding those lines:

```
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

. /home/pi/.cargo/env
cd /home/pi/UltrasonicPiPiano
./run.sh > /var/log/ultrasonic-pi.log 2>&1

exit 0
```

If the code doesn't start running on bootup, check the log at `/var/log/ultrasonic-pi.log` for error messages.

# Stopping the program from running

To stop the program from running in the background, run the following command:

```
sudo killall -9 ultrasonic_piano
```


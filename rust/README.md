# Ultrasonic Pi Piano - Rust Version

This folder contains the original Rust version of the Ultrasonic Pi Piano software. We now 
recommend using the Python version instead, but if you are comfortable with Rust, then who
are we to stop you!

To run this version, simply run the `run.sh` script.

# Running in headless mode (this is likely somewhat out-of-date!)

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


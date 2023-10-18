from octasonic import Octasonic

octasonic = Octasonic(0)
protocol_version = octasonic.get_protocol_version()
firmware_version = octasonic.get_firmware_version()
print("Protocol v%s; Firmware v%s" % (protocol_version, firmware_version))
octasonic.set_sensor_count(8)
print("Sensor count: %s" % octasonic.get_sensor_count())

# TODO
# octasonic.set_max_distance(2); // 2= 48 cm
# octasonic.set_interval(2); // no pause between taking sensor readings

# The MIDI note number for the currently playing note, or 0 for no note
key_note = [ 0, 0, 0, 0, 0, 0, 0, 0 ]

# Counter for how many cycles the note has been playing
key_counter = [ 0, 0, 0, 0, 0, 0, 0, 0 ]

# Scale to play for each octave
# The numbers are zero-based indexes into a 12-note octave
# C scale : 0, 2, 4, 5, 7, 9, 11 (C, D, E, F, G, A, B)
scale = [0, 2, 4, 5, 7, 9, 11 ]

# Set the lowest note on the keyboard
# C0 = 12, C1 = 24, C2 = 36, ...
start_note = 12
octave_offset = 12

# choose MIDI instrument to associate with each key
# see https://en.wikipedia.org/wiki/General_MIDI
# 1 = Piano, 14 = Xylophone, 18 = Percussive Organ, 41 = Violin
instruments = [ 1, 10, 18, 25, 41, 89, 49, 14 ]

# we use a fixed velocity of 127 (the max value)
velocity = 127

# determine the max distance to measure
cm_per_note = 5

# TODO enable gestures
# let mut gesture_change_instrument = 129_u8; // two outermost sensors
# let mut gesture_shutdown = 24_u8; // middle two sensors

max_distance = len(scale) * cm_per_note

# now start taking measurements from the sensors in a loop
counter = 0
while True:

    # toggle the LED occasionally to show activity
    if counter == 100:
        octasonic.toggle_led()
        counter = 0

    # take readings from each sensor
    distance = []
    for i in range(0, 7):
        distance.append(octasonic.get_sensor_reading(i))

    # debug logging
    # print(distance)

    for i in range(8):
        channel = i + 1
        # is the key covered?
        if distance[i] < max_distance:
            # the key is covered, so figure out which note to play
            scale_start = start_note + octave_offset * i
            # this is a bit funky ... we use modulus to pick the note within the scale ... it
            # seemed to sound better than trying to divide the distance by the number of notes
            new_note = scale_start + scale[distance[i]%7]
            # is this a different note to the one already playing?
            if new_note != key_note[i]:
                # stop the previous note on this key (if any) from playing
                if key_note[i] > 0:
                    print("noteoff {} {}".format(channel, key_note[i]))
                # play the new note
                key_note[i] = new_note
                print("noteon {} {} {}".format(channel, key_note[i], velocity))
            elif key_note[i] > 0:
                # a note was playing but the key is not currently covered
                key_counter[i] = key_counter[i] + 1
                if key_counter[i] == 100:
                    # it's time to stop playing this note
                    print("noteoff {} {}".format(channel, key_note[i]))
                    key_note[i] = 0

    counter = counter + 1
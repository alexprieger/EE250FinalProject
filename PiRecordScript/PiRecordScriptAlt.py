import sys

sys.path.append('Python')

import grovepi
import time
import subprocess

if len(sys.argv) < 3:
    print("Records a wave file to the specified location on a button press.\n\nUsage: %s <filename>.wav <button_port>" % sys.argv[0])
    sys.exit(-1)

# Used for simple debouncing - if the button is held for two ticks, initiate recording
last_tick_pressed = False

filename = sys.argv[1]

button_port = int(sys.argv[2])

def record_audio():
    global last_tick_pressed
    p = subprocess.Popen("arecord -f cd %s.mp3" % filename, shell=True)
    this_tick_pressed = (grovepi.digitalRead(button_port) == 1)
    while(this_tick_pressed or last_tick_pressed):
        last_tick_pressed = this_tick_pressed
        this_tick_pressed = (grovepi.digitalRead(button_port) == 1)
        time.sleep(0.1)
    p.terminate()
    p.wait()

# main body of program
while True:
    if grovepi.digitalRead(button_port) == 1:
        if last_tick_pressed:
            print("Recording audio")
            record_audio()
        else:
            print("Debouncing")
            last_tick_pressed = True
    else:
        last_tick_pressed = False
    time.sleep(0.1)

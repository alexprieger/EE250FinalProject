import sys
import pyaudio
import grovepi
import time
import doorbellClient
import json
import gpiozero

CHUNK = 1024

if len(sys.argv) < 2:
    print("Records a wave file and sends it to the server on a button press.\n\nUsage: %s <button_port>" % sys.argv[0])
    sys.exit(-1)

# Used for simple debouncing - if the button is held for two ticks, initiate recording
last_tick_pressed = False

button_port = int(sys.argv[1])

# instantiate PyAudio
p = pyaudio.PyAudio()

def record_audio():
    global last_tick_pressed
    
    # open stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True)
    
    this_tick_pressed = grovepi.analogRead(button_port)
    data = []
    # read from stream
    while last_tick_pressed or this_tick_pressed:
        last_tick_pressed = this_tick_pressed
        this_tick_pressed = (grovepi.digitalRead(button_port) == 1)
        data.append(stream.read(CHUNK))

    # stop stream
    stream.stop_stream()
    stream.close()

    data = b''.join(data)
    return data

# main body of program
while True:
    if grovepi.digitalRead(button_port) == 1:
        if last_tick_pressed:
            print("Recording audio")
            data = record_audio()
            print("Finished recording audio")
            response = doorbellClient.sendRecordingToServer(data)
            responseDict = json.loads(str(response.text))
            if(responseDict['opens']):
                print('opening')
                gpiozero.LED(11).on()
                time.sleep(10)
                gpiozero.LED(11).off()
            else:
                print('access denied')
        else:
            last_tick_pressed = True
    else:
        last_tick_pressed = False
    time.sleep(0.1)

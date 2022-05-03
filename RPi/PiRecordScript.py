import sys
import pyaudio
import wave
import grovepi
import time
import subprocess

CHUNK = 1024

if len(sys.argv) < 3:
    print("Records a wave file to the specified location on a button press.\n\nUsage: %s <filename>.wav <button_port>" % sys.argv[0])
    sys.exit(-1)

# Used for simple debouncing - if the button is held for two ticks, initiate recording
last_tick_pressed = False

filename = sys.argv[1]
button_port = int(sys.argv[2])

# instantiate PyAudio
p = pyaudio.PyAudio()

def record_audio():
    global last_tick_pressed
    wf = wave.open(filename + ".wav", 'wb')
        
    # wav params
    nchannels = 1
    sampwidth = 2
    # 44100 is the industry standard sample rate - CD quality.
    sample_rate = 44100
    nframes = 0
    comptype = "NONE"
    compname = "not compressed"
    wf.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    # open stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True)
    
    this_tick_pressed = grovepi.analogRead(button_port)
    # read from stream
    while last_tick_pressed or this_tick_pressed:
        last_tick_pressed = this_tick_pressed
        this_tick_pressed = (grovepi.digitalRead(button_port) == 1)
        data = stream.read(CHUNK)
        wf.writeframes(data)

    # stop stream
    stream.stop_stream()
    stream.close()

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

import pyaudio
import wave
import sys

CHUNK = 1024

if len(sys.argv) < 2:
    print("Records a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'wb')
    
# wav params
nchannels = 1
sampwidth = 2
# 44100 is the industry standard sample rate - CD quality.
sample_rate = 44100
nframes = CHUNK * 10
comptype = "NONE"
compname = "not compressed"
wf.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                input=True)

# read from stream (3)
for i in range(10):
    data = stream.read(CHUNK)
    wf.writeframes(data)

# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()


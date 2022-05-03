from flask import Flask
from flask import request

import decode
import wave

app = Flask('RaspberryPi Doorbell Server')

@app.route('/doorbell', methods=['POST'])
def get_doorbell_callback():
    data = request.data
    waveToStore = wave.open('toneKey.wav', mode='wb')
    # Set parameters: Number of channels (1), sample width (2 bytes), sample rate (44.1 kHz), number of frames (0 to start), compression type (none), and compression name
    waveToStore.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))
    waveToStore.writeframes(data)
    
    response = {"opens" : decode.main('toneKey.wav')}

    return response

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)


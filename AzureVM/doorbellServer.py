from flask import Flask
from flask import request
from flask import send_file

import decode
import wave
import threading
import os

admitNextEntrant = False
admitLock = threading.Lock()
admitQueue = threading.Condition(admitLock)

app = Flask('RaspberryPi Doorbell Server')

@app.route('/doorbell', methods=['POST'])
def get_doorbell_callback():
    global admitNextEntrant
    global admitLock
    global admitQueue
    data = request.data
    waveToStore = wave.open('audioMessage.wav', mode='wb')
    # Set parameters: Number of channels (1), sample width (2 bytes), sample rate (44.1 kHz), number of frames (0 to start), compression type (none), and compression name
    waveToStore.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))
    waveToStore.writeframes(data)

    try:
        shouldOpen = decode.main('audioMessage.wav', '1234567890')
    except:
        print("Crashed in decode.py")
        shouldOpen = False

    admitLock.acquire()
    timeout = False
    # There shouldn't be any spurious wakeups, so technically this should be unnecessary
    while(not shouldOpen and not admitNextEntrant and not timeout):
        # wait returns false if the timeout expires without being woken
        timeout = not admitQueue.wait(60.0)
    shouldOpen = shouldOpen or admitNextEntrant
    admitNextEntrant = False
    admitLock.release()
    
    response = {"opens" : shouldOpen}
    try:
        os.remove('audioMessage.wav')
    except:
        print('File was already removed')

    return response

@app.route('/app', methods=['GET'])
def app_callback():
    try:
        return send_file("audioMessage.wav")
    except:
        return "nofile"

@app.route('/lock', methods=['GET'])
def lock_callback():
    global admitNextEntrant
    global admitLock
    global admitQueue
    admitLock.acquire()
    print("Locking")
    admitNextEntrant = False
    admitLock.release()
    return "Locked"

@app.route('/unlock', methods=['GET'])
def unlock_callback():
    global admitNextEntrant
    global admitLock
    global admitQueue
    admitLock.acquire()
    print("Unlocking")
    admitNextEntrant = True
    admitQueue.notify()
    admitLock.release()
    return "Unlocked"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)

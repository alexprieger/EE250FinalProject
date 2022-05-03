import requests
import json

# data should be the frames of data recorded in wav CD-style format
def sendRecordingToServer(data):
    
    headers = {
        'Authorization': None   # not using HTTP secure
    }

    response = requests.post("http://20.125.112.134/doorbell",
                             headers=headers,
                             data=data)

    return response

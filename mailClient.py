import requests
import json

def main():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': None   # not using HTTP secure
    }

    filecontents = 0
    # The payload of our message starts as a simple dictionary. Before sending
    # the HTTP message, we will format this into a JSON object
    payload = {
        'file': filecontents
    }

    # Send an HTTP POST message and block until a response is given.
    # Note: requests is NOT the same thing as the request from the Flask
    # library.
    response = requests.post("http://20.125.112.134/doorbell",
                             headers=headers,
                             data=json.dumps(payload))

    return 0

if __name__ == '__main__':
    main()

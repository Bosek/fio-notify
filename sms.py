from os import getenv

import requests

if (BULKGATE_ID := getenv("BULKGATE_ID")) is None:
    raise EnvironmentError("No BULKGATE_ID")
if (BULKGATE_TOKEN := getenv("BULKGATE_TOKEN")) is None:
    raise EnvironmentError("No BULKGATE_TOKEN")
if (BULKGATE_SENDER := getenv("BULKGATE_SENDER")) is None:
    raise EnvironmentError("No BULKGATE_SENDER")

def send(numbers, text):
    for number in numbers:
        print(f"Sending SMS to {number}")
        req = requests.post("https://portal.bulkgate.com/api/1.0/simple/transactional", json={
            "application_id": BULKGATE_ID,
            "application_token": BULKGATE_TOKEN,
            "number": number,
            "text": text,
            "sender_id": "gText",
            "sender_id_value": BULKGATE_SENDER,
            "unicode": True
        })
        print(f"Response: {req.status_code}")

def test():
    req = requests.get("https://portal.bulkgate.com/api/1.0/simple/info", params={
        "application_id": BULKGATE_ID,
        "application_token": BULKGATE_TOKEN
    })
    req_body = req.json()
    print(f"Credit: {req_body['data']['credit']} {req_body['data']['currency']}")
    return req.status_code == 200
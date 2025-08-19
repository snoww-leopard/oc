import hashlib
import requests
import json
from datetime import datetime, timezone

def order_placement(api_url, payload, secret_key, appkey, session_token):
    time_stamp = datetime.now(timezone.utc).isoformat()[:19] + '.000Z'
    checksum = hashlib.sha256((time_stamp+payload+secret_key).encode("utf-8")).hexdigest()
    print(checksum)
    headers = {
        'Content-Type': 'application/json',
        'X-Checksum': 'token '+ checksum,
        'X-Timestamp': time_stamp,
        'X-AppKey': appkey,
        'X-SessionToken': session_token
    }

    response = requests.request("POST", api_url, headers=headers, data=payload)
    print(response.text)

def get_list(api_url, exchange_code, secret_key, appkey, session_token):
    time_stamp = datetime.now(timezone.utc).isoformat()[:19] + '.000Z'
    payload = json.dumps({
        "exchange_code": "NSE",
        "from_date": "2025-02-28T10:00:00.000Z",
        "to_date": "2025-03-04T10:00:00.000Z"
        }, separators=(',', ':'))
    
    checksum = hashlib.sha256((time_stamp+payload+secret_key).encode("utf-8")).hexdigest()
    headers = {
        'Content-Type': 'application/json',
        'X-Checksum': 'token '+ checksum,
        'X-Timestamp': time_stamp,
        'X-AppKey': appkey,
        'X-SessionToken': session_token
    }

    response = requests.request("GET", api_url, headers=headers, data=payload)
    print(response.text)
    
import requests
import json
from datetime import datetime


def get_session_token(api_url, api_key, session_key):
    customerDetail_url = api_url
    customerDetail_payload = json.dumps({
        "SessionToken": session_key,
        "AppKey": api_key
        })
    
    customerDetail_headers = {
        'Content-Type': 'application/json',
        }
    customerDetail_response = requests.request("GET", customerDetail_url, headers=customerDetail_headers, data=customerDetail_payload)
    data = json.loads(customerDetail_response.text)
    session_token = data["Success"]["session_token"]
    print(f"session token: {session_token}")
    return session_token

def load_options_request_json():
    try:
        with open("./op-request.json") as file:
            return json.load(file)
    except FileNotFoundError:
            print("Error: The file 'symbol.txt' was not found.")

def log_oc_event(stock_code, strikediff, expiry_date, lot_size):
    now = datetime.now()

    folder_name = int(now.strftime("%Y%m%d"))
    print(folder_name)

    with open(f"./order_logs/{folder_name}.txt", "a") as file:
         file.write(f"{stock_code}\t{strikediff}\t{expiry_date}\t{lot_size}\n")

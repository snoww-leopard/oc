import requests
import json

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
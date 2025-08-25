import requests
import json
import hashlib
from datetime import datetime, timezone

def get_future_payoff(stock_code, expiry_date):
    customerDetail_url = "https://api.icicidirect.com/breezeapi/api/v1/customerdetails"
    session_key = 52724357
    secret_key = '0N3)929DW@2Q98I810949X436y3^UM6j'
    appkey = '5541c144r8VC59X9117ek4573=1312AM'
    time_stamp = datetime.now(timezone.utc).isoformat()[:19] + '.000Z'

    customerDetail_payload = json.dumps({
        "SessionToken": session_key,
        "AppKey": appkey
    })

    customerDetail_headers = {
        'Content-Type': 'application/json',
    }

    customerDetail_response = requests.request(
        "GET", customerDetail_url, headers=customerDetail_headers, data=customerDetail_payload)
    data = json.loads(customerDetail_response.text)
    session_token = data["Success"]["session_token"]

    url = "https://api.icicidirect.com/breezeapi/api/v1/quotes"

    payload = json.dumps({
        "stock_code": stock_code,
        "exchange_code": "NFO",
        "right": "others",
        "expiry_date": expiry_date,
        "product_type": "futures"
    }, separators=(',', ':'))

    checksum = hashlib.sha256((time_stamp + payload + secret_key).encode("utf-8")).hexdigest()

    headers = {
        'Content-Type': 'application/json',
        'X-Checksum': 'token ' + checksum,
        'X-Timestamp': time_stamp,
        'X-AppKey': appkey,
        'X-SessionToken': session_token
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print("Response Status Code get quote:", response.status_code, response.text  )
    response_json = response.json()

    option_chain = response_json.get("Success", [])
    #print("Option Chain:", option_chain)
    futurevalue = next((item.get("ltp") for item in option_chain), None)
    spot_price = option_chain[0].get("spot_price") if option_chain else None
    #print("Spot Price:", spot_price)
    #print("Future Value:", futurevalue)
    return {"spot_price": spot_price, "future_value": futurevalue}
#stock_code = "SRF"
#expiry_date = "2025-09-30T06:00:00.000Z"
#result = get_future_payoff(stock_code, expiry_date)
#print("In functionFuturePayoffresult:", result.get("spot_price"), result.get("future_value"))

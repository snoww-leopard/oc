import requests
import json
import hashlib
from datetime import datetime, timezone
from app_helper import get_session_token

def get_future_payoff(stock_code, expiry_date, appkey, secret_key, session_key):
    customerDetail_url = "https://api.icicidirect.com/breezeapi/api/v1/customerdetails"
    time_stamp = datetime.now(timezone.utc).isoformat()[:19] + '.000Z'

    session_token = get_session_token(customerDetail_url, appkey, session_key)

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
# stock_code = "SRF"
# expiry_date = "2025-09-30T06:00:00.000Z"
# result = get_future_payoff(stock_code, expiry_date)
# print("In functionFuturePayoffresult:", result.get("spot_price"), result.get("future_value"))

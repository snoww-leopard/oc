import requests
import pandas as pd
import json
import sys
from datetime import datetime, timezone
from order import order_placement, get_list
from sessiontoken import get_session_token

#symbol=["INFY", "ICICIBANK","HDFCBANK"]
customerDetail_url = "https://api.icicidirect.com/breezeapi/api/v1/customerdetails"
session_key=52615839
secret_key= sys.argv[2]
print(secret_key)
api_key= sys.argv[1]
time_stamp = datetime.now(timezone.utc).isoformat()[:19] + '.000Z'

session_token = get_session_token("https://api.icicidirect.com/breezeapi/api/v1/customerdetails", api_key, session_key)

#---------------------------------------Delete this 
payload = json.dumps({
  "stock_code": "NIFTY",
  "exchange_code": "NFO",
  "product": "options",
  "action": "buy",
  "order_type": "limit",
  "quantity": "1",
  "price": "1",
  "validity": "day",
  "stoploss": "",
  "validity_date": "2025-08-14T06:00:00.000Z",
  "disclosed_quantity": "0",
  "expiry_date": "2025-09-12T06:00:00.000Z",
  "right": "call",
  "strike_price": "2500",
  "user_remark": "testing" 
  }, separators=(',', ':'))

#order_placement("https://api.icicidirect.com/breezeapi/api/v1/order", payload, "`Z3n52161270k(0f513257F945yX257#", "58Y68D`8G5EZ89j17i4N48J3217h6m09", session_token)
get_list("https://api.icicidirect.com/breezeapi/api/v1/order", "NFO", secret_key, api_key, session_token)
#

try:
    with open("./symbol.txt") as file:
        symbol = list(file.read().split(","))
        print(symbol)
except FileNotFoundError:
    print("Error: The file 'symbol.txt' was not found.")

try:
    with open("./cookie.txt") as file:
        cookie = file.read()
except FileNotFoundError:
    print("Error: The file 'cookie.txt' was not found.")
#print(rawOp)

def curlapi(symbol):
    headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "content-type": "Content-Type: application/json; charset=UTF-8",
            "cookie": cookie
        }
    
    for i in range(0, len(symbol)):

        url = f"https://www.nseindia.com/api/option-chain-v3?type=Indices&symbol={symbol[i]}&expiry=28-Aug-2025"
        #print(url)
        session = requests.Session()
        request = session.get(url, headers=headers)
        cookies = dict(request.cookies)
        response = session.get(url, headers=headers, cookies=cookies).json()
        rawdata= pd.DataFrame(response).fillna(0)
        #rawOp = pd.DataFrame(rawdata["filtered"]["data"]).fillna(0)
        dataframe(rawdata)
    return
        
    

def dataframe(rawop):
    data = []
    underlying = rawop['records']['underlyingValue']
    option_data = rawop['records']['data']
    
    for entry in option_data:
        #print(entry)
        strike =  entry['strikePrice']
        ce_premium = entry['CE']['lastPrice']
        pe_premium = entry['PE']['lastPrice']
        ce_pe_diff = ce_premium - pe_premium
        strike_underlying_diff = underlying - strike
        diff_of_diffs = ce_pe_diff - strike_underlying_diff

        # Only consider if both premium difference and strike price difference are positive
        if ce_pe_diff > 0 and strike_underlying_diff > 0 and diff_of_diffs > 0:
            print("----------------------------------------------------------------------------")
            print(f"Strike Price: {strike}, CE-PE Premium Difference: {ce_pe_diff:.2f}, Strike-Underlying Difference: {strike_underlying_diff:.2f}, Diff of Diffs: {diff_of_diffs:.2f}")

    #for i in range(0, len(rawop)):
        # call = callchange = calllastprice =  put = putchange = putlastprice = 0
        # strikeprice = rawop["strikePrice"][i]

        # if (rawop["CE"][i] == 0):
        #     call = callchange = 0
        # else:
        #     call = rawop["CE"][i]["openInterest"]
        #     callchange = rawop["CE"][i]["changeinOpenInterest"]
        #     calllastprice = rawop["CE"][i]["lastPrice"]

        # if (rawop["PE"][i] == 0):
        #     put = putchange = 0
        # else:
        #     put = rawop["PE"][i]["openInterest"]
        #     putchangechange = rawop["PE"][i]["changeinOpenInterest"]
        #     putlastprice = rawop["PE"][i]["lastPrice"]

        # option_data = {
        #     "Call OI": call, "Call Change":callchange, "Call Last Price": calllastprice, "Strike Price": strikeprice,
        #     "Put OI": put, "Put Change": putchange, "Put Last Price": putlastprice
        # }

        #data.append(option_data)
    #optionchain = pd.DataFrame(data)
    #print(optionchain)
    return data


curlapi(symbol)
#processedoptionchain = dataframe(rawOp)
#print(processedoptionchain)
    
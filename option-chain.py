import requests
import pandas as pd

symbol=["INFY", "ICICIBANK","HDFCBANK"]

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

        url = f"https://www.nseindia.com/api/option-chain-v3?type=Indices&symbol={symbol[i]}&strike=1,400.00"
        print(url)
        session = requests.Session()
        request = session.get(url, headers=headers)
        cookies = dict(request.cookies)
        response = session.get(url, headers=headers, cookies=cookies).json()
        rawdata= pd.DataFrame(response)
        rawOp = pd.DataFrame(rawdata["filtered"]["data"]).fillna(0)
        dataframe(rawOp)
    return
        
    

def dataframe(rawop):
    data = []
    for i in range(0, len(rawop)):
        call = callchange = calllastprice =  put = putchange = putlastprice = 0
        strikeprice = rawop["strikePrice"][i]

        if (rawop["CE"][i] == 0):
            call = callchange = 0
        else:
            call = rawop["CE"][i]["openInterest"]
            callchange = rawop["CE"][i]["changeinOpenInterest"]
            calllastprice = rawop["CE"][i]["lastPrice"]

        if (rawop["PE"][i] == 0):
            put = putchange = 0
        else:
            put = rawop["PE"][i]["openInterest"]
            putchangechange = rawop["PE"][i]["changeinOpenInterest"]
            putlastprice = rawop["PE"][i]["lastPrice"]

        option_data = {
            "Call OI": call, "Call Change":callchange, "Call Last Price": calllastprice, "Strike Price": strikeprice,
            "Put OI": put, "Put Change": putchange, "Put Last Price": putlastprice
        }

        data.append(option_data)
    optionchain = pd.DataFrame(data)
    print(optionchain)
    return optionchain

curlapi(symbol)
#processedoptionchain = dataframe(rawOp)
#print(processedoptionchain)
    
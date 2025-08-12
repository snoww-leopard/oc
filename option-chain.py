import requests
import pandas as pd

symbol=["INFY", "ICICIBANK","HDFCBANK"]

#print(rawOp)

def curlapi(symbol):
    headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "content-type": "Content-Type: application/json; charset=UTF-8",
            "cookie": '_ga=GA1.1.469374668.1754816442; _abck=0ED01C228C0898855553584D03B375C7~0~YAAQv+lUuDIGp4qYAQAAXOJonw42j3+zZg6ij5j5RyWrqQV6qudLx6iWQf/p0WW5zJ4uf1EuQozhmhHHtd1VsMDX/PVrLh7ByEFKKOU6zqjQcLpUMt8SfTrr13m+nDZEzIjRW1glTI2OxQzv39ORxBCRgrbIByuf4ohaqW2SzyNXZoyjyDQlH6K+ghHWTyhd0xQ4xaBEwkGtUmf3W46grT+5lhBdaCCA57Cl8qFRkKncI+aTLU4WwQIaDJWZYlznJvycuDnPIHiLIODeK73q6RXgIfj+/Afy5DfDiJ1nkm1PkJkIAdgT1dZLJ08XLpW5PeFnIbjJ0g0nTnVEzmSHnb4HRI/J5PPyxN51hJdpIozIV+ipEBTnxe1oL3dKrYmZrK4/a3f9qZoc7+9CR4eF9JjFSB5zcgJypgb7VdDKmgQBUPlwBCf2mO1ThJda4Xq/DdC1MbisN5dHSNXsVtgmyyejvH73arbsMHtCOKGjqDuQXOsA98UBYwzXqhnLADuOUD/7GaQFY9ZhUzGrtrBI3MbxtjR2bXoH9LDSHRF6OGvkJNyNSULBG2XwiTABRoFjBnREGvMtogAyiJTubbgrgh7PhaZQ73ZYLbtcgS24R8rcewLkMXPx2crdaNSFqu9UpTr9~-1~-1~-1; nsit=4v8YEqLp-FxdyVkNQ5sG1Vho; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTc1NTAyMTEwOSwiZXhwIjoxNzU1MDI4MzA5fQ.W23fdUCQsxlvWynyK_7DtqyAzsnZpqFMvdPCvkUjSQE; AKA_A2=A; bm_mi=07DB114DE11A11C66BB8641AB5D8764E~YAAQv+lUuAoHp4qYAQAAQutonxx2Ihm6so65K3YZ7gY+yLMD+sMXCua/hbmCq2RpVU7uX/e/3dSkp+DvQSUYTXfQrG/DF915gNbab0Om8qIrZ4cBcBjPT/9oEm9bUSUJXW0S9Vu8zpiNLQPsvXH1RPAO87MlTHg90GwFHEE8ylhQ6mKlAvJRLbqnUY8++LH/o1sIKPhSOCF1gU2DUGfnJRNX+lzzGrnJpeZ2TYBkPNEDfV3B/5GXHDBOUkLhiLatIdWH9ZuaXopHMkkj10GIB5nxuQdXXweQ4JV4DGSsbvkbEhan9+3gwO6pycRwWl86YfWj9rurPK36oW2Q~1; bm_sz=05C0ACDBD0ED7046B994E10E3CCA3FE6~YAAQv+lUuAwHp4qYAQAAQutonxx0F7kep4CuOJUBPd3QxgdntzodjpsMl1FrnV9WeyknnhBsb5sVDPa548S3nePbg5v6Suj0LMwwUF14aVZ2GovQg+1WLLyx7RsvNcc6DIT8aIra54TijhxaO1RhCI4MoyK+A/mzN+fXSoX+QYY3bhqIdeyK8vqQtCW1/cw5hsuzfvdhDG9iSBNMDMGX0r1JafrZ0e1CnkREeppx+KlzUA2b04VF6gizfX/ihw2zaTINhT4LU8d/ZsJPIvjbndbiJl0ndEVUtNyo7tUzVoaQNew+MSUhVKwL/gSlsvNDch4Rdm6+W5qO08FSsPLvebBwFVqYIBrUaRgQc9xtSDfEWSlorA6BvBgbLuik4Sj5/1qU0hX9TBGLh5/U~3618865~4272451; ak_bmsc=4FDC2F559FFFCCDFA97509846F4E0F85~000000000000000000000000000000~YAAQv+lUuL8Hp4qYAQAARfRonxziN0V95Y4cYemanikSyTdSuthYziPrlDufShRwQdrmzS9GltrEOwq6B3hgMuaRO/0U8u9qMR0Ba0qu8WZumoGjg6US6n5rXLJZCP6dHgVvXjO5ojzTep/DqogEU3Xv5mD12dsmeKHqKUhxlhB7eCyKzJjGi2EJKXy9czNfAaJDEgKlzA17RGDMv38JCtrS2DV4+jkhzhT6fF1C2E6aGPeePVDe++QLO4dBqdj5tJikHKu/qJTIbTADxVLrar1LUlvmcX0E20Sd77FVCWVeOpgkgdDz4Aqe3micg/ehIJWw994qU13saumYOjapSiCVsKVGGpQzGyVFToK3UKV5p5qBsvV+nIK6JUiypn0PM9xfs/i8sIOmNnX8vApzIcjn+7QM62S33byvTQ/SeQ0Uw5rJ/cZaMByxoxmzx8RXoPKsb8w0hrXxxIKiM8JUoQjkDgdYshHsNsZj5T8/XJ9JQpXfO7e9qSSodExkyGzNaXE=; _ga_87M7PJ3R97=GS2.1.s1755021110$o6$g1$t1755021112$j58$l0$h0; RT="z=1&dm=nseindia.com&si=0dfdb704-31af-4a0c-87ed-4b9c34da7333&ss=me8u973f&sl=0&se=8c&tt=0&bcn=%2F%2F684d0d41.akstat.io%2F";'
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
    
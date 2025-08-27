import requests
import json
import hashlib
from datetime import datetime, timezone

def total_payoff(S_expiry, K1, K2, C1, P2, F):
    short_call_payoff = -(max(0, S_expiry - K1))
    long_put_payoff = max(0, K2 - S_expiry)
    long_future_payoff = S_expiry - F
    net_premium = C1 - P2
    return short_call_payoff + long_put_payoff + long_future_payoff + net_premium

def get_optionchain(url,appkey, session_token,payload,checksum):
	time_stamp = datetime.now(timezone.utc).isoformat()[:19] + '.000Z'
	headers = {
    		'Content-Type': 'application/json',
    		'X-Checksum': 'token '+ checksum,
    		'X-Timestamp': time_stamp,
    		'X-AppKey': appkey,
    		'X-SessionToken': session_token
	}

	response = requests.request("GET", url, headers=headers, data=payload)

	return response.json()

def get_future_payoff(quote_url, stock_code, expiry_date, secret_key, appkey, session_token):
	time_stamp = datetime.now(timezone.utc).isoformat()[:19] + '.000Z'
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
	response = requests.request("GET", quote_url, headers=headers, data=payload)

	response_json = response.json()
	print(f"$$$$$$$$$$$$$$$$${response_json}")
	option_chain = response_json.get("Success", [])
	
	futurevalue = next((item.get("ltp") for item in option_chain), 0)
	spot_price = option_chain[0].get("spot_price") if option_chain else 0
	return {"spot_price": spot_price, "future_value": futurevalue}

		

def process_option_data(option_chain, strikediff, lot_size, stock_code, expiry_date, appkey, secret_key, session_token, quote_url):
	result = []
	strikes = sorted([item.get("strike_price", 0) for item in option_chain])

	if len(strikes) >= 10:
		mid = len(strikes) // 2
		middle_strikes = strikes[mid-5:mid+5]
		print(f"Mid index: {mid}")
		print(f"Middle strikes: {middle_strikes}")
		filtered = [item for item in option_chain if item.get("strike_price", 0) in middle_strikes]
	else:
		filtered = option_chain
	#print (f"Filtered option chain: {filtered}")
	#filtered = option_chain
	#filtered = [item for item in option_chain if abs(item.get("strike_price", 0) - spot_price) <= 5000]

	for item in filtered:
		strike_price = item.get("strike_price")
		K1 = strike_price
		# Find ltp for call at K1
		C1 = next((i.get("ltp") for i in filtered if i.get("strike_price") == K1 and i.get("right") == "Call"), 0)
		P1 = next((i.get("ltp") for i in filtered if i.get("strike_price") == K1 and i.get("right") == "Put"), 0)
		# Find ltp for put at K2
		K2 = strike_price + strikediff  # or your logic for next strike
		P2 = next((i.get("ltp") for i in filtered if i.get("strike_price") == K2 and i.get("right") == "Put"), 0)

		F = get_future_payoff(quote_url, stock_code, expiry_date, secret_key, appkey, session_token).get("future_value")
		#K1, K1, K2, C1, P2, F)
		payoffU = total_payoff(K1, strike_price, K2, C1, P2, F)
		payoffL = total_payoff(K2, strike_price, K2, C1, P2, F)
		payoffARBITAGE = total_payoff(K1, K1, K1, C1, P1, F)
		if payoffL != 0:
			ratio = abs(payoffU / payoffL)
		else:
			ratio = float('inf')
		print(f"Strike Price: {strike_price}, K1: {K1} , K2: {K2}, C1: {C1}, P2: {P2}, F: {F}, payoffL:  {lot_size * payoffL:.2f} , payoffU: {lot_size * payoffU:.2f}, Ratio: {ratio:.2f}, Payoff Arbitrage: {lot_size * payoffARBITAGE:.2f}")
	
	# if C1 > 2 and P2 > 2:
		result.append({
				"strike_price": strike_price,
				"C1": C1,
				"K2": K2,
				"P2": P2,
				"payoff": payoffL,
				"payoffU": payoffU
			})
	return result




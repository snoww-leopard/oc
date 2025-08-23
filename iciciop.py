import json
import hashlib
import sys
from datetime import datetime, timezone
from app_helper import get_session_token, load_options_request_json
from breeze_helper import get_optionchain,process_option_data
#from lowRiskReward import total_payoff

op_request = load_options_request_json()

session_key = op_request['session_key']
secret_key= sys.argv[2]
print(secret_key)
appkey= sys.argv[1]
time_stamp = datetime.now(timezone.utc).isoformat()[:19] + '.000Z'

customerDetail_url = op_request['customerDetail_url']
session_token = get_session_token(customerDetail_url, appkey, session_key)


#print(f'{op_request['optionchain']['payload']}')
url = op_request['optionchain_method']['url']
#FutureUrl = "https://api.icicidirect.com/breezeapi/api/v1/quotes"

payload = json.dumps(op_request['optionchain_method']['payload'], separators=(',', ':'))
checksum = hashlib.sha256((time_stamp+payload+secret_key).encode("utf-8")).hexdigest()

result = []
response_json = get_optionchain(url, appkey, session_token, payload, checksum)

option_chain = response_json.get("Success", [])
strikediff = op_request['optionchain_method']['strikediff'] # diffrence between first and second strikes
lot_size = op_request['optionchain_method']['lot_size'] # lot size for ICICI Bank options


result = process_option_data(option_chain, strikediff, lot_size)

print(result)
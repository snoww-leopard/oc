import json
import hashlib
import sys
from datetime import datetime, timezone
from app_helper import get_session_token, load_options_request_json, log_oc_event
from breeze_helper import get_optionchain,process_option_data
#from lowRiskReward import total_payoff

op_request = load_options_request_json()

session_key = op_request['session_key']
secret_key= sys.argv[2]
print(secret_key)
appkey= sys.argv[1]

log_oc_event(1,1,1,1)


customerDetail_url = op_request['customerDetail_url']
session_token = get_session_token(customerDetail_url, appkey, session_key)
count = 0

for item in op_request['optionchain_method']:
    #print(f'{op_request['optionchain']['payload']}')
    count += 1
    print(f"============================================={count}")
    url = op_request["option_chain_url"]
    time_stamp = datetime.now(timezone.utc).isoformat()[:19] + '.000Z'
    #FutureUrl = "https://api.icicidirect.com/breezeapi/api/v1/quotes"

    payload = json.dumps(item['payload'], separators=(',', ':'))
    checksum = hashlib.sha256((time_stamp+payload+secret_key).encode("utf-8")).hexdigest()

    result = []
    response_json = get_optionchain(url, appkey, session_token, payload, checksum)

    option_chain = response_json.get("Success", [])

    strikediff = item['strikediff'] # diffrence between first and second strikes
    lot_size = item['lot_size'] # lot size for ICICI Bank options


    result = process_option_data(option_chain, strikediff, lot_size, item['payload']["stock_code"], item['payload']["expiry_date"], appkey, secret_key, session_token, op_request["quote_url"])

    #print(result)
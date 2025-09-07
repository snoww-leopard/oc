import base64
import socketio
import sys

from app_helper import get_session_token, load_options_request_json

# Please refer this link https://api.icicidirect.com/breezeapi/documents/index.html#candle-stream
# from understanding the script code.
# from venv run pip install pipreqs
op_request = load_options_request_json()

session_key = op_request['session_key']
secret_key= sys.argv[2]

appkey= sys.argv[1]

session_key = get_session_token(op_request['customerDetail_url'], appkey, session_key)

user_id, session_token = base64.b64decode(session_key.encode('ascii')).decode('ascii').split(":")

# Python Socket IO Client
sio = socketio.Client()
auth = {"user": user_id, "token": session_token}
sio.connect("https://breezeapi.icicidirect.com/", socketio_path='ohlcvstream', headers={"User-Agent":"python-socketio[client]/socket"}, 
                auth=auth, transports="websocket", wait_timeout=3)

if sio.connected:
    print("Connection established successfully!")
else:
    print("Failed to connect.")


# Script Code of Stock or Instrument  e.g 4.1!1594, 1.1!500209 , 13.1!5023, 6.1!247457. 
script_code = ["4.1!1594"] #Subscribe more than one stock at a time

#Channel name i.e 1SEC,1MIN,5MIN,30MIN
channel_name = "1SEC"

#CallBack functions to receive feeds
def on_ticks(ticks):
       print(f"test{ticks}")

#Connect to receive feeds
sio.emit('join', script_code)
sio.on(channel_name, on_ticks)

#Unwatch from the stock
sio.emit("leave", script_code)

#Disconnect from the server
sio.emit("disconnect", "transport close")




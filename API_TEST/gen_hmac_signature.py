import hmac
import time
import hashlib
import requests
from urllib.parse import urlencode

""" This is a very simple script working on Binance API

- work with USER_DATA endpoint with no third party dependency
- work with testnet

Provide the API key and secret, and it's ready to go

Because USER_DATA endpoints require signature:
- call `send_signed_request` for USER_DATA endpoints
- call `send_public_request` for public endpoints

```python

python spot.py

```

"""

KEY = "ZFGJl21ojPlcn1LpTavvH4ohHfUv03rwj8dm852bbN5ILGyq1dUwxxmCBEDQYYdQ"
SECRET = "MfcHL4SFkDVs9ouo9CEOm3yNYvxDv6SkYuHCicZVxrR4pjcUvRSbJo8GJoFFpv4f"

BASE_URL = 'https://testnet.binance.vision' # testnet base url

""" ======  begin of functions, you don't need to touch ====== """


def hashing(query_string):
    return hmac.new(
        SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()


def get_timestamp():
    return int(time.time() * 1000)


def dispatch_request(http_method):
    session = requests.Session()
    session.headers.update(
        {"Content-Type": "application/json;charset=utf-8", "X-MBX-APIKEY": KEY}
    )
    return {
        "GET": session.get,
        "DELETE": session.delete,
        "PUT": session.put,
        "POST": session.post,
    }.get(http_method, "GET")


# used for sending request requires the signature
def send_signed_request(http_method, url_path, payload={}):
    query_string = urlencode(payload, True)
    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp())
    else:
        query_string = "timestamp={}".format(get_timestamp())

    url = (
        BASE_URL + url_path + "?" + query_string + "&signature=" + hashing(query_string)
    )
    print("{} {}".format(http_method, url))
    params = {"url": url, "params": {}}

    response = dispatch_request(http_method)(**params)
    return response.json()


# used for sending public data request
def send_public_request(url_path, payload={}):
    query_string = urlencode(payload, True)
    url = BASE_URL + url_path
    if query_string:
        url = url + "?" + query_string
    print("{}".format(url))
    response = dispatch_request("GET")(url=url)
    return response.json()


""" ======  end of functions ====== """

### public data endpoint, call send_public_request #####
# get klines
#response = send_public_request(
    #"/api/v3/klines", {"symbol": "BTCUSDT", "interval": "1d"})
#print(response)


### USER_DATA endpoints, call send_signed_request #####
# get account informtion
# if you can see the account details, then the API key/secret is correct


payload = {
    "symbol": "BTCUSDT",
    "side": "BUY",
    "type": "MARKET",
    "quoteOrderQty": 1000, # spend 1000 USDT
}


payload = {
    "symbol": "BTCUSDT"
}

target_url = "/api/v3/order"
target_url = '/api/v3/allOrders'
response = send_signed_request("GET", target_url, payload)
print(response)

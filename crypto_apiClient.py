import hmac
import hashlib
import time
from time import sleep

from api_config import *

import websocket, json
from urllib.parse import urljoin

#client for Crpto.com exchange api
class CryptoAPIClient:
    __id = 0

    def __init__(self):
        try:
            self.ws = websocket.WebSocketApp(MARKETBASEURL,
                                             on_open=self.onOpen, on_close=self.onClose, on_message=self.onMsg)
            self.ws.run_forever()
        except BaseException as e:
            print(e)

    #when wesocket connection opens, send request with authentication info
    def onOpen(self, ws):
        auth_req = {
            "id": 1,
            "api_key": APIKEY
        }
        payload_str = f'{PUBAUTH}{self.getNewId()}{auth_req["api_key"]}{""}{self.getNonce()}'

        auth_req['sig'] = self.__sign(payload_str)
        ws.url = urljoin(ws.url, PUBAUTH)
        ws.send(json.dumps(auth_req))
        #sleep for 1 second as per crypto.com recommendation
        time.sleep(1)
        # FIXME: Check why authentication requests are not working
        print("Opened a webscoket connection")

    #when connection is closed
    #NOTE: for some reason this is not getting called!!
    def onClose(self, ws):
        print("Closed connection")

    #when message is received
    def onMsg(self, ws, msg):
        print("message received: " , msg)

    #id for new websocket request
    def getNewId(self):
        if self.__id <= 1000:
            return self.__id + 1
        else:
            return 1

    #get nonce
    def getNonce(self):
        return int(time.time() * 1000)

    #create a signature for the request
    def __sign(self, payload_str):
        return hmac.new(
            bytes(str(SECRETKEY), 'utf-8'),
            msg=bytes(payload_str, 'utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()


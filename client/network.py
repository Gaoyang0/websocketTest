# -*- coding:utf-8 -*-
# Author:DaoYang
import websocket
import threading

try:
    import thread
except ImportError:
    import _thread as thread
import time, json


class NetWork(threading.Thread):
    def __init__(self, url_host, room):
        threading.Thread.__init__(self)
        self.url = url_host + room
        self.ws = None
        self.room = room
        self.res = {}

    def run(self):
        print("Network " + self.room + " started!")
        self.ws = websocket.WebSocketApp(self.url, on_message=self.on_message, on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.run_forever()

    def connect(self):
        self.start()
        time.sleep(0.5)

    def on_message(self, message):
        data = json.loads(message)
        self.res = data
        print('Receive: ', data)
        if data['flag'] == 'getRes':
            self.send({
                "flag": "res",
                "message": data['message']+'jisuan'
            })


    def on_error(self, error):
        print('Error', error)

    def on_close(self, ):
        print("### closed ###")

    def on_open(self, ):
        print("### open ###")

    def send(self, dict, delay=0.1):
        self.ws.send(json.dumps(dict))
        time.sleep(delay)

    def disconnect(self):
        self.ws.close()


if __name__ == "__main__":
    # websocket.enableTrace(True)
    "ws://127.0.0.1:8000/ws/test/test/"
    # url_host = "ws://47.100.83.146:8000"
    url_host = "ws://47.100.83.146:8000"
    room = "/websocket/test/test/"
    nw = NetWork(url_host, room)
    print(nw.url)
    nw.connect()

    # nw.disconnect()

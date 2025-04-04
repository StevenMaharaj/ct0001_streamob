from connectors.base_connector import BaseConnector
from websockets.sync.client import connect
import zmq
import orjson

class GateConnector(BaseConnector):
    def __init__(self):
        self.base_url = "wss://fx-ws.gateio.ws/v4/ws/usdt"
        self.message_port = 5555  # Port for PUB socket
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(f"tcp://*:{self.message_port}")  # Bind PUB socket to a port

    def connect(self):
        """Connect to Gate.io WebSocket and publish order book updates."""
        with connect(self.base_url) as ws:
            # Subscribe to order book updates
            ws.send('{"channel": "futures.order_book", "event": "subscribe", "payload": ["BTC_USDT", "20", "0"]}')
            resp_str = ws.recv()
            resp = orjson.loads(resp_str)
            print(resp)
            assert resp['result']['status'] == 'success', "Subscription failed"

            while True:
                # Receive and process messages
                raw_data = orjson.loads(ws.recv())
                # print(raw_data)
                if raw_data:
                    # Parse the message
                    parsed_data = self.parse_data(raw_data)
                    # Publish the parsed data
                    self.socket.send(parsed_data)
                else:
                    break

    def parse_data(self, raw_data):
        """
        Parse the raw order book data into the format [bp, ap, bqty, aqty].
        """
        result = raw_data.get("result", {})
        bids = result.get("bids", [])
        asks = result.get("asks", [])

        # Extract the top bid and ask
        top_bid = bids[0] if bids else {"p": "0", "s": 0}
        top_ask = asks[0] if asks else {"p": "0", "s": 0}

        # Format the output as [bp, ap, bqty, aqty]
        bp = float(top_bid["p"])
        bqty = float(top_bid["s"])
        ap = float(top_ask["p"])
        aqty = float(top_ask["s"])

        return f"{bp} {ap} {bqty} {aqty}".encode('utf-8')

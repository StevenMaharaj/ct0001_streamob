from connectors.base_connector import BaseConnector
from websockets.sync.client import connect
import zmq
import orjson


class BybitConnector(BaseConnector):
    def __init__(self):
        self.base_url = "wss://stream.bybit.com/v5/public/linear"
        self.message_port = 5556  # Port for PUB socket
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(f"tcp://*:{self.message_port}")  # Bind PUB socket to a port

    def connect(self):
        """Connect to Bybit WebSocket and publish order book updates."""
        with connect(self.base_url) as ws:
            # Subscribe to order book updates
            ws.send('{"op": "subscribe", "args": ["orderbook.25.BTCUSDT"]}')
            resp_str = ws.recv()
            resp = orjson.loads(resp_str)
            print(resp)
            assert resp.get("success", False), "Subscription failed"

            while True:
                # Receive and process messages
                raw_data = orjson.loads(ws.recv())
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
        result = raw_data.get("data", {})
        bids = result.get("b", [])
        asks = result.get("a", [])

        # Extract the top bid and ask
        top_bid = bids[0] if bids else {"p": "0", "s": 0}
        top_ask = asks[0] if asks else {"p": "0", "s": 0}

        # Format the output as [bp, ap, bqty, aqty]
        bp = float(top_bid["p"])
        bqty = float(top_bid["s"])
        ap = float(top_ask["p"])
        aqty = float(top_ask["s"])

        return f"{bp} {ap} {bqty} {aqty}".encode('utf-8')

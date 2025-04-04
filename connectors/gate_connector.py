from connectors.base_connector import BaseConnector
from websockets.sync.client import connect
import zmq


class GateConnector(BaseConnector):
    def __init__(self):
        self.base_url = "wss://fx-ws.gateio.ws/v4/ws/usdt"
        self.message_port = 5555
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        

    def connect(self):
        # Logic to connect to the Gate API
        with connect("wss://fx-ws-testnet.gateio.ws/v4/ws/btc") as ws:
            # Subscribe to order book updates
            ws.send('{"time" : 123456, "channel" : "futures.order_book", "event": "subscribe", "payload" : ["BTC_USD", "1", "0"]}')
            resp = ws.recv()
            assert resp['result']['status'] == 'success', "Subscription failed"
            while True:
                # Receive and process messages
                raw_data = ws.recv()
                if raw_data:
                    # Process the message
                    parsed_data = self.parse_data(raw_data)
                    # Send the parsed data to the message queue
                    self.socket.send(parsed_data)
                else:
                    break

    def parse_data(self, raw_data):
        """
        Parse the raw order book data into the format [bp, ap, bqty, aqty].
        """
        result = raw_data.get("result", {})
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

        return [bp, ap, bqty, aqty]

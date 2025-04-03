from connectors.base_connector import BaseConnector


class GateConnector(BaseConnector):
    def __init__(self, api_key, api_secret):
        self.base_url = "https://api.gate.io/api2/1"

    def connect(self):
        # Logic to connect to the Gate API
        pass

    def parse_data(self, raw_data):
        # Logic to parse the raw order book data
        order_book = {
            "bids": raw_data.get("bids", []),
            "asks": raw_data.get("asks", []),
        }
        return order_book

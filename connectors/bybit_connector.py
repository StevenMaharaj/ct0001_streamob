from connectors.base_connector import BaseConnector


class BybitConnector(BaseConnector):
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.bybit.com"

    def connect(self):
        # Logic to connect to the Bybit API
        pass

    def parse_data(self, raw_data):
        # Logic to parse the raw order book data
        order_book = {"bids": [], "asks": []}
        for entry in raw_data["result"]:
            if entry["side"] == "Buy":
                order_book["bids"].append(entry)
            elif entry["side"] == "Sell":
                order_book["asks"].append(entry)
        return order_book

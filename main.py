# File: /btcusdt-arbitrage/btcusdt-arbitrage/src/main.py

from connectors.gate_connector import GateConnector
from connectors.bybit_connector import BybitConnector
from detector import ArbitrageDetector


def main():
    gate_connector = GateConnector()
    bybit_connector = BybitConnector()

    gate_order_book = gate_connector.fetch_order_book()
    bybit_order_book = bybit_connector.fetch_order_book()

    arb_detector = ArbitrageDetector()
    opportunities = arb_detector.detect_opportunities(gate_order_book, bybit_order_book)

    if opportunities:
        for opportunity in opportunities:
            print(f"Arbitrage Opportunity: {opportunity}")
    else:
        print("No arbitrage opportunities found.")


if __name__ == "__main__":
    main()

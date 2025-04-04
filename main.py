# File: /btcusdt-arbitrage/btcusdt-arbitrage/src/main.py

from multiprocessing import Process
from connectors.gate_connector import GateConnector
import zmq


def run_gate_connector():
    """Run the GateConnector as a publisher."""
    gate_connector = GateConnector()
    gate_connector.connect()


def arbitrage_detector():
    """Run the subscriber to receive messages from GateConnector."""
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")  # Connect to the PUB socket
    socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages

    while True:
        # Receive messages from the GateConnector
        message = socket.recv()
        print("Received message:", message.decode('utf-8'))
        # Here you can implement your arbitrage detection logic


def main():
    # Create a separate process for the GateConnector
    gate_process = Process(target=run_gate_connector)
    gate_process.start()

    # Create a separate process for the ArbitrageDetector
    detector_process = Process(target=arbitrage_detector)
    detector_process.start()

    # Wait for both processes to finish
    gate_process.join()
    detector_process.join()


if __name__ == "__main__":
    main()

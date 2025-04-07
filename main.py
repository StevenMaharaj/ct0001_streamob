from multiprocessing import Process
from connectors.bybit_connector import BybitConnector
from connectors.gate_connector import GateConnector
import zmq


def run_gate_connector():
    """Run the GateConnector as a publisher."""
    gate_connector = GateConnector()
    gate_connector.connect()

def run_bybit_connector():
    """Run the BybitConnector as a publisher."""
    bybit_connector = BybitConnector()
    bybit_connector.connect()

def arbitrage_detector():
    context = zmq.Context()
    socket_gate = context.socket(zmq.SUB)
    socket_gate.connect("tcp://localhost:5555")  # Connect to the PUB socket
    socket_gate.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages
    socket_bybit = context.socket(zmq.SUB)
    socket_bybit.connect("tcp://localhost:5556")  # Connect to the PUB socket
    socket_bybit.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages

    while True:
        message_gate_encoded = socket_gate.recv()
        message_bybit_encoded = socket_bybit.recv()

        # Decode the message
        message_gate = message_gate_encoded.decode('utf-8')
        message_bybit = message_bybit_encoded.decode('utf-8')

        # Split the message into components
        gate_components = message_gate.split()
        bybit_components = message_bybit.split()
        # Extract the components
        bp_gate = float(gate_components[0])
        ap_gate = float(gate_components[1])
        bp_bybit = float(bybit_components[0])
        ap_bybit = float(bybit_components[1])

        # decide if arbitrage opportunity exists
        if bp_gate > ap_bybit:
            print(f"Arbitrage opportunity detected! Buy on Bybit at {ap_bybit} and sell on Gate at {bp_gate}")
        elif ap_gate < bp_bybit:
            print(f"Arbitrage opportunity detected! Buy on Gate at {bp_gate} and sell on Bybit at {ap_bybit}")
        



def main():
    # Create a separate process for the GateConnector
    gate_process = Process(target=run_bybit_connector)
    gate_process.start()

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

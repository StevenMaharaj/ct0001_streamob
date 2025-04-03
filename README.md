# Stream Orderbooks
We will connect to two different orderbook for BTCUSDT perp. The orderbook data will be fed into another component which will detect any arbitrage opportunity.

## Program structure
Will create a general exchange connector interface then implement the connect interface for two different exchanges.

```mermaid
flowchart TD
    C{Connector Interface}
    C --> D[GateConnector]
    C --> E[BybitConnector]
```

The exchange will send raw json data. The connector will pass that into our data structure then send those objects to the arbitrage detector. The arbitrage detector will print any arbitrage opportunities to the terminal.

```mermaid
flowchart TD
    M(Exchange 1)
    N(Exchange 2)
    P{Connector 1}
    Q{Connector 2}
    R{Arb Finder}

    M --> |Raw OB data| P
    N -->|Raw OB data| Q
    P --> R
    Q --> R
```


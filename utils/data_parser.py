def parse_order_book(data):
    order_book = {"bids": [], "asks": []}

    for bid in data.get("bids", []):
        order_book["bids"].append({"price": float(bid[0]), "quantity": float(bid[1])})

    for ask in data.get("asks", []):
        order_book["asks"].append({"price": float(ask[0]), "quantity": float(ask[1])})

    return order_book


def format_order_book(order_book):
    formatted = {
        "highest_bid": order_book["bids"][0] if order_book["bids"] else None,
        "lowest_ask": order_book["asks"][0] if order_book["asks"] else None,
    }
    return formatted

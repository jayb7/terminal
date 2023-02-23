from bybit_api import client


def create_order(symbol_var, qty_entry, leverage_entry, side_var):
    symbol = symbol_var.get()
    qty = int(qty_entry.get())
    leverage = int(leverage_entry.get())
    side = side_var.get().lower()
    print(symbol, qty, leverage, side) # add this line

    if side == "buy":
        side = "Buy"
    elif side == "sell":
        side = "Sell"
    else:
        print("Invalid side")
        exit()

    # Set the leverage for all positions
    # client.Position.Position_leverage_update(symbol=symbol, leverage=leverage).result()

    order_response = client.Order.Order_new(
        symbol=symbol,
        side=side,
        order_type="Limit",
        qty=qty,
        price=10000,
        time_in_force="GoodTillCancel"
    ).result()

    print(order_response)

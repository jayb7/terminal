import tkinter as tk
import bybit

api_key = "your_api_key"
api_secret = "your_api_secret"

client = bybit.bybit(api_key=api_key, api_secret=api_secret)

def create_order():
    symbol = symbol_var.get()
    qty = int(qty_entry.get())
    leverage = int(leverage_entry.get())
    side = side_var.get().lower()

    if side == "buy":
        side = "Buy"
    elif side == "sell":
        side = "Sell"
    else:
        print("Invalid side")
        exit()

    # Set the leverage for all positions
    client.Position.Position_leverage_update(symbol=symbol, leverage=leverage).result()

    order_response = client.Order.Order_create(
        symbol=symbol,
        side=side,
        qty=qty,
        price=10000
    ).result()

    print(order_response)

def search_symbols(*args):
    # Get the search query
    query = search_entry.get().lower()

    # Remove all items from the OptionMenu widget
    symbol_var.set('')
    symbol_menu['menu'].delete(0, 'end')

    # Add the symbols that match the search query
    for symbol in symbols:
        if query in symbol.lower():
            symbol_menu['menu'].add_command(label=symbol, command=tk._setit(symbol_var, symbol))

# Create the main window
root = tk.Tk()
root.title("Bybit Order Creator")

# Get the list of symbols using the Symbol resource
symbol_data = client.Symbol.Symbol_get().result()[0]
symbols = [symbol['name'] for symbol in symbol_data['result']]

# Create a dropdown menu for symbol selection
symbol_var = tk.StringVar()
symbol_var.set(symbols[0])  # default value
symbol_menu = tk.OptionMenu(root, symbol_var, *symbols)
symbol_menu.pack()

# Create the Entry widget for the search query
search_entry = tk.Entry(root)
search_entry.pack()

# Bind the <KeyRelease> event to the Entry widget
search_entry.bind('<KeyRelease>', search_symbols)

# Create the label and entry widgets for quantity
qty_label = tk.Label(root, text="Enter the quantity:")
qty_label.pack()

qty_entry = tk.Entry(root)
qty_entry.pack()

# Create the label and entry widgets for leverage
leverage_label = tk.Label(root, text="Enter the leverage:")
leverage_label.pack()

leverage_entry = tk.Entry(root)
leverage_entry.insert(0, "1")  # Set the default leverage to 1
leverage_entry.pack()


# Create a dropdown menu for side selection
side_var = tk.StringVar()
side_var.set("Buy")  # default value
side_menu = tk.OptionMenu(root, side_var, "Buy", "Sell")
side_menu.pack()

# Create the button to create the order
create_button = tk.Button(root, text="Create Order", command=create_order)
create_button.pack()

# Run the main loop
root.mainloop()

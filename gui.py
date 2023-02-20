import tkinter as tk
from bybit_api import client
from order_creator import create_order
from symbol_searcher import search_symbols

def create_gui():
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
    search_entry.bind('<KeyRelease>', lambda event: search_symbols(search_entry, symbol_var, symbol_menu, symbols))

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
    create_button = tk.Button(root, text="Create Order", command=lambda: create_order(symbol_var, qty_entry, leverage_entry, side_var))
    create_button.pack()

    # Run the main loop
    root.mainloop()

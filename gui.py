import tkinter as tk
import requests
from bybit_api import client
from order_creator import create_order
from symbol_searcher import search_symbols

def get_news_data():
    url = "https://news.treeofalpha.com/api/news?limit=2"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def create_gui():
    # Create the main window
    root = tk.Tk()
    root.title("Bybit Order Creator and News")

    # Create a frame for the order creation widgets
    order_frame = tk.Frame(root)
    order_frame.pack(padx=20, pady=20)

    # Get the list of symbols using the Symbol resource
    symbol_data = client.Symbol.Symbol_get().result()[0]
    symbols = [symbol['name'] for symbol in symbol_data['result']]

    # Create a dropdown menu for symbol selection
    symbol_var = tk.StringVar()
    symbol_var.set(symbols[0])  # default value
    symbol_menu = tk.OptionMenu(order_frame, symbol_var, *symbols)
    symbol_menu.pack(side=tk.LEFT)

    # Create the Entry widget for the search query
    search_entry = tk.Entry(order_frame)
    search_entry.pack(side=tk.LEFT)

    # Bind the <KeyRelease> event to the Entry widget
    search_entry.bind('<KeyRelease>', lambda event: search_symbols(search_entry, symbol_var, symbol_menu, symbols))

    # Create the label and entry widgets for quantity
    qty_label = tk.Label(order_frame, text="Enter the quantity:")
    qty_label.pack()

    qty_entry = tk.Entry(order_frame)
    qty_entry.pack()

    # Create the label and entry widgets for leverage
    leverage_label = tk.Label(order_frame, text="Enter the leverage:")
    leverage_label.pack()

    leverage_entry = tk.Entry(order_frame)
    leverage_entry.insert(0, "1")  # Set the default leverage to 1
    leverage_entry.pack()

    # # Create a dropdown menu for side selection
    side_var = tk.StringVar()
    side_var.set("Buy")  # default value
    side_menu = tk.OptionMenu(order_frame, side_var, "Buy", "Sell")
    side_menu.pack()

    # # Create the button to create the order
    # create_button = tk.Button(order_frame, text="Create Order", command=lambda: create_order(symbol_var, qty_entry, leverage_entry, side_var))
    # create_button.pack()

    # Create buttons for side selection
    buy_long_button = tk.Button(order_frame, text="Buy/Long", command=lambda: create_order(symbol_var, qty_entry, leverage_entry, tk.StringVar(value="Buy")))
    buy_long_button.pack(side=tk.LEFT)

    sell_short_button = tk.Button(order_frame, text="Sell/Short", command=lambda: create_order(symbol_var, qty_entry, leverage_entry, tk.StringVar(value="Sell")))
    sell_short_button.pack(side=tk.LEFT)

    # Create the button to create the order
    create_button = tk.Button(order_frame, text="Create Order", command=lambda: create_order(symbol_var, qty_entry, leverage_entry, side_var))
    create_button.pack(side=tk.LEFT)



    # Get the news data
    news_data = get_news_data()

    # Create a frame for the news widgets
    news_frame = tk.Frame(root)
    news_frame.pack(padx=20, pady=20)

    # Create a label for the news data
    news_label = tk.Label(news_frame, text="News")
    news_label.pack()

    # Add the news data to the GUI
    if news_data is not None:
        for item in news_data:
            title = item.get("title", "")
            content = item.get("content", "")
            source = item.get("source", "")
            news_title_label = tk.Label(news_frame, text=title, font=("Helvetica", 16))
            news_title_label.pack()
            if content:
                news_content_label = tk.Label(news_frame, text=content, font=("Helvetica", 12))
                news_content_label.pack()
            news_source_label = tk.Label(news_frame, text=source, font=("Helvetica", 10))
            news_source_label.pack()
            news_divider_label = tk.Label(news_frame, text="--------------------------")
            news_divider_label.pack()

    # Run the main loop
    root.mainloop()
if __name__ == "__main__":
    create_gui()
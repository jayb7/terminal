import tkinter as tk
import requests
from bybit_api import client
from order_creator import create_order
from symbol_searcher import search_symbols

def get_news_data():
    url = "https://news.treeofalpha.com/api/news?limit=100"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def create_gui():
    # Create the main window
    root = tk.Tk()
    root.configure(background='#18122B')
    root.geometry("1200x700")
    root.title("JTerminal")

    # Get the news data
    news_data = get_news_data()

    # Extract symbols from news data
    symbols = []
    if news_data is not None:
        for item in news_data:
            symbol = item.get("symbol")
            if symbol:
                symbols.append(symbol)

     # Remove duplicates and sort the list
    symbols = sorted(list(set(symbols)))

    # Create a frame for the news widgets
    news_frame = tk.Frame(root)
    news_frame.pack(padx=20, pady=20, side=tk.TOP)

    # Create a frame for Other news
    other_news_frame = tk.Frame(news_frame)
    other_news_frame.pack(pady=10)

    # Create a label for Other news
    other_news_label = tk.Label(other_news_frame, text="Other News", font=("Helvetica", 16), bg="#443C68", fg="#ffffff")
    other_news_label.pack()

   # Create a frame for Twitter news
    twitter_news_frame = tk.Frame(news_frame)
    twitter_news_frame.pack(pady=10)

    # Create a label for Twitter news
    twitter_news_label = tk.Label(twitter_news_frame, text="Twitter News", font=("Helvetica", 16), bg="#443C68", fg="#ffffff")
    twitter_news_label.pack()

   # Add the news data to the GUI
    if news_data is not None:
        latest_twitter_item = None
        latest_other_item = None
        for item in news_data:
            source = item.get("source", "")
            if source == "Twitter":
             if latest_twitter_item is None or (item.get("published_at") is not None and latest_twitter_item.get("published_at") is not None and item.get("published_at") > latest_twitter_item.get("published_at")):
                 latest_twitter_item = item
            else:
                if latest_other_item is None or (item.get("published_at") is not None and latest_other_item.get("published_at") is not None and item.get("published_at") > latest_other_item.get("published_at")):
                    latest_other_item = item


        # Add the latest Twitter item to the GUI
        if latest_twitter_item is not None:
            title = latest_twitter_item.get("title", "")
            content = latest_twitter_item.get("content", "")
            bg_color = '#443C68'
            news_title_label = tk.Label(twitter_news_frame, text=title, font=("Helvetica", 16), bg=bg_color, fg="#ffffff")
            news_title_label.pack()
            if content:
                news_content_label = tk.Label(twitter_news_frame, text=content, font=("Helvetica", 12), bg=bg_color, fg="#ffffff", wraplength=600)
                news_content_label.pack()
                news_twitter_source_label = tk.Label(twitter_news_frame, text="source: Twitter", font=("Helvetica", 10))
                news_twitter_source_label.pack()

        # Add the latest item from any other source to the GUI
        if latest_other_item is not None:
            source = latest_other_item.get("source", "")
            title = latest_other_item.get("title", "")
            content = latest_other_item.get("content", "")
            bg_color = '#443C68'
            news_title_label = tk.Label(other_news_frame, text=title, font=("Helvetica", 16), bg=bg_color, fg="#ffffff")
            news_title_label.pack()
            if content:
                news_content_label = tk.Label(other_news_frame, text=content, font=("Helvetica", 12), bg=bg_color, fg="#ffffff", wraplength=600)
                news_content_label.pack()
                news_other_source_label = tk.Label(other_news_frame, text="source: "+source, font=("Helvetica", 10))
                news_other_source_label.pack()




    # Create a frame for the order creation widgets
    order_frame = tk.Frame(root)
    order_frame.pack(padx=20, pady=20)

    # Get the list of symbols using the Symbol resource
    symbol_data = client.Symbol.Symbol_get().result()[0]
    symbols += [symbol['name'] for symbol in symbol_data['result']]

   # Create a dropdown menu for symbol selection
    symbol_var = tk.StringVar()
    symbol_var.set(symbols[0])  # default value
    symbol_menu = tk.OptionMenu(other_news_frame, symbol_var, *symbols)
    symbol_menu.pack()

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

    # Create buttons for side selection
    buy_long_button = tk.Button(order_frame, text="Buy/Long", command=lambda: create_order(symbol_var, qty_entry, leverage_entry, tk.StringVar(value="Buy")))
    buy_long_button.pack(side=tk.LEFT)

    sell_short_button = tk.Button(order_frame, text="Sell/Short", command=lambda: create_order(symbol_var, qty_entry, leverage_entry, tk.StringVar(value="Sell")))
    sell_short_button.pack(side=tk.LEFT)


    
    # Run the main loop
    root.mainloop()
if __name__ == "__main__":
    create_gui()
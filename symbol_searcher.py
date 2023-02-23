import tkinter as tk
from bybit_api import client

def search_symbols(search_entry, symbol_var, symbol_menu, symbols):
    # Get the search query
    query = search_entry.get().lower()

    # Remove all items from the OptionMenu widget
    symbol_var.set('')
    symbol_menu['menu'].delete(0, 'end')

    # Add the symbols that match the search query
    for symbol in symbols:
        if query in symbol.lower():
            symbol_menu['menu'].add_command(label=symbol, command=tk._setit(symbol_var, symbol))

    # Open the dropdown menu
    symbol_menu['menu'].tk_popup(search_entry.winfo_rootx(), search_entry.winfo_rooty() + search_entry.winfo_height())

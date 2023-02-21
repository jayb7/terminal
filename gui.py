import tkinter as tk
from terminal.config import Config


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.title("Python Terminal")
        self.geometry("500x500")
        self.text_area = tk.Text(self)
        self.text_area.grid(row=0, column=0, sticky="nsew")
        self.scrollbar = tk.Scrollbar(self, command=self.text_area.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.input_field = tk.Entry(self)
        self.input_field.grid(row=1, column=0, sticky="ew")
        self.input_field.bind("<Return>", self.process_input)

    def process_input(self, event):
        input_text = self.input_field.get()
        self.input_field.delete(0, tk.END)
        self.text_area.insert(tk.END, f"{input_text}\n")
        if input_text == "quit":
            self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()

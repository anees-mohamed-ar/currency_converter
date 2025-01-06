import tkinter as tk
from tkinter import ttk, messagebox
import requests
from utils import apply_styles
from reversed_currency_codes import currency_codes  # Import the currency_codes dictionary

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        self.exchange_rates = {}

        # Apply styles
        apply_styles()

        # UI Elements
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Currency Converter", font=("Helvetica", 18, "bold")).pack(pady=10)

        from_frame = ttk.Frame(main_frame)
        from_frame.pack(pady=5)
        ttk.Label(from_frame, text="From Currency:").pack(side=tk.LEFT, padx=5)
        self.from_currency = ttk.Combobox(from_frame, width=30, values=[])
        self.from_currency.pack(side=tk.LEFT, padx=5)

        to_frame = ttk.Frame(main_frame)
        to_frame.pack(pady=5)
        ttk.Label(to_frame, text="To Currency:").pack(side=tk.LEFT, padx=5)
        self.to_currency = ttk.Combobox(to_frame, width=30, values=[])
        self.to_currency.pack(side=tk.LEFT, padx=5)

        amount_frame = ttk.Frame(main_frame)
        amount_frame.pack(pady=5)
        ttk.Label(amount_frame, text="Amount:").pack(side=tk.LEFT, padx=5)
        self.amount_entry = ttk.Entry(amount_frame, width=20)
        self.amount_entry.pack(side=tk.LEFT, padx=5)

        self.status_label = ttk.Label(main_frame, text="Status: Ready", font=("Helvetica", 10, "italic"))
        self.status_label.pack(pady=5)

        self.convert_button = ttk.Button(main_frame, text="Convert", command=self.convert_currency)
        self.convert_button.pack(pady=10)

        self.result_label = ttk.Label(main_frame, text="", style="Result.TLabel")
        self.result_label.pack(pady=10)

        # Fetch exchange rates after initializing status_label
        self.fetch_exchange_rates()

    def fetch_exchange_rates(self):
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        try:
            response = requests.get(url)
            data = response.json()
            self.date = data['date']
            print(f'Date : {self.date}')
            self.exchange_rates = data['rates']
            self.from_currency['values'] = [f"{currency_codes[code]} ({code})" for code in self.exchange_rates.keys() if code in currency_codes]
            self.to_currency['values'] = [f"{currency_codes[code]} ({code})" for code in self.exchange_rates.keys() if code in currency_codes]
            self.status_label.config(text="Status: Exchange rates updated")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching exchange rates: {e}")
            self.status_label.config(text="Status: Error fetching exchange rates")

    def convert_currency(self):
        from_currency = self.from_currency.get().split()[-1][1:-1]
        to_currency = self.to_currency.get().split()[-1][1:-1]
        amount = self.amount_entry.get()

        if not from_currency or not to_currency or not amount:
            messagebox.showwarning("Input Error", "Please enter all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid amount.")
            return
        #operation to convert the amount
        rate = self.exchange_rates.get(to_currency) / self.exchange_rates.get(from_currency)
        converted_amount = amount * rate

        # Update the result label with the converted amount and style
        self.result_label.config(
            text=f"Converted Amount: {converted_amount:.2f} {to_currency}"
        )

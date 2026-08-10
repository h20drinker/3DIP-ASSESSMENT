#takeaway ordering system verison 1



import csv
import tkinter as tk
from tkinter import messagebox

MENU_FILE = "menue.csv"

# creating a class for menu items and orders
class menue_item:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Order:
    def __init__(self):
        self.items = []
    def add_item(self, item):
        self.items.append(item)

    def calculate_total(self):
        return sum(item.price for item in self.items)

    def clear(self):
        self.items = []

def load_menu(filename):
    menu_items = []
    try: 
        with open(filename, newline="", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if len(row) != 2:
                    continue
 
                name, price_text = row
                name = name.strip()
 
                try:
                    price = float(price_text)
                except ValueError:
                    print(f"Skipping invalid menu row: {row}")
                    continue
 
                if price < 0:
                    print(f"Skipping menu row with negative price: {row}")
                    continue
 
                menu_items.append(menue_item(name, price))
 
    except FileNotFoundError:
        print(f"Menu file '{filename}' was not found.")
 
    return menu_items


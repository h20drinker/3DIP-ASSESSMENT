#takeaway ordering system verison 2

import csv
import tkinter as tk
from tkinter import messagebox

# Name of the CSV file containing the menu items and prices
MENU_FILE = "menu.csv"

# creating a class for menu items and orders
class menu_item:
    def __init__(self, name, price):
        self.name = name
        self.price = price

# Stores and manages the customer's order
class Order:
    def __init__(self):
        self.items = []
    def add_item(self, item):
        self.items.append(item)

    def calculate_total(self):
        return sum(item.price for item in self.items)

    def clear(self):
        self.items = []

# Loads menu items from the CSV file
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
 
                menu_items.append(menu_item(name, price))
 
    except FileNotFoundError:
        print(f"Menu file '{filename}' was not found.")
 
    return menu_items


# Main application and GUI
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Takeaway Order System")

        self.menu_items = load_menu(MENU_FILE)
        self.order = Order()

        self.build_gui()

    def build_gui(self):
        menu_frame = tk.LabelFrame(
            self.root,
            text="Menu",
            padx=10,
            pady=10
        )
        menu_frame.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="n"
        )

        if not self.menu_items:
            tk.Label(
                menu_frame,
                text="No menu items found. Check menu.csv.",
                fg="red",
            ).pack()
        else:
            for item in self.menu_items:
                button_text = f"{item.name} - ${item.price:.2f}"

                button = tk.Button(
                    menu_frame,
                    text=button_text,
                    width=25,
                    command=lambda menu_item=item:
                        self.add_item_to_order(menu_item),
                )

                button.pack(pady=2)

        order_frame = tk.LabelFrame(
            self.root,
            text="Current Order",
            padx=10,
            pady=10
        )
        order_frame.grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky="n"
        )

        self.order_listbox = tk.Listbox(
            order_frame,
            width=35,
            height=12
        )
        self.order_listbox.pack()

        self.total_label = tk.Label(
            order_frame,
            text="Total: $0.00",
            font=("Arial", 12, "bold")
        )
        self.total_label.pack(pady=(10, 5))

        clear_button = tk.Button(
            order_frame,
            text="Clear Order",
            command=self.clear_order
        )
        clear_button.pack(pady=5)


    # Adds a menu item and refreshes the order display
    def add_item_to_order(self, item):
        self.order.add_item(item)
        self.update_order_display()

    # Updates the order list and total price
    def update_order_display(self):
        self.order_listbox.delete(0, tk.END)

        for item in self.order.items:
            self.order_listbox.insert(
                tk.END,
                f"{item.name} - ${item.price:.2f}"
            )

        total = self.order.calculate_total()

        self.total_label.config(
            text=f"Total: ${total:.2f}"
        )

    # Clears the order after asking for confirmation
    def clear_order(self):
        if not self.order.items:
            return

        confirmed = messagebox.askyesno(
            "Clear Order",
            "Are you sure you want to clear the current order?"
        )

        if confirmed:
            self.order.clear()
            self.update_order_display()


# Start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

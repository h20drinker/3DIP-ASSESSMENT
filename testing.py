#takeaway ordering system verison 3

import os
import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

MENU_FILE = "menu.csv"
ORDERS_FILE = "orders.csv"

class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, index):
        if 0 <= index < len(self.items):
            del self.items[index]

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
 
                menu_items.append(MenuItem(name, price))
 
    except FileNotFoundError:
        print(f"Menu file '{filename}' was not found.")
 
    return menu_items

def validate_payment(payment_text, total):
    payment_text = payment_text.strip()

    if payment_text == "":
        return False, "Please enter a payment amount."
 
    try:
        amount = float(payment_text)
    except ValueError:
        return False, "Payment must be a number, e.g. 10.00."
 
    if amount < 0:
        return False, "Payment cannot be negative."
 
    if amount < total:
        return False, "Payment is less than the total. Please enter a larger amount."
 
    return True, amount

def calculate_change(amount_paid, total):
    return round(amount_paid - total, 2)

def save_order(order, amount_paid, change, filename=ORDERS_FILE):
    file_exists = os.path.isfile(filename)
 
    with open(filename, "a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
 
        if not file_exists:
            writer.writerow(["timestamp", "items", "total", "amount_paid", "change"])
 
        items_summary = "; ".join(
            f"{item.name} (${item.price:.2f})" for item in order.items
        )
        total = order.calculate_total()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
        writer.writerow(
            [
                timestamp,
                items_summary,
                f"{total:.2f}",
                f"{amount_paid:.2f}",
                f"{change:.2f}",
            ]
        )


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

        #test
        order_frame = tk.LabelFrame(self.root, text="Current Order", padx=10, pady=10)
        order_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")
 
        self.order_listbox = tk.Listbox(order_frame, width=35, height=10)
        self.order_listbox.pack()

        remove_button = tk.Button(
            order_frame, text="Remove Selected Item", command=self.remove_selected_item
        )
        remove_button.pack(pady=(5, 0))




 
        self.total_label = tk.Label(
            order_frame, text="Total: $0.00", font=("Arial", 12, "bold")
        )
        self.total_label.pack(pady=(10, 10))
 
        
        payment_row = tk.Frame(order_frame)
        payment_row.pack(pady=5)
 
        tk.Label(payment_row, text="Amount Paid: $").pack(side="left")
        self.payment_entry = tk.Entry(payment_row, width=10)
        self.payment_entry.pack(side="left")
 
        button_row = tk.Frame(order_frame)
        button_row.pack(pady=5)
 
        complete_button = tk.Button(
            button_row, text="Complete Order", command=self.complete_order
        )
        complete_button.pack(side="left", padx=5)
 
        clear_button = tk.Button(
            button_row, text="Clear Order", command=self.clear_order
        )
        clear_button.pack(side="left", padx=5)
 
        self.change_label = tk.Label(order_frame, text="")
        self.change_label.pack(pady=(10, 0))

    def add_item_to_order(self, item):
        self.order.add_item(item)
        self.update_order_display()

    def remove_selected_item(self):
        selection = self.order_listbox.curselection()
        if not selection:
            messagebox.showerror(
                "No Selection", "Please select an item in the order to remove."
            )
            return
 
        index = selection[0]
        self.order.remove_item(index)
        self.update_order_display()

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

    def complete_order(self):
        if not self.order.items:
            messagebox.showerror(
                "No Items",
                "Please add at least one item before completing the order."
            )
            return

        total = self.order.calculate_total()
        payment_text = self.payment_entry.get()

        is_valid, result = validate_payment(payment_text, total)

        if not is_valid:
            messagebox.showerror("Invalid Payment", result)
            return

        amount_paid = result
        change = calculate_change(amount_paid, total)

        save_order(self.order, amount_paid, change)

        self.change_label.config(
            text=f"Change given: ${change:.2f}"
        )

        messagebox.showinfo(
            "Order Complete",
            f"Order complete!\n"
            f"Total: ${total:.2f}\n"
            f"Paid: ${amount_paid:.2f}\n"
            f"Change: ${change:.2f}"
        )

        self.order.clear()
        self.payment_entry.delete(0, tk.END)
        self.change_label.config(text="")
        self.update_order_display()

    def clear_order(self):
        if not self.order.items:
            return

        confirmed = messagebox.askyesno(
            "Clear Order",
            "Are you sure you want to clear the current order?"
        )

        if confirmed:
            self.order.clear()
            self.change_label.config(text="")
            self.update_order_display()



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

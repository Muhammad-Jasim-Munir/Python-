import tkinter as tk
from tkinter import ttk, messagebox
import os
import math

# File paths for saving history
TAX_FILE = "tax_results.txt"
CALC_HISTORY_FILE = "calculator_history.txt"

# Tax slabs for calculation
TAX_SLABS = [
    (600000, 0.0),
    (1200000, 0.05),
    (2200000, 0.15),
    (3200000, 0.25),
    (4100000, 0.30),
    (float('inf'), 0.35),
]

def calculate_tax(income):
    tax = 0
    if income <= 600000:
        tax = 0
    elif income <= 1200000:
        tax = (income - 600000) * 0.05
    elif income <= 2200000:
        tax = 30000 + (income - 1200000) * 0.15
    elif income <= 3200000:
        tax = 180000 + (income - 2200000) * 0.25
    elif income <= 4100000:
        tax = 430000 + (income - 3200000) * 0.30
    else:
        tax = 700000 + (income - 4100000) * 0.35
    return round(tax, 2)

def calculate_tax_gui():
    try:
        income = float(tax_income_entry.get())
        if income < 0:
            raise ValueError("Income cannot be negative.")
        tax = calculate_tax(income)
        net_income = income - tax
        tax_result_label.config(text=f"Total Tax Payable: Rs. {tax}")
        net_income_label.config(text=f"Net Annual Income: Rs. {net_income}")
        with open(TAX_FILE, "a") as file:
            file.write(f"Income: Rs. {income}, Tax: Rs. {tax}, Net Income: Rs. {net_income}\n")
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def view_tax_history():
    if os.path.exists(TAX_FILE):
        with open(TAX_FILE, "r") as file:
            history = file.read()
        messagebox.showinfo("Tax History", history or "No history available.")
    else:
        messagebox.showinfo("Tax History", "No history available.")

def search_tax_history():
    search_term = tax_search_entry.get()
    if os.path.exists(TAX_FILE):
        with open(TAX_FILE, "r") as file:
            history = file.readlines()
        search_results = [line for line in history if search_term in line]
        if search_results:
            messagebox.showinfo("Search Results", "\n".join(search_results))
        else:
            messagebox.showinfo("Search Results", f"No records found for '{search_term}'.")
    else:
        messagebox.showinfo("Tax History", "No history available.")

def delete_tax_history():
    if os.path.exists(TAX_FILE):
        os.remove(TAX_FILE)
        messagebox.showinfo("Success", "Tax history cleared.")
    else:
        messagebox.showinfo("Error", "No history to clear.")

def calculate_expression():
    try:
        expression = calc_entry.get()
        result = eval(expression)
        calc_entry.delete(0, tk.END)
        calc_entry.insert(0, str(round(result, 2)))
        with open(CALC_HISTORY_FILE, "a") as file:
            file.write(f"{expression} = {result}\n")
    except Exception as e:
        messagebox.showerror("Error", "Invalid expression.")

def view_calc_history():
    if os.path.exists(CALC_HISTORY_FILE):
        with open(CALC_HISTORY_FILE, "r") as file:
            history = file.read()
        messagebox.showinfo("Calculator History", history or "No history available.")
    else:
        messagebox.showinfo("Calculator History", "No history available.")

def clear_calc_history():
    if os.path.exists(CALC_HISTORY_FILE):
        os.remove(CALC_HISTORY_FILE)
        messagebox.showinfo("Success", "Calculator history cleared.")
    else:
        messagebox.showinfo("Error", "No history to clear.")

def add_to_expression(symbol):
    calc_entry.insert(tk.END, symbol)

def calculate_sqrt():
    add_to_expression("math.sqrt(")

def calculate_sin():
    add_to_expression("math.sin(math.radians(")

def calculate_cos():
    add_to_expression("math.cos(math.radians(")

def calculate_tan():
    add_to_expression("math.tan(math.radians(")

def calculate_log():
    add_to_expression("math.log10(")

def calculate_exp():
    add_to_expression("math.exp(")

def create_app():
    root = tk.Tk()
    root.title("Simple Tax & Scientific Calculator App")
    root.geometry("600x700")

    ttk.Label(root, text="Created by Muhammad Jasim", font=("Arial", 14), foreground="#000000").pack(pady=10)

    tab_control = ttk.Notebook(root)

    tax_tab = ttk.Frame(tab_control)
    tab_control.add(tax_tab, text="Tax Calculator")

    ttk.Label(tax_tab, text="Enter Annual Income:").pack(pady=10)
    global tax_income_entry
    tax_income_entry = ttk.Entry(tax_tab, width=30, font=('Arial', 12))
    tax_income_entry.pack(pady=10)
    ttk.Button(tax_tab, text="Calculate Tax", command=calculate_tax_gui).pack(pady=10)
    ttk.Button(tax_tab, text="View Tax History", command=view_tax_history).pack(pady=10)

    global tax_result_label, net_income_label
    tax_result_label = ttk.Label(tax_tab, text="", font=("Arial", 14))
    tax_result_label.pack(pady=20)

    net_income_label = ttk.Label(tax_tab, text="", font=("Arial", 14))
    net_income_label.pack(pady=20)

    ttk.Label(tax_tab, text="Search in History:").pack(pady=5)
    global tax_search_entry
    tax_search_entry = ttk.Entry(tax_tab, width=30, font=('Arial', 12))
    tax_search_entry.pack(pady=5)
    ttk.Button(tax_tab, text="Search", command=search_tax_history).pack(pady=5)
    ttk.Button(tax_tab, text="Delete History", command=delete_tax_history).pack(pady=10)

    calc_tab = ttk.Frame(tab_control)
    tab_control.add(calc_tab, text="Scientific Calculator")

    global calc_entry
    calc_entry = ttk.Entry(calc_tab, width=30, font=('Arial', 14))
    calc_entry.pack(pady=10)

    button_frame = ttk.Frame(calc_tab)
    button_frame.pack(pady=20)

    buttons = [
        ("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("/", 0, 3),
        ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("*", 1, 3),
        ("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("-", 2, 3),
        ("0", 3, 0), (".", 3, 1), ("=", 3, 2), ("+", 3, 3),
        ("√", 4, 0), ("sin", 4, 1), ("cos", 4, 2), ("tan", 4, 3),
        ("log", 5, 0), ("exp", 5, 1)
    ]

    for text, row, col in buttons:
        if text == "=":
            command = calculate_expression
        elif text == "√":
            command = calculate_sqrt
        elif text == "sin":
            command = calculate_sin
        elif text == "cos":
            command = calculate_cos
        elif text == "tan":
            command = calculate_tan
        elif text == "log":
            command = calculate_log
        elif text == "exp":
            command = calculate_exp
        else:
            command = lambda t=text: add_to_expression(t)

        button = ttk.Button(button_frame, text=text, width=8, command=command)
        button.grid(row=row, column=col, padx=10, pady=10)

    ttk.Button(calc_tab, text="View Calc History", command=view_calc_history).pack(pady=10)
    ttk.Button(calc_tab, text="Clear Calc History", command=clear_calc_history).pack(pady=10)

    tab_control.pack(expand=1, fill="both")
    root.mainloop()

if __name__ == "__main__":
    create_app()

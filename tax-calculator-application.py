# tax-calculator-application-py
import tkinter as tk
from tkinter import messagebox, ttk
import json
import csv
from pathlib import Path

# Load tax slabs from JSON file
def load_tax_slabs():
    try:
        with open('tax_slabs.json') as file:
            slabs = json.load(file)
            return [(s['limit'], s['rate']) for s in slabs]
    except Exception as e:
        messagebox.showerror("Error", f"Could not load tax slabs: {e}")
        return []

tax_slabs = load_tax_slabs()

# Function to calculate tax
def calculate_tax(income):
    tax = 0
    for slab in tax_slabs:
        if slab[0] is None or income > slab[0]:
            tax += slab[0] * slab[1] if slab[0] is not None else (income * slab[1])
            income -= slab[0] if slab[0] is not None else income
        else:
            tax += income * slab[1]
            break
    return tax

# Function to save income and tax to a file
def save_to_file(income, tax, deductions):
    with open('tax_records.json', 'a') as file:
        record = {'income': income, 'tax': tax, 'deductions': deductions}
        file.write(json.dumps(record) + '\n')

# Function to export history to CSV
def export_to_csv():
    try:
        with open('tax_records.json') as file:
            records = [json.loads(line) for line in file]
        
        with open('tax_records.csv', 'w', newline='') as csvfile:
            fieldnames = ['income', 'tax', 'deductions']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
        
        messagebox.showinfo("Export", "Data exported to tax_records.csv")
    except Exception as e:
        messagebox.showerror("Error", f"Could not export data: {e}")

# Function to handle the calculation and file saving
def on_calculate():
    try:
        income = float(entry_income.get())
        deductions = float(entry_deductions.get())
        if income < 0 or deductions < 0:
            raise ValueError("Income and deductions cannot be negative.")
        
        taxable_income = income - deductions
        if taxable_income < 0:
            raise ValueError("Deductions cannot exceed income.")

        tax = calculate_tax(taxable_income)
        messagebox.showinfo("Tax Calculation", f"Your tax is: PKR {tax:.2f}")
        save_to_file(income, tax, deductions)
        
        update_history(income, tax, deductions)
        
        entry_income.delete(0, tk.END)
        entry_deductions.delete(0, tk.END)
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# Function to update history display
def update_history(income, tax, deductions):
    history_list.insert(tk.END, f"Income: PKR {income}, Tax: PKR {tax:.2f}, Deductions: PKR {deductions}")

# Setting up the GUI
root = tk.Tk()
root.title("Enhanced Tax Calculator")

# Application layout
frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

label_title = tk.Label(frame, text="Salaried Person Tax Calculator", font=("Arial", 16))
label_title.grid(row=0, columnspan=2, pady=10)

label_income = tk.Label(frame, text="Enter your annual income (PKR):")
label_income.grid(row=1, column=0, sticky="e")

entry_income = tk.Entry(frame, width=25)
entry_income.grid(row=1, column=1)

label_deductions = tk.Label(frame, text="Enter deductions (PKR):")
label_deductions.grid(row=2, column=0, sticky="e")

entry_deductions = tk.Entry(frame, width=25)
entry_deductions.grid(row=2, column=1)

button_calculate = tk.Button(frame, text="Calculate Tax", command=on_calculate)
button_calculate.grid(row=3, columnspan=2, pady=10)

button_export = tk.Button(frame, text="Export History to CSV", command=export_to_csv)
button_export.grid(row=4, columnspan=2, pady=10)

label_history = tk.Label(frame, text="Calculation History:")
label_history.grid(row=5, columnspan=2, pady=10)

history_list = tk.Listbox(frame, width=50, height=10)
history_list.grid(row=6, columnspan=2, pady=10)

label_footer = tk.Label(frame, text="Developed by Your Name", font=("Arial", 10))
label_footer.grid(row=7, columnspan=2, pady=10)

root.mainloop()
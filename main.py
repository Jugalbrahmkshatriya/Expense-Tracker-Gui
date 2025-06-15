"""

import json
import os 
import csv
from datetime import datetime
EXPENSE_FILE = "expenses.json" # The file where we will save expenses

def load_expenses():
    if os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "r") as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open(EXPENSE_FILE,"w") as f:
        json.dump(expenses, f, indent=4)

def add_expense(expenses):
    date=input("Enter date(YYYY-MM-DD) or leave blank for today: ").strip()
    if not date:
        date= datetime.today().strftime("%y-%m-%d")
    category=input("Enter category (e.g., food, transport):").strip()
    try:
        amount=float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount.  Must be in Number.")
        return 
    note= input("Optional note: ").strip()

    expense={
        "date":date,
        "category":category,
        "amount":amount,
        "note":note
    }

    expenses.append(expense)
    save_expenses(expenses)
    print("✅ Expense added!")

def view_expenses(expenses):
    if not expenses:
        print("No ex[expenses recorded yet.")
        return 
    print("\n--- Your Expenses ---")
    for i, exp in enumerate(expenses,1):
        print(f"{i}.{exp['date']} | ₹{exp['amount']} | {exp['category']} | {exp.get('note','')}")

def delete_expense(expenses):
    view_expenses(expenses)
    try:
        idx= int(input("Enter expense number to delete: "))
        if 1<= idx <= len(expenses):
            removed= expenses.pop(idx-1)
            save_expenses(expenses)
            print(f"✅ Removed: ₹{removed['amount']} on {removed['date']}")
        else:
            print("Invalid Index.")
    except ValueError:
        print("Invalid Error")

def export_to_csv(expenses):
    if not expenses:
        print("No expenses to export.")
        return 
    if not os.path.exists("exports"):
        os.makedirs("exports")
    filepath = os.path.join("exports", "report.csv")
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f,fieldnames=["date", "category", "amount", "note"])
        writer.writeheader()
        writer.writerows(expenses)
    print(f"✅ Exported to {filepath}")
def show_summary(expenses):
    if not expenses:
        print("No expenses to summarize.")
        return 
    total = sum(exp["amount"]for exp in expenses)
    print(f"\n 💰 Total Spent: ₹{total:.2f}")
    categories = {}
    for exp in expenses:
        categories[exp["category"]] = categories.get(exp["category"],0)+exp["amount"]
    print("\n📂 Category-wise:")
    for cat,amt in categories.items():
        print(f" {cat}: ₹{amt:.2f}")

def main():
    expenses = load_expenses()
    while True:
        print("\n=== PERSONAL EXPENSE TRACKER ===")
        print("1. Add Expense")
        print("2. View Expense")
        print("3. Delete Expense")
        print("4. Export to CSV")
        print("5. Show Summary")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            delete_expense(expenses)
        elif choice == "4":
            export_to_csv(expenses)
        elif choice == "5":
            show_summary(expenses)
        elif choice == "6":
            print("👋 Exiting... All data saved.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main() 

"""

"""
import json
import os
import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

EXPENSE_FILE = "expenses.json"

def load_expenses():
    if os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "r") as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open(EXPENSE_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

def export_to_csv():
    if not expenses:
        messagebox.showinfo("Info", "No expenses to export.")
        return
    if not os.path.exists("exports"):
        os.makedirs("exports")
    filepath = os.path.join("exports", "report.csv")
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "category", "amount", "note"])
        writer.writeheader()
        writer.writerows(expenses)
    messagebox.showinfo("Success", f"Exported to {filepath}")

def show_summary():
    if not expenses:
        messagebox.showinfo("Summary", "No expenses to summarize.")
        return
    total = sum(exp["amount"] for exp in expenses)
    categories = {}
    for exp in expenses:
        categories[exp["category"]] = categories.get(exp["category"], 0) + exp["amount"]
    summary_text = f"💰 Total Spent: ₹{total:.2f}\n\n📂 Category-wise:\n"
    for cat, amt in categories.items():
        summary_text += f"{cat}: ₹{amt:.2f}\n"
    messagebox.showinfo("Summary", summary_text)

def refresh_tree():
    for row in tree.get_children():
        tree.delete(row)
    for exp in expenses:
        tree.insert("", "end", values=(exp["date"], exp["category"], f"₹{exp['amount']}", exp["note"]))

def add_expense_gui():
    date = date_entry.get().strip()
    if not date:
        date = datetime.today().strftime("%Y-%m-%d")
    category = category_entry.get().strip()
    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number.")
        return
    note = note_entry.get().strip()

    new_expense = {
        "date": date,
        "category": category,
        "amount": amount,
        "note": note
    }
    expenses.append(new_expense)
    save_expenses(expenses)
    refresh_tree()
    clear_inputs()
    messagebox.showinfo("Success", "Expense added!")

def delete_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select an expense to delete.")
        return
    for sel in selected:
        index = tree.index(sel)
        del expenses[index]
    save_expenses(expenses)
    refresh_tree()

def clear_inputs():
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    note_entry.delete(0, tk.END)

# ---------------------- GUI Setup ----------------------

expenses = load_expenses()

root = tk.Tk()
root.title("💸 Personal Expense Tracker (GUI)")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# -------- Form Inputs --------
tk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="e")
date_entry = tk.Entry(frame)
date_entry.grid(row=0, column=1, pady=2)

tk.Label(frame, text="Category:").grid(row=1, column=0, sticky="e")
category_entry = tk.Entry(frame)
category_entry.grid(row=1, column=1, pady=2)

tk.Label(frame, text="Amount:").grid(row=2, column=0, sticky="e")
amount_entry = tk.Entry(frame)
amount_entry.grid(row=2, column=1, pady=2)

tk.Label(frame, text="Note:").grid(row=3, column=0, sticky="e")
note_entry = tk.Entry(frame)
note_entry.grid(row=3, column=1, pady=2)

# -------- Buttons --------
tk.Button(frame, text="Add Expense", command=add_expense_gui, bg="#4CAF50", fg="white").grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")
tk.Button(frame, text="Delete Selected", command=delete_selected, bg="#f44336", fg="white").grid(row=5, column=0, columnspan=2, pady=5, sticky="ew")
tk.Button(frame, text="Export to CSV", command=export_to_csv).grid(row=6, column=0, columnspan=2, pady=5, sticky="ew")
tk.Button(frame, text="Show Summary", command=show_summary).grid(row=7, column=0, columnspan=2, pady=5, sticky="ew")

# -------- Tree Table --------
tree = ttk.Treeview(root, columns=("Date", "Category", "Amount", "Note"), show="headings")
tree.heading("Date", text="Date")
tree.heading("Category", text="Category")
tree.heading("Amount", text="Amount")
tree.heading("Note", text="Note")
tree.pack(padx=10, pady=10, fill="both", expand=True)

refresh_tree()

root.mainloop()
"""
import json
import os
import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
import openpyxl
import subprocess  # For opening Excel on Windows

EXPENSE_FILE = "expenses.json"

def load_expenses():
    if os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "r") as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open(EXPENSE_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

def export_to_csv():
    if not expenses:
        messagebox.showinfo("Info", "No expenses to export.")
        return

    if not os.path.exists("exports"):
        os.makedirs("exports")

    csv_path = os.path.join("exports", "report.csv")
    xlsx_path = os.path.join("exports", "report.xlsx")

    # Export to CSV (original)
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "category", "amount", "note"])
        writer.writeheader()
        writer.writerows(expenses)

    # Also export to Excel
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Expenses"
        ws.append(["Date", "Category", "Amount", "Note"])
        for exp in expenses:
            ws.append([exp["date"], exp["category"], exp["amount"], exp["note"]])
        wb.save(xlsx_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export Excel: {e}")
        return

    # Ask to open Excel
    response = messagebox.askyesno("Export Complete", "Files saved to 'exports/'.\nDo you want to open in Excel?")
    if response:
        try:
            subprocess.Popen(["start", xlsx_path], shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Excel:\n{e}")

def show_summary():
    if not expenses:
        messagebox.showinfo("Summary", "No expenses to summarize.")
        return
    total = sum(exp["amount"] for exp in expenses)
    categories = {}
    for exp in expenses:
        categories[exp["category"]] = categories.get(exp["category"], 0) + exp["amount"]
    summary_text = f"💰 Total Spent: ₹{total:.2f}\n\n📂 Category-wise:\n"
    for cat, amt in categories.items():
        summary_text += f"{cat}: ₹{amt:.2f}\n"
    messagebox.showinfo("Summary", summary_text)

def refresh_tree():
    for row in tree.get_children():
        tree.delete(row)
    for exp in expenses:
        tree.insert("", "end", values=(exp["date"], exp["category"], f"₹{exp['amount']}", exp["note"]))

def add_expense_gui():
    date = date_entry.get().strip()
    if not date:
        date = datetime.today().strftime("%Y-%m-%d")
    category = category_entry.get().strip()
    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number.")
        return
    note = note_entry.get().strip()

    new_expense = {
        "date": date,
        "category": category,
        "amount": amount,
        "note": note
    }
    expenses.append(new_expense)
    save_expenses(expenses)
    refresh_tree()
    clear_inputs()
    messagebox.showinfo("Success", "Expense added!")

def delete_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select an expense to delete.")
        return
    for sel in selected:
        index = tree.index(sel)
        del expenses[index]
    save_expenses(expenses)
    refresh_tree()

def clear_inputs():
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    note_entry.delete(0, tk.END)

# ---------------------- GUI Setup ----------------------

expenses = load_expenses()

root = tk.Tk()
root.title("💸 Personal Expense Tracker (GUI)")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="e")
date_entry = tk.Entry(frame)
date_entry.grid(row=0, column=1, pady=2)

tk.Label(frame, text="Category:").grid(row=1, column=0, sticky="e")
category_entry = tk.Entry(frame)
category_entry.grid(row=1, column=1, pady=2)

tk.Label(frame, text="Amount:").grid(row=2, column=0, sticky="e")
amount_entry = tk.Entry(frame)
amount_entry.grid(row=2, column=1, pady=2)

tk.Label(frame, text="Note:").grid(row=3, column=0, sticky="e")
note_entry = tk.Entry(frame)
note_entry.grid(row=3, column=1, pady=2)

tk.Button(frame, text="Add Expense", command=add_expense_gui, bg="#4CAF50", fg="white").grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")
tk.Button(frame, text="Delete Selected", command=delete_selected, bg="#f44336", fg="white").grid(row=5, column=0, columnspan=2, pady=5, sticky="ew")
tk.Button(frame, text="Export to CSV/Excel", command=export_to_csv).grid(row=6, column=0, columnspan=2, pady=5, sticky="ew")
tk.Button(frame, text="Show Summary", command=show_summary).grid(row=7, column=0, columnspan=2, pady=5, sticky="ew")

tree = ttk.Treeview(root, columns=("Date", "Category", "Amount", "Note"), show="headings")
tree.heading("Date", text="Date")
tree.heading("Category", text="Category")
tree.heading("Amount", text="Amount")
tree.heading("Note", text="Note")
tree.pack(padx=10, pady=10, fill="both", expand=True)

refresh_tree()
root.mainloop()

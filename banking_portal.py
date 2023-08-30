import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create SQLite database and tables
conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

def create_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS accounts (account_number TEXT PRIMARY KEY, balance REAL)")

def create_transactions_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS transactions "
                    "(id INTEGER PRIMARY KEY, account_number TEXT, transaction_type TEXT, amount REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")

create_table()
create_transactions_table()

# GUI Setup
root = tk.Tk()
root.title("Banking App")

label = tk.Label(root, text="Banking App", font=("Helvetica", 16))
label.pack(pady=20)

account_label = tk.Label(root, text="Account Number:")
account_label.pack()
account_entry = tk.Entry(root)
account_entry.pack()

# Functions
def create_account():
    account_number = account_entry.get()
    cursor.execute("INSERT INTO accounts (account_number, balance) VALUES (?, 0.0)", (account_number,))
    conn.commit()
    messagebox.showinfo("Success", "Account created successfully")

def check_balance():
    account_number = account_entry.get()
    cursor.execute("SELECT balance FROM accounts WHERE account_number=?", (account_number,))
    result = cursor.fetchone()
    if result:
        messagebox.showinfo("Balance", f"Account Balance: ${result[0]:.2f}")
    else:
        messagebox.showerror("Error", "Account not found")

def deposit():
    account_number = account_entry.get()
    amount = float(simpledialog.askstring("Deposit", "Enter amount to deposit:"))
    cursor.execute("UPDATE accounts SET balance=balance+? WHERE account_number=?", (amount, account_number))
    conn.commit()
    record_transaction(account_number, "Deposit", amount)
    messagebox.showinfo("Success", f"${amount:.2f} deposited successfully")

def withdraw():
    account_number = account_entry.get()
    amount = float(simpledialog.askstring("Withdraw", "Enter amount to withdraw:"))
    cursor.execute("SELECT balance FROM accounts WHERE account_number=?", (account_number,))
    result = cursor.fetchone()
    if result and result[0] >= amount:
        cursor.execute("UPDATE accounts SET balance=balance-? WHERE account_number=?", (amount, account_number))
        conn.commit()
        record_transaction(account_number, "Withdrawal", amount)
        messagebox.showinfo("Success", f"${amount:.2f} withdrawn successfully")
    else:
        messagebox.showerror("Error", "Insufficient balance or account not found")

def transfer_funds():
    sender_account = account_entry.get()
    receiver_account = simpledialog.askstring("Transfer Funds", "Enter receiver's account number:")
    amount = float(simpledialog.askstring("Transfer Funds", "Enter amount to transfer:"))

    cursor.execute("SELECT balance FROM accounts WHERE account_number=?", (sender_account,))
    sender_balance = cursor.fetchone()
    cursor.execute("SELECT balance FROM accounts WHERE account_number=?", (receiver_account,))
    receiver_balance = cursor.fetchone()

    if sender_balance and receiver_balance and sender_balance[0] >= amount:
        cursor.execute("UPDATE accounts SET balance=balance-? WHERE account_number=?", (amount, sender_account))
        cursor.execute("UPDATE accounts SET balance=balance+? WHERE account_number=?", (amount, receiver_account))
        conn.commit()
        record_transaction(sender_account, "Transfer", amount)
        record_transaction(receiver_account, "Transfer", amount)
        messagebox.showinfo("Success", f"${amount:.2f} transferred successfully")
    else:
        messagebox.showerror("Error", "Transfer failed. Check account balances or account numbers.")

def pay_bill():
    account_number = account_entry.get()
    bill_amount = float(simpledialog.askstring("Pay Bill", "Enter bill amount:"))

    cursor.execute("SELECT balance FROM accounts WHERE account_number=?", (account_number,))
    account_balance = cursor.fetchone()

    if account_balance and account_balance[0] >= bill_amount:
        cursor.execute("UPDATE accounts SET balance=balance-? WHERE account_number=?", (bill_amount, account_number))
        conn.commit()
        record_transaction(account_number, "Bill Payment", bill_amount)
        messagebox.showinfo("Success", f"${bill_amount:.2f} paid successfully")
    else:
        messagebox.showerror("Error", "Payment failed. Check account balance or account number.")

def record_transaction(account_number, transaction_type, amount):
    cursor.execute("INSERT INTO transactions (account_number, transaction_type, amount) VALUES (?, ?, ?)",
                    (account_number, transaction_type, amount))
    conn.commit()

def view_history():
    account_number = account_entry.get()
    cursor.execute("SELECT transaction_type, amount, timestamp FROM transactions WHERE account_number=?", (account_number,))
    transactions = cursor.fetchall()

    if transactions:
        history_window = tk.Toplevel(root)
        history_window.title("Transaction History")

        history_label = tk.Label(history_window, text=f"Transaction History for Account {account_number}", font=("Helvetica", 14))
        history_label.pack(pady=20)

        history_text = tk.Text(history_window, height=10, width=40)
        history_text.pack()

        for transaction in transactions:
            transaction_type, amount, timestamp = transaction
            history_text.insert(tk.END, f"{transaction_type}: ${amount:.2f} ({timestamp})\n")
        history_text.config(state=tk.DISABLED)
    else:
        messagebox.showinfo("No Transactions", "No transaction history available for this account.")

def visualize_data():
    account_number = account_entry.get()
    cursor.execute("SELECT timestamp, amount FROM transactions WHERE account_number=?", (account_number,))
    transactions = cursor.fetchall()

    timestamps = [transaction[0] for transaction in transactions]
    amounts = [transaction[1] for transaction in transactions]

    fig, ax = plt.subplots()
    ax.plot(timestamps, amounts, marker='o')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Amount')
    ax.set_title('Account Balance History')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

def manage_accounts():
    # Implement account management functionality here
    pass

# GUI Buttons
create_button = tk.Button(root, text="Create Account", command=create_account)
create_button.pack()

balance_button = tk.Button(root, text="Check Balance", command=check_balance)
balance_button.pack(pady=10)

deposit_button = tk.Button(root, text="Deposit", command=deposit)
deposit_button.pack()

withdraw_button = tk.Button(root, text="Withdraw", command=withdraw)
withdraw_button.pack()

transfer_button = tk.Button(root, text="Transfer Funds", command=transfer_funds)
transfer_button.pack()

bill_button = tk.Button(root, text="Pay Bill", command=pay_bill)
bill_button.pack()

history_button = tk.Button(root, text="View Transaction History", command=view_history)
history_button.pack()

visualization_button = tk.Button(root, text="View Balance Chart", command=visualize_data)
visualization_button.pack()

manage_button = tk.Button(root, text="Manage Accounts", command=manage_accounts)
manage_button.pack(pady=20)

root.mainloop()

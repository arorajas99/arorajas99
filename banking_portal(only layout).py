import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
root.title("Banking App")

def create_account():
    account_number = account_entry.get()
    messagebox.showinfo("Success", f"Account {account_number} created successfully")

def check_balance():
    account_number = account_entry.get()
    messagebox.showinfo("Balance", f"Account Balance: $1000.00")  # Placeholder balance

def deposit():
    account_number = account_entry.get()
    amount = float(simpledialog.askstring("Deposit", "Enter amount to deposit:"))
    messagebox.showinfo("Success", f"${amount:.2f} deposited successfully")

def withdraw():
    account_number = account_entry.get()
    amount = float(simpledialog.askstring("Withdraw", "Enter amount to withdraw:"))
    messagebox.showinfo("Success", f"${amount:.2f} withdrawn successfully")

def transfer_funds():
    sender_account = account_entry.get()
    receiver_account = simpledialog.askstring("Transfer Funds", "Enter receiver's account number:")
    amount = float(simpledialog.askstring("Transfer Funds", "Enter amount to transfer:"))
    messagebox.showinfo("Success", f"${amount:.2f} transferred successfully")

def pay_bill():
    account_number = account_entry.get()
    bill_amount = float(simpledialog.askstring("Pay Bill", "Enter bill amount:"))
    messagebox.showinfo("Success", f"${bill_amount:.2f} paid successfully")

def view_history():
    account_number = account_entry.get()
    history_text.delete("1.0", tk.END)
    history_text.insert(tk.END, "Transaction history:\n")
    history_text.insert(tk.END, "Deposit: $100.00\n")  # Placeholder transactions
    history_text.insert(tk.END, "Withdrawal: $50.00\n")

def visualize_data():
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2, 3, 4], [0, 2, 1, 3, 4], marker='o')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_title('Sample Chart')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

# GUI Components
label = tk.Label(root, text="Banking App", font=("Helvetica", 16))
label.pack(pady=20)

account_label = tk.Label(root, text="Account Number:")
account_label.pack()
account_entry = tk.Entry(root)
account_entry.pack()

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

history_text = tk.Text(root, height=10, width=40)
history_text.pack()

root.mainloop()

# PyBank ATM
# By Bhavya Chourey

import tkinter as tk
from tkinter import messagebox
import os

# globals
users = []
current_user = None
current_index = -1

# users.txt in the same folder as this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.txt")


def ensure_users_file():
    """Create users.txt with 50 users if it does not exist or is empty."""
    if (not os.path.exists(USERS_FILE)) or os.path.getsize(USERS_FILE) == 0:
        with open(USERS_FILE, "w") as f:
            base_balance = 5000
            for i in range(1, 51):
                name = f"User{i}"
                pin = str(1000 + i)       # 1001, 1002, ...
                unique_balance = base_balance + i * 73
                f.write(f"{name},{pin},{unique_balance}\n")


def load_users():
    """Load users from users.txt into the list."""
    global users
    ensure_users_file()

    users = []
    with open(USERS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) != 3:
                continue
            name, pin, bal = parts
            users.append({
                "name": name,
                "pin": pin,
                "balance": int(bal),
                "history": []
            })


def save_users():
    """Write current user data back to users.txt."""
    with open(USERS_FILE, "w") as f:
        for u in users:
            f.write(f"{u['name']},{u['pin']},{u['balance']}\n")


def do_login():
    """Handle login button click."""
    global current_user, current_index
    pin = entry_pin.get().strip()
    if not pin:
        messagebox.showwarning("PIN", "Please enter your PIN.")
        return

    found = False
    for i, u in enumerate(users):
        if u["pin"] == pin:
            current_user = u
            current_index = i
            found = True
            break

    if not found:
        messagebox.showerror("Login Failed", "Invalid PIN.")
        return

    entry_pin.delete(0, tk.END)
    label_welcome.config(text=f"Welcome, {current_user['name']}")
    update_balance_label()
    frame_login.pack_forget()
    frame_main.pack(padx=20, pady=20)


def do_logout():
    """Logout current user and show login screen again."""
    global current_user, current_index
    current_user = None
    current_index = -1
    frame_main.pack_forget()
    frame_login.pack(padx=20, pady=40)


def update_balance_label():
    """Refresh the balance label on the main screen."""
    if current_user is not None:
        label_balance.config(text=f"₹ {current_user['balance']}")
    else:
        label_balance.config(text="₹ 0")


def btn_check_balance():
    if current_user is None:
        messagebox.showerror("Error", "No user logged in.")
        return
    update_balance_label()
    messagebox.showinfo("Balance", f"Your balance is ₹{current_user['balance']}")


def btn_deposit():
    if current_user is None:
        messagebox.showerror("Error", "No user logged in.")
        return
    amt_str = entry_amount.get().strip()
    if not amt_str.isdigit():
        messagebox.showerror("Amount", "Please enter a valid positive number.")
        return
    amt = int(amt_str)
    if amt <= 0:
        messagebox.showerror("Amount", "Amount must be greater than 0.")
        return
    current_user["balance"] += amt
    current_user["history"].append(f"Deposit +₹{amt}")
    users[current_index] = current_user
    save_users()
    update_balance_label()
    messagebox.showinfo("Deposit", f"₹{amt} deposited successfully.")
    entry_amount.delete(0, tk.END)


def btn_withdraw():
    if current_user is None:
        messagebox.showerror("Error", "No user logged in.")
        return
    amt_str = entry_amount.get().strip()
    if not amt_str.isdigit():
        messagebox.showerror("Amount", "Please enter a valid positive number.")
        return
    amt = int(amt_str)
    if amt <= 0:
        messagebox.showerror("Amount", "Amount must be greater than 0.")
        return
    if amt > current_user["balance"]:
        messagebox.showerror("Amount", "Insufficient balance.")
        return
    current_user["balance"] -= amt
    current_user["history"].append(f"Withdraw -₹{amt}")
    users[current_index] = current_user
    save_users()
    update_balance_label()
    messagebox.showinfo("Withdraw", f"₹{amt} withdrawn successfully.")
    entry_amount.delete(0, tk.END)


def btn_statement():
    if current_user is None:
        messagebox.showerror("Error", "No user logged in.")
        return
    if not current_user["history"]:
        messagebox.showinfo("Mini Statement", "No transactions yet.")
        return
    lines = current_user["history"][-5:]
    msg = "\n".join(lines)
    messagebox.showinfo("Mini Statement", msg)


def btn_change_pin():
    if current_user is None:
        messagebox.showerror("Error", "No user logged in.")
        return
    old = entry_old_pin.get().strip()
    new1 = entry_new_pin.get().strip()
    new2 = entry_confirm_pin.get().strip()

    if old != current_user["pin"]:
        messagebox.showerror("PIN", "Current PIN is incorrect.")
        return
    if new1 != new2:
        messagebox.showerror("PIN", "New PINs do not match.")
        return
    if len(new1) != 4 or not new1.isdigit():
        messagebox.showerror("PIN", "New PIN must be exactly 4 digits.")
        return
    current_user["pin"] = new1
    users[current_index] = current_user
    save_users()
    messagebox.showinfo("PIN", "PIN changed successfully.")
    entry_old_pin.delete(0, tk.END)
    entry_new_pin.delete(0, tk.END)
    entry_confirm_pin.delete(0, tk.END)


def do_exit():
    root.destroy()


# --------- BUILD GUI ---------

load_users()

root = tk.Tk()
root.title("PyBank ATM - GUI Version")
root.configure(bg="#0f172a")  # dark background
root.resizable(False, False)

# Header
frame_header = tk.Frame(root, bg="#0f172a")
frame_header.pack(fill="x", pady=(10, 0))

label_app = tk.Label(
    frame_header,
    text="💳 PyBank ATM System",
    font=("Segoe UI", 18, "bold"),
    fg="#e5e7eb",
    bg="#0f172a"
)
label_app.pack()

subtitle = tk.Label(
    frame_header,
    text="Secure • Simple • Student Project",
    font=("Segoe UI", 10),
    fg="#9ca3af",
    bg="#0f172a"
)
subtitle.pack(pady=(0, 10))

# Login frame
frame_login = tk.Frame(root, padx=30, pady=30, bg="#1f2937", bd=0, relief="ridge")
frame_login.pack(padx=20, pady=40)

label_title = tk.Label(
    frame_login,
    text="Login to your Account",
    font=("Segoe UI", 14, "bold"),
    fg="#f9fafb",
    bg="#1f2937"
)
label_title.pack(pady=(0, 15))

label_pin_login = tk.Label(
    frame_login,
    text="Enter 4-digit PIN",
    font=("Segoe UI", 10),
    fg="#e5e7eb",
    bg="#1f2937"
)
label_pin_login.pack()

entry_pin = tk.Entry(frame_login, show="*", width=20, font=("Consolas", 11), justify="center")
entry_pin.pack(pady=8, ipady=3)

btn_login = tk.Button(
    frame_login,
    text="Login",
    width=18,
    bg="#10b981",
    fg="white",
    activebackground="#059669",
    activeforeground="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    command=do_login
)
btn_login.pack(pady=10)

hint = tk.Label(
    frame_login,
    text="Example PINs: 1001 - 1050",
    font=("Segoe UI", 9),
    fg="#9ca3af",
    bg="#1f2937"
)
hint.pack(pady=(5, 0))

# Main ATM frame (hidden until login)
frame_main = tk.Frame(root, padx=20, pady=20, bg="#0f172a")

# Top card: welcome + balance
card_top = tk.Frame(frame_main, bg="#111827", padx=15, pady=15)
card_top.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))

label_welcome = tk.Label(
    card_top,
    text="Welcome,",
    font=("Segoe UI", 14, "bold"),
    fg="#e5e7eb",
    bg="#111827"
)
label_welcome.grid(row=0, column=0, sticky="w")

tk.Label(
    card_top,
    text="Current Balance",
    font=("Segoe UI", 9),
    fg="#9ca3af",
    bg="#111827"
).grid(row=1, column=0, sticky="w", pady=(8, 0))

label_balance = tk.Label(
    card_top,
    text="₹ 0",
    font=("Segoe UI", 16, "bold"),
    fg="#22c55e",
    bg="#111827"
)
label_balance.grid(row=2, column=0, sticky="w")

# Amount card
card_amount = tk.Frame(frame_main, bg="#111827", padx=15, pady=15)
card_amount.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))

tk.Label(
    card_amount,
    text="Amount (₹):",
    font=("Segoe UI", 10),
    fg="#e5e7eb",
    bg="#111827"
).grid(row=0, column=0, sticky="w")

entry_amount = tk.Entry(card_amount, width=18, font=("Consolas", 11))
entry_amount.grid(row=1, column=0, pady=5, sticky="w", ipady=2)

# Buttons section
card_buttons = tk.Frame(frame_main, bg="#0f172a")
card_buttons.grid(row=2, column=0, columnspan=2, pady=(0, 10))

btn_check = tk.Button(
    card_buttons,
    text="Check Balance",
    width=15,
    bg="#3b82f6",
    fg="white",
    activebackground="#2563eb",
    activeforeground="white",
    font=("Segoe UI", 10),
    relief="flat",
    command=btn_check_balance
)
btn_check.grid(row=0, column=0, padx=5, pady=5)

btn_depo = tk.Button(
    card_buttons,
    text="Deposit",
    width=15,
    bg="#10b981",
    fg="white",
    activebackground="#059669",
    activeforeground="white",
    font=("Segoe UI", 10),
    relief="flat",
    command=btn_deposit
)
btn_depo.grid(row=0, column=1, padx=5, pady=5)

btn_with = tk.Button(
    card_buttons,
    text="Withdraw",
    width=15,
    bg="#f97316",
    fg="white",
    activebackground="#ea580c",
    activeforeground="white",
    font=("Segoe UI", 10),
    relief="flat",
    command=btn_withdraw
)
btn_with.grid(row=1, column=0, padx=5, pady=5)

btn_stmt = tk.Button(
    card_buttons,
    text="Mini Statement",
    width=15,
    bg="#6b7280",
    fg="white",
    activebackground="#4b5563",
    activeforeground="white",
    font=("Segoe UI", 10),
    relief="flat",
    command=btn_statement
)
btn_stmt.grid(row=1, column=1, padx=5, pady=5)

# Change PIN card
card_pin = tk.Frame(frame_main, bg="#111827", padx=15, pady=15)
card_pin.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(5, 10))

tk.Label(
    card_pin,
    text="Change PIN",
    font=("Segoe UI", 11, "bold"),
    fg="#e5e7eb",
    bg="#111827"
).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))

tk.Label(
    card_pin,
    text="Old PIN:",
    font=("Segoe UI", 9),
    fg="#9ca3af",
    bg="#111827"
).grid(row=1, column=0, sticky="e", padx=(0, 5))
entry_old_pin = tk.Entry(card_pin, show="*", width=10, font=("Consolas", 10))
entry_old_pin.grid(row=1, column=1, sticky="w", pady=2)

tk.Label(
    card_pin,
    text="New PIN:",
    font=("Segoe UI", 9),
    fg="#9ca3af",
    bg="#111827"
).grid(row=2, column=0, sticky="e", padx=(0, 5))
entry_new_pin = tk.Entry(card_pin, show="*", width=10, font=("Consolas", 10))
entry_new_pin.grid(row=2, column=1, sticky="w", pady=2)

tk.Label(
    card_pin,
    text="Confirm:",
    font=("Segoe UI", 9),
    fg="#9ca3af",
    bg="#111827"
).grid(row=3, column=0, sticky="e", padx=(0, 5))
entry_confirm_pin = tk.Entry(card_pin, show="*", width=10, font=("Consolas", 10))
entry_confirm_pin.grid(row=3, column=1, sticky="w", pady=2)

btn_change = tk.Button(
    card_pin,
    text="Update PIN",
    width=15,
    bg="#facc15",
    fg="#111827",
    activebackground="#eab308",
    activeforeground="#111827",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    command=btn_change_pin
)
btn_change.grid(row=4, column=0, columnspan=2, pady=(8, 0))

# Bottom buttons
card_bottom = tk.Frame(frame_main, bg="#0f172a")
card_bottom.grid(row=4, column=0, columnspan=2, pady=(5, 0))

btn_logout = tk.Button(
    card_bottom,
    text="Logout",
    width=10,
    bg="#ef4444",
    fg="white",
    activebackground="#dc2626",
    activeforeground="white",
    relief="flat",
    font=("Segoe UI", 9),
    command=do_logout
)
btn_logout.grid(row=0, column=0, padx=5, pady=5)

btn_exit = tk.Button(
    card_bottom,
    text="Exit",
    width=10,
    bg="#374151",
    fg="white",
    activebackground="#1f2937",
    activeforeground="white",
    relief="flat",
    font=("Segoe UI", 9),
    command=do_exit
)
btn_exit.grid(row=0, column=1, padx=5, pady=5)

root.mainloop()

# 💳 PyBank ATM System

A secure and simple ATM simulation built using Python's `tkinter` library for the graphical user interface (GUI). This project is designed as a student exercise to demonstrate file handling, state management, and basic GUI development in Python.

## ✨ Features

* **GUI Interface:** User-friendly graphical interface built with `tkinter`.
* **Persistent Data:** User accounts (name, PIN, balance) are stored in and loaded from a local file (`users.txt`).
* **Initial Setup:** Automatically generates 50 dummy user accounts if `users.txt` is missing or empty.
* **User Authentication:** Secure login using a 4-digit PIN.
* **Core ATM Operations:**
    * **Check Balance:** View the current account balance.
    * **Deposit:** Add funds to the account.
    * **Withdraw:** Remove funds from the account (with insufficient balance check).
    * **Mini Statement:** View the last 5 transactions (deposits/withdrawals).
* **Security:** Option to **Change PIN** with validation for old PIN and new PIN match/format.
* **Logout/Exit:** Functions to log out and return to the login screen, or exit the application completely.

## ⚙️ Setup and Installation

Follow these steps to get a local copy of the project up and running.

### Prerequisites

You need **Python 3.x** installed on your system. The `tkinter` library is generally included with standard Python installations.

### 1. Download the Code

Clone the repository or download the source code files (`pybank_atm.py` and potentially `users.txt` if provided) into a folder on your computer.

### 2. Run the Application

Navigate to the project directory in your terminal or command prompt and run the Python script:

```bash
python pybank_atm.py

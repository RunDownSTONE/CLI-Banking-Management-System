# CLI-Banking-Management-System
A CLI (Command Line Interface)-based Banking Management System built in Python using object-oriented programming. The system supports account creation, PIN-based authentication, deposits, withdrawals, transaction history with timestamps, and persistent data storage using JSON.

# 🏦 CLI Banking Management System (Python)

A command-line based Banking Management System built using Python.  
This project demonstrates object-oriented programming, file handling, authentication, and data persistence using JSON.

---

## 🚀 Features

- Create new bank accounts
- Secure PIN-based authentication (4-digit PIN)
- Deposit money into accounts
- Withdraw money with balance validation
- Check account balance
- View account details
- View transaction history with timestamps
- Persistent data storage using JSON (data remains after program restart)

---

## 🛠️ Technologies Used

- Python 3
- Object-Oriented Programming (OOP)
- JSON (data storage)
- File Handling
- datetime module

---

## 📁 Project Structure

```

bank_system.py     → Main program (contains all classes and CLI interface)
accounts.json      → Auto-generated file for storing account data

````

---

## ▶️ How to Run

1. Clone the repository:
```bash
git clone https://github.com/your-username/cli-banking-management-system.git
````

2. Navigate to the project directory:

```bash
cd cli-banking-management-system
```

3. Run the program:

```bash
python bank_system.py
```

---

## 🔐 Authentication System

* Each account is protected with a **4-digit PIN**
* PIN verification is required for:

  * Deposit
  * Withdrawal
  * Balance check
  * Account details
  * Transaction history

---

## 💾 Data Storage

* Uses a local JSON file (`accounts.json`)
* Automatically created and updated
* Stores:

  * Account information
  * Balance
  * Transaction history with timestamps

---

## 📊 Example Transaction Format

```
2026-05-04 15:30:12 | Deposit         | Amount:    500 | Balance: 1500
```

---

## 🎯 What I Learned

* Object-Oriented Programming in Python
* Designing real-world systems using classes
* File handling and JSON-based persistence
* Input validation and error handling
* Building CLI-based applications
* Structuring clean and maintainable code

---

## 📌 Future Improvements

* Add PIN attempt limit (security enhancement)
* Encrypt PIN storage for better security
* Add account deletion feature
* Convert CLI project into a GUI application
* Replace JSON with a database system (SQLite/MySQL)

---

## 👨‍💻 Author

Built by a Computer Science student exploring backend systems, programming fundamentals, and real-world application design.

---

## 📜 License

This project is for educational purposes only.


Just tell me 👍
```

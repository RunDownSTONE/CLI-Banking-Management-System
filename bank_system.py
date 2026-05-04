import json
import os
from datetime import datetime

class Account:
    def __init__(self, name, account_number, pin, balance):
        self.name = name
        self.account_number = account_number
        self.pin = pin
        self.balance = balance
        self.transaction_history = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        self._record_transaction("Deposit", amount)

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self._record_transaction("Withdrawal", amount)

    def _record_transaction(self, activity, amount):
        self.transaction_history.append({
            "type": activity,
            "amount": amount,
            "balance": self.balance,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

    def to_dict(self):
        return {
            "name": self.name,
            "account_number": self.account_number,
            "pin": self.pin,
            "balance": self.balance,
            "transaction_history": self.transaction_history,
        }

    @staticmethod
    def from_dict(data):
        account = Account(
            data["name"],
            data["account_number"],
            data.get("pin", "0000"),  
            data["balance"],
        )
        account.transaction_history = data.get("transaction_history", [])
        return account

class Bank:
    def __init__(self, filename="accounts.json"):
        self.filename = filename
        self.accounts = {}
        self.load_accounts()

    def load_accounts(self):
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
            if isinstance(data, list):
                for account_data in data:
                    account = Account.from_dict(account_data)
                    self.accounts[account.account_number] = account
            else:
                for account_number, account_data in data.items():
                    self.accounts[account_number] = Account.from_dict(account_data)
        except (json.JSONDecodeError, TypeError):
            print("Warning: account data file is corrupted. Starting with no accounts.")
            self.accounts = {}

    def save_accounts(self):
        data = {number: account.to_dict() for number, account in self.accounts.items()}
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    def generate_account_number(self):
        if not self.accounts:
            return "1001"
        numbers = [int(num) for num in self.accounts.keys() if num.isdigit()]
        return str(max(numbers, default=1000) + 1)

    def create_account(self, name, pin, initial_balance):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        if len(pin) != 4 or not pin.isdigit():
            raise ValueError("PIN must be a 4-digit number")
        account_number = self.generate_account_number()
        account = Account(name, account_number, pin, initial_balance)
        account._record_transaction("Account opened", initial_balance)
        self.accounts[account_number] = account
        self.save_accounts()
        return account

    def get_account(self, account_number):
        account = self.accounts.get(account_number)
        if not account:
            raise KeyError("Account not found")
        return account

    def verify_pin(self, account, pin):
        if account.pin != pin:
            raise ValueError("Incorrect PIN")

    def deposit_to_account(self, account_number, amount, pin):
        account = self.get_account(account_number)
        self.verify_pin(account, pin)
        account.deposit(amount)
        self.save_accounts()
        return account

    def withdraw_from_account(self, account_number, amount, pin):
        account = self.get_account(account_number)
        self.verify_pin(account, pin)
        account.withdraw(amount)
        self.save_accounts()
        return account

    def account_balance(self, account_number, pin):
        account = self.get_account(account_number)
        self.verify_pin(account, pin)
        return account.balance

    def account_details(self, account_number, pin):
        account = self.get_account(account_number)
        self.verify_pin(account, pin)
        return account.to_dict()

    def transaction_history(self, account_number, pin):
        account = self.get_account(account_number)
        self.verify_pin(account, pin)
        return account.transaction_history

def prompt_non_empty(prompt_text):
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("Input cannot be empty")

def prompt_positive_number(prompt_text):
    while True:
        value = input(prompt_text).strip()
        if not value:
            print("Input cannot be empty")
            continue
        if not value.isdigit():
            print("Enter a valid positive number")
            continue
        return int(value)

def prompt_pin(prompt_text):
    while True:
        pin = input(prompt_text).strip()
        if len(pin) == 4 and pin.isdigit():
            return pin
        print("Enter a 4-digit PIN")

def print_account_summary(details):
    print("\nAccount Details")
    print("----------------")
    print(f"Owner: {details['name']}")
    print(f"Account Number: {details['account_number']}")
    print(f"Balance: {details['balance']}")
    print("----------------")

def print_transaction_history(history):
    if not history:
        print("No transactions recorded yet")
        return
    print("\nTransaction History")
    print("---------------------")
    for item in history:
        print(f"{item['time']} | {item['type']:15} | Amount: {item['amount']:>8} | Balance: {item['balance']}")

def main():
    bank = Bank()
    while True:
        print("\nBanking Management System")
        print("1. Create new account")
        print("2. Deposit money")
        print("3. Withdraw money")
        print("4. Check account balance")
        print("5. View account details")
        print("6. View transaction history")
        print("7. Exit")
        choice = input("Enter your choice (1-7): ").strip()

        try:
            if choice == "1":
                name = prompt_non_empty("Enter account owner name: ")
                pin = prompt_pin("Create a 4-digit PIN: ")
                initial_balance = prompt_positive_number("Enter initial balance: ")
                account = bank.create_account(name, pin, initial_balance)
                print(f"Account created successfully. Account Number: {account.account_number}")
            elif choice == "2":
                account_number = prompt_non_empty("Enter account number: ")
                pin = prompt_pin("Enter your 4-digit PIN: ")
                amount = prompt_positive_number("Enter deposit amount: ")
                account = bank.deposit_to_account(account_number, amount, pin)
                print(f"Deposit successful. New balance: {account.balance}")
            elif choice == "3":
                account_number = prompt_non_empty("Enter account number: ")
                pin = prompt_pin("Enter your 4-digit PIN: ")
                amount = prompt_positive_number("Enter withdrawal amount: ")
                account = bank.withdraw_from_account(account_number, amount, pin)
                print(f"Withdrawal successful. Remaining balance: {account.balance}")
            elif choice == "4":
                account_number = prompt_non_empty("Enter account number: ")
                pin = prompt_pin("Enter your 4-digit PIN: ")
                balance = bank.account_balance(account_number, pin)
                print(f"Current balance: {balance}")
            elif choice == "5":
                account_number = prompt_non_empty("Enter account number: ")
                pin = prompt_pin("Enter your 4-digit PIN: ")
                details = bank.account_details(account_number, pin)
                print_account_summary(details)
                print_transaction_history(details["transaction_history"])
            elif choice == "6":
                account_number = prompt_non_empty("Enter account number: ")
                pin = prompt_pin("Enter your 4-digit PIN: ")
                history = bank.transaction_history(account_number, pin)
                print_transaction_history(history)
            elif choice == "7":
                print("Thank you for using the banking system. Goodbye!")
                break
            else:
                print("Please choose a valid option from 1 to 7")
        except ValueError as error:
            print(f"Error: {error}")
        except KeyError:
            print("Error: Account number not found")

if __name__ == "__main__":
    main()

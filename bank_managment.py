
import datetime


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Customer(Person):
    def __init__(self, name, age, customer_id):
        super().__init__(name, age)
        self.customer_id = customer_id


class BankAccount:
    def __init__(self, account_number, account_holder, balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance
        self.creation_date = datetime.datetime.now()
        self.transaction_history = []

    def deposit(self, amount):
        self.balance += amount
        self.add_transaction("Deposit", amount, self.balance)
        self.print_transactions()

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.add_transaction("Withdrawal", -amount, self.balance)
            self.print_transactions()
        else:
            print("Insufficient funds")

    def add_transaction(self, transaction, amount, balance):
        date = datetime.datetime.now()
        self.transaction_history.append((date, transaction, amount, balance))

    def print_transactions(self):
        print(f"Transactions for Account {self.account_number}:")
        for date, transaction, amount, balance in self.transaction_history[-5:]:
            print(f"Date: {date}, Transaction: {transaction}, Amount: {amount}, Balance: {balance}")


class ShortTermDepositAccount(BankAccount):
    def __init__(self, account_number, account_holder, balance=0):
        super().__init__(account_number, account_holder, balance)
        self.interest_date = None

    def calculate_monthly_interest(self):
        current_date = datetime.datetime.now()
        last_month_date = current_date.replace(month=current_date.month - 1)
        if not self.interest_date or last_month_date > self.interest_date:
            monthly_interest = self.balance * 0.5 / 12
            self.balance += monthly_interest
            self.interest_date = current_date
            self.add_transaction("Monthly Interest", monthly_interest, self.balance)
            print(f"Calculated monthly interest for Account {self.account_number}: {monthly_interest}")


class LongTermDepositAccount(BankAccount):
    def withdraw(self, amount):
        print("Withdrawal not allowed for long-term deposit accounts")

    def __init__(self, account_number, account_holder, balance=0):
        super().__init__(account_number, account_holder, balance)
        self.interest_date = None

    def calculate_annual_interest(self):
        current_date = datetime.datetime.now()
        last_year_date = current_date.replace(year=current_date.year - 1)
        if not self.interest_date or last_year_date > self.interest_date:
            annual_interest = self.balance * 0.20
            self.balance += annual_interest
            self.interest_date = current_date
            self.add_transaction("Annual Interest", annual_interest, self.balance)
            print(f"Calculated annual interest for Account {self.account_number}: {annual_interest}")


class Bank:
    def __init__(self):
        self.accounts = []
        self.customers = []

    def create_account(self, account_type, account_number, account_holder, initial_balance=0):
        if account_type == "short_term":
            account = ShortTermDepositAccount(account_number, account_holder, initial_balance)
        elif account_type == "long_term":
            account = LongTermDepositAccount(account_number, account_holder, initial_balance)
        else:
            print("Invalid account type")
            return
        self.accounts.append(account)
        self.add_customer(account_holder)

    def transfer_money(self, sender_account_number, receiver_account_number, amount):
        sender_account = self.get_account_by_number(sender_account_number)
        receiver_account = self.get_account_by_number(receiver_account_number)
        if not sender_account or not receiver_account:
            print("Invalid account number")
            return
        if amount <= sender_account.balance:
            sender_account.withdraw(amount)
            receiver_account.deposit(amount)
            print(
                f"Transferred {amount} from Account {sender_account.account_number} to Account {receiver_account.account_number}")
        else:
            print("Insufficient funds")

    def get_account_by_number(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        return None

    def add_customer(self, customer):
        self.customers.append(customer)

    def print_all_customers(self):
        for customer in self.customers:
            print(f"Customer: {customer.name}, Age: {customer.age}, Customer ID: {customer.customer_id}")
            print("Accounts:")
            for account in self.accounts:
                if account.account_holder == customer:
                    print(f"Account Number: {account.account_number}, Balance: {'{:.2f}'.format(account.balance)}")
            print()

    def calculate_interests(self):
        for account in self.accounts:
            if isinstance(account, ShortTermDepositAccount):
                account.calculate_monthly_interest()
            elif isinstance(account, LongTermDepositAccount):
                account.calculate_annual_interest()


bank = Bank()

# Create customers
customer1 = Customer("Kamyar", 22, "CUST_1")
customer2 = Customer("Abolfazl", 30, "CUST_2")

# Create accounts
bank.create_account("short_term", "ACC_1", customer1, 10500)
bank.create_account("long_term", "ACC_2", customer2, 2000)

# Print all customers and their initial balances
print('List of bank Customers and their initial balances:')
bank.print_all_customers()
print('---------------------------')

# Transfer money between accounts
bank.transfer_money("ACC_1", "ACC_2", 500)
print('---------------------------')

# Calculate interests
print('Interests after 1 month for short-term accounts and 1 year for long-term accounts:')
bank.calculate_interests()
print('---------------------------')

bank.print_all_customers()
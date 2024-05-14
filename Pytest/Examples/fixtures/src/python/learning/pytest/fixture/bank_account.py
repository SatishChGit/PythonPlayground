class BankAccount:
    def __init__(self, acc_no, bal=0):
        self.acc_no = acc_no
        self.bal = bal

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.bal = self.bal + amount

    def withdrawl(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawl amount must be positive")
        if amount > self.bal:
            raise ValueError("Insufficient funds")
        self.bal = self.bal - amount

    def get_balance(self):
        return self.bal


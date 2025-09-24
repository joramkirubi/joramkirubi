from abc import ABC, abstractmethod

# --------------------------
# BASE CLASS
# --------------------------
class BankAccount(ABC):
    def __init__(self, owner, balance=0):
        """
        Initialize a bank account.
        """
        self.owner = owner
        self.__balance = balance

    @property
    def balance(self):
        """Read-only property for balance."""
        return self.__balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"✅ Deposited {amount}. New balance = {self.__balance}")
        else:
            print("❌ Deposit must be positive.")

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"✅ Withdrew {amount}. New balance = {self.__balance}")
        else:
            print("❌ Invalid withdrawal amount or insufficient funds.")

    def transfer(self, amount, other_account):
        """
        Transfer money to another account.
        """
        if isinstance(other_account, BankAccount):
            if 0 < amount <= self.__balance:
                self.withdraw(amount)
                other_account.deposit(amount)
                print(f"🔁 Transferred {amount} from {self.owner} to {other_account.owner}")
            else:
                print("❌ Transfer failed: insufficient funds or invalid amount.")
        else:
            print("❌ Transfer failed: target is not a BankAccount.")

    @abstractmethod
    def account_type(self):
        """Each account type must implement this."""
        pass

    def __str__(self):
        return f"{self.account_type()} Account | Owner: {self.owner} | Balance: {self.__balance}"


# --------------------------
# CHILD CLASSES
# --------------------------
class SavingsAccount(BankAccount):
    interest_rate = 0.03  # 3% annual interest

    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.deposit(interest)
        print(f"💰 Applied interest: {interest}")

    def account_type(self):
        return "Savings"


class CheckingAccount(BankAccount):
    transaction_fee = 2  # $2 fee per withdrawal

    def withdraw(self, amount):
        total_amount = amount + self.transaction_fee
        if 0 < total_amount <= self.balance:
            super().withdraw(total_amount)
            print(f"💸 Transaction fee applied: {self.transaction_fee}")
        else:
            print("❌ Withdrawal failed: insufficient funds including transaction fee.")

    def account_type(self):
        return "Checking"


# --------------------------
# TESTING THE SYSTEM
# --------------------------
if __name__ == "__main__":
    # Create accounts
    savings = SavingsAccount("Alice", 1000)
    checking = CheckingAccount("Bob", 500)

    # Show accounts
    print(savings)
    print(checking)

    # Deposits
    savings.deposit(200)
    checking.deposit(300)

    # Withdrawals
    savings.withdraw(100)
    checking.withdraw(50)

    # Apply interest to savings
    savings.apply_interest()

    # Transfers
    savings.transfer(200, checking)

    # Final balances
    print(savings)
    print(checking)

class CoinSystem:
    def __init__(self, initial_balance=0):
        self.balance = initial_balance  # User starts with 100 coins
    
    def spend(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True  # Transaction successful
        return False  # Not enough coins
    
    def earn(self, amount):
        self.balance += amount
    
    def get_balance(self):
        return self.balance

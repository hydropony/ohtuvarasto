class Warehouse:
    def __init__(self, capacity, initial_balance=0):
        self.capacity = capacity if capacity > 0.0 else 0.0

        if initial_balance < 0.0:
            # invalid, reset to zero
            self.balance = 0.0
        elif initial_balance <= capacity:
            # fits
            self.balance = initial_balance
        else:
            # fill to capacity, excess is lost!
            self.balance = capacity

    # note: property can also be calculated.
    # No separate field needed for available_space etc.
    def available_space(self):
        return self.capacity - self.balance

    def add_to_warehouse(self, amount):
        if amount < 0:
            return
        if amount <= self.available_space():
            self.balance = self.balance + amount
        else:
            self.balance = self.capacity

    def take_from_warehouse(self, amount):
        if amount < 0:
            return 0.0
        if amount > self.balance:
            all_that_can_be_taken = self.balance
            self.balance = 0.0

            return all_that_can_be_taken

        self.balance = self.balance - amount

        return amount

    def __str__(self):
        return f"balance = {self.balance}, space = {self.available_space()}"

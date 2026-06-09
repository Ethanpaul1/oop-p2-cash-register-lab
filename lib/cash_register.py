class CashRegister:
    """
    A cash register that tracks items, totals, discounts, and transaction history.
    """

    def __init__(self, discount=0):
        self._discount = discount
        self.total = 0
        self.items = []
        self.previous_transactions = []

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, value):
        if not isinstance(value, int) or not (0 <= value <= 100):
            print("Not valid discount")
        else:
            self._discount = value

    def add_item(self, title, price, quantity=1):
        """Add item(s) to the register, updating total and item list."""
        self.total += price * quantity
        for _ in range(quantity):
            self.items.append(title)
        self.previous_transactions.append({
            "item": title,
            "price": price,
            "quantity": quantity
        })

    def apply_discount(self):
        """Apply discount % to total. Prints error if discount is 0."""
        if not self._discount:
            print("There is no discount to apply.")
            return
        self.total = self.total * ((100 - self._discount) / 100)
        # Format: no trailing zeros after decimal (800.0 -> "800")
        total_str = f"{self.total:g}"
        print(f"After the discount, the total comes to ${total_str}.")

    def void_last_transaction(self):
        """Subtract the last transaction from the total and remove its items."""
        if not self.previous_transactions:
            return
        last = self.previous_transactions.pop()
        self.total -= last["price"] * last["quantity"]
        for _ in range(last["quantity"]):
            for i in range(len(self.items) - 1, -1, -1):
                if self.items[i] == last["item"]:
                    self.items.pop(i)
                    break
        if not self.previous_transactions:
            self.total = 0.0

class CashRegister:
    """
    A cash register that tracks items, totals, discounts, and transaction history.
    Supports adding items, applying discounts, and voiding the last transaction.
    """

    def __init__(self, discount=0):
        # Optional discount percentage (0-100); defaults to 0 if not provided
        self._discount = discount
        # Running total of all item prices
        self.total = 0
        # Flat list of item names (duplicated for quantity > 1)
        self.items = []
        # History of each transaction as dicts with item, price, quantity
        self.previous_transactions = []

    # --- Discount property with validation ---

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, value):
        # Discount must be an integer between 0 and 100 inclusive
        if not isinstance(value, int) or not (0 <= value <= 100):
            print("Not valid discount")
        else:
            self._discount = value

    # --- Methods ---

    def add_item(self, title, price, quantity=1):
        """
        Add an item to the register.
        - Increases total by price * quantity
        - Appends the item name once per quantity to items list
        - Records the transaction in previous_transactions
        """
        self.total += price * quantity

        # Add the item name once per unit purchased
        for _ in range(quantity):
            self.items.append(title)

        # Record the full transaction for potential voiding
        self.previous_transactions.append({
            "item": title,
            "price": price,
            "quantity": quantity
        })

    def apply_discount(self):
        """
        Apply the discount percentage to the current total.
        Prints an error if there are no transactions to discount.
        """
        if not self.previous_transactions:
            print("There is no discount to apply.")
            return

        # Calculate discounted total and round to 2 decimal places
        self.total = round(self.total * ((100 - self._discount) / 100), 2)
        print(f"After the discount, the total comes to ${self.total:.2f}.")

        # Remove the last transaction record after applying discount
        self.previous_transactions.pop()

    def void_last_transaction(self):
        """
        Remove the last transaction from the register.
        Subtracts its price * quantity from the total.
        Resets total to 0.0 if no transactions remain.
        """
        if not self.previous_transactions:
            return

        last = self.previous_transactions.pop()

        # Subtract the last transaction's cost from the total
        self.total -= last["price"] * last["quantity"]

        # Remove the item entries added by that transaction
        for _ in range(last["quantity"]):
            # Remove last occurrence of the item
            for i in range(len(self.items) - 1, -1, -1):
                if self.items[i] == last["item"]:
                    self.items.pop(i)
                    break

        # Guard against floating-point drift leaving a tiny non-zero value
        if not self.previous_transactions:
            self.total = 0.0
#!/usr/bin/env python3

class CashRegister:
    """Model a checkout register with discounts and voidable transactions."""

    def __init__(self, discount=0):
        self._discount = 0
        self.discount = discount
        self.total = 0
        self.items = []
        self.previous_transactions = []

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, value):
        if type(value) is not int or value < 0 or value > 100:
            print("Not valid discount")
            return

        self._discount = value

    def add_item(self, item, price, quantity=1):
        # Store one list entry per item so multiples can be displayed and voided.
        for _ in range(quantity):
            self.items.append(item)

        self.total = round(self.total + (price * quantity), 2)
        self.previous_transactions.append({
            "item": item,
            "price": price,
            "quantity": quantity,
        })

    def apply_discount(self):
        if self.discount == 0 or self.total == 0:
            print("There is no discount to apply.")
            return

        self.total = round(self.total * (1 - self.discount / 100), 2)
        print(f"After the discount, the total comes to ${self._format_total()}.")

    def void_last_transaction(self):
        if not self.previous_transactions:
            print("There is no transaction to void.")
            return

        transaction = self.previous_transactions.pop()
        self.total = round(
            self.total - (transaction["price"] * transaction["quantity"]),
            2,
        )
        self._remove_transaction_items(transaction)

    def _remove_transaction_items(self, transaction):
        # Remove from the end so voiding reverses the most recent matching items.
        for _ in range(transaction["quantity"]):
            for index in range(len(self.items) - 1, -1, -1):
                if self.items[index] == transaction["item"]:
                    del self.items[index]
                    break

    def _format_total(self):
        return int(self.total) if self.total == int(self.total) else self.total

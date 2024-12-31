from Order_management_system.customers import VIPCustomer


class Order:
    def __init__(self, customer):
        self.customer = customer
        self.items = []
        self.total = 0
        self.paid = False

    def add_product(self, product, quantity):
        self.items.append((product, quantity))

    def calculate_total(self):
        self.total = sum(product.price * quantity for product, quantity in self.items)
        if isinstance(self.customer, VIPCustomer):
            self.total *= (1 - self.customer.get_discount_rate())
        return self.total

    def pay(self):
        self.paid = True

    def is_paid(self):
        return self.paid
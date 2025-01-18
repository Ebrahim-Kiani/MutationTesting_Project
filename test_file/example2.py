class Customer:

    def __init__(self, name, email):
        self.name = name
        self.email = email


class VIPCustomer(Customer):

    def __init__(self, name, email, discount_rate):
        super().__init__(name, email)
        self.discount_rate = discount_rate

    def get_discount_rate(self):
        return self.discount_rate


class Product:

    def __init__(self, name, price):
        self.name = name
        self.price = price


class Order:

    def __init__(self, customer):
        self.customer = customer
        self.items = []
        self.total = 0
        self.paid = False

    def add_product(self, product, quantity):
        self.items.append((product, quantity))

    def calculate_total(self):
        self.total = sum(product.price * quantity for product, quantity in
            self.items)
        if isinstance(self.customer, VIPCustomer):
            self.total *= 1 - self.customer.get_discount_rate()
        return self.total

    def pay(self):
        self.paid = True

    def is_paid(self):
        return self.paid


class BulkOrderProcessor:

    def __init__(self, orders):
        self.orders = orders

    def process_all_orders(self):
        for order in self.orders:
            if not order.is_paid():
                order.calculate_total()
                order.pay()


def admin_only(func):

    def wrapper(*args, **kwargs):
        user = kwargs.get('user')
        if user and user.get('is_admin', False):
            return func(*args, **kwargs)
        else:
            raise PermissionError('Admin access required')
    return wrapper


class Payment:

    def process_payment(self, order, amount):
        try:
            if amount >= order.calculate_total():
                order.pay()
                return True
            else:
                raise ValueError('Insufficient funds')
        except ValueError as e:
            print(f'Payment error: {e}')
            return False


class Discount:

    def __init__(self, flags):
        self.flags = flags

    def has_discount(self):
        return bool(self.flags & 1)


if __name__ == '__main__':
    customer1 = Customer('John Doe', 'john@example.com')
    vip_customer = VIPCustomer('Jane Doe', 'jane@example.com', 0.2)
    product1 = Product('Laptop', 1000)
    product2 = Product('Phone', 500)
    order1 = Order(customer1)
    order1.add_product(product1, 1)
    order1.add_product(product2, 2)
    order2 = Order(vip_customer)
    order2.add_product(product2, 3)
    bulk_processor = BulkOrderProcessor([order1, order2])
    bulk_processor.process_all_orders()
    payment = Payment()
    print(payment.process_payment(order1, 2000))
    print(payment.process_payment(order1, 2500))

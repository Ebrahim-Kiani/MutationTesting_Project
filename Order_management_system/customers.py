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


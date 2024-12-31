class Discount:
    def __init__(self, flags):
        self.flags = flags

    def has_discount(self):
        return bool(self.flags & 0b01)
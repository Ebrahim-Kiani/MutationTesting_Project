class BulkOrderProcessor:
    def __init__(self, orders):
        self.orders = orders

    def process_all_orders(self):
        for order in self.orders:
            if not order.is_paid():
                order.calculate_total()
                order.pay()
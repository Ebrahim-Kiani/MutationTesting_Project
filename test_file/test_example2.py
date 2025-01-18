# tests/test_orders.py
from project_module.order_management_system import *
from unittest import TestCase
class ProjectTest(TestCase):
    # ----------------------------
    # These are tests to perform the mathematical operator mutation test.
    # ----------------------------
    def test_order_calculate_total_with_vip_discount(self):
        # Arrange
        vip_customer = VIPCustomer(name="Jane Doe", email="jane@example.com", discount_rate=0.1)
        order = Order(vip_customer)
        product1 = Product(name="Laptop", price=1000)
        product2 = Product(name="Phone", price=500)

        # Act
        order.add_product(product1, 1)  # 1000
        order.add_product(product2, 2)  # 500 * 2
        total = order.calculate_total()  # (1000 + 1000) * 0.9

        # Assert
        assert total == 1800  # Total should be 1800 after discount

    def test_order_calculate_total_without_discount(self):
        # Arrange
        customer = VIPCustomer(name="John Doe", email="john@example.com", discount_rate=0)
        order = Order(customer)
        product = Product(name="Tablet", price=200)

        # Act
        order.add_product(product, 3)  # 200 * 3
        total = order.calculate_total()  # 600 (No discount)

        # Assert
        assert total == 600  # Total should be 600

    # -------------------------------------------------------
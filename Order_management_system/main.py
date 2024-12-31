if __name__ == "__main__":
    from customers import Customer, VIPCustomer
    from products import Product
    from orders import Order
    from bulk_processor import BulkOrderProcessor
    from payment import Payment

    # Create customers
    customer1 = Customer("John Doe", "john@example.com")
    vip_customer = VIPCustomer("Jane Doe", "jane@example.com", 0.2)

    # Create products
    product1 = Product("Laptop", 1000)
    product2 = Product("Phone", 500)

    # Create orders
    order1 = Order(customer1)
    order1.add_product(product1, 1)
    order1.add_product(product2, 2)

    order2 = Order(vip_customer)
    order2.add_product(product2, 3)

    # Process bulk orders
    bulk_processor = BulkOrderProcessor([order1, order2])
    bulk_processor.process_all_orders()

    # Check payments
    payment = Payment()
    print(payment.process_payment(order1, 1500))  # False
    print(payment.process_payment(order1, 2500))  # True

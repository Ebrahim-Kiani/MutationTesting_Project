def admin_only(func):
    def wrapper(*args, **kwargs):
        user = kwargs.get('user')
        if user and user.get('is_admin', False):
            return func(*args, **kwargs)
        else:
            raise PermissionError("Admin access required")
    return wrapper

class Payment:
    def process_payment(self, order, amount):
        try:
            if amount >= order.calculate_total():
                order.pay()
                return True
            else:
                raise ValueError("Insufficient funds")
        except ValueError as e:
            print(f"Payment error: {e}")
            return False
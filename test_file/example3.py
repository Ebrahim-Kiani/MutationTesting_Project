def calculate_discounted_price(price, discount_rate):
    """
    Calculate the discounted price given the original price and discount rate.
    
    Args:
        price (float): Original price of the product (must be >= 0).
        discount_rate (float): Discount rate as a percentage (0 <= discount_rate <= 100).
        
    Returns:
        float: Discounted price.
    """
    if price < 0:
        raise ValueError('Price cannot be negative.')
    if discount_rate < 0 or discount_rate > 100:
        raise ValueError('Discount rate must be between 0 and 100.')
    
    discount = price * (discount_rate / 100)
    discounted_price = price - discount
    
    return discounted_price
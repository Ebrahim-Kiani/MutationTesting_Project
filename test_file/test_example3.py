from example3 import calculate_discounted_price 
import unittest

class TestCalculateDiscountedPrice(unittest.TestCase):
    def test_valid_inputs(self):
        # Normal cases
        self.assertAlmostEqual(calculate_discounted_price(100, 10), 90)
        self.assertAlmostEqual(calculate_discounted_price(50, 50), 25)
        self.assertAlmostEqual(calculate_discounted_price(200, 25), 150)
    
    def test_zero_discount(self):
        # Edge case: No discount
        self.assertAlmostEqual(calculate_discounted_price(100, 0), 100)
    
    def test_full_discount(self):
        # Edge case: 100% discount
        self.assertAlmostEqual(calculate_discounted_price(100, 100), 0)
    
    def test_price_zero(self):
        # Edge case: Price is zero
        self.assertAlmostEqual(calculate_discounted_price(0, 50), 0)
    
    def test_invalid_price(self):
        # Negative price should raise an error
        with self.assertRaises(ValueError):
            calculate_discounted_price(-10, 10)
    
    def test_invalid_discount_rate(self):
        # Discount rate out of bounds
        with self.assertRaises(ValueError):
            calculate_discounted_price(100, -1)
        with self.assertRaises(ValueError):
            calculate_discounted_price(100, 101)
    
    def test_boundary_conditions(self):
        # Boundary values for discount_rate
        self.assertAlmostEqual(calculate_discounted_price(100, 0), 100)
        self.assertAlmostEqual(calculate_discounted_price(100, 100), 0)
        # Boundary value for price
        self.assertAlmostEqual(calculate_discounted_price(0, 50), 0)

# Run the tests
if __name__ == "__main__":
    unittest.main()
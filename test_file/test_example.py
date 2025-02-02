import unittest
from example import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(add_numbers(3, 5), 8)

    def test_negative_numbers(self):
        self.assertEqual(add_numbers(-2, -4), -6)

    def test_mixed_sign_numbers(self):
        self.assertEqual(add_numbers(-3, 7), 4)

    def test_zero(self):
        self.assertEqual(add_numbers(0, 0), 0)

if __name__ == "__main__":
    unittest.main()

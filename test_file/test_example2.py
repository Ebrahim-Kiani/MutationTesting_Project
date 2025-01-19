from example2 import *
import unittest


class TestDecorators(unittest.TestCase):
    def test_slow_addition(self):
        # Test slow addition with expected output
        self.assertEqual(slow_addition(2, 3), 5)

    def test_fast_multiplication(self):
        # Test fast multiplication with expected output
        self.assertEqual(fast_multiplication(2, 3), 6)

    def test_execution_time_logging(self):
        # Check that the decorator logs the execution time
        # Note: You can't easily test print statements directly in unit tests,
        # but you can mock or patch 'time.sleep' if needed for precise timing.
        start = time.time()
        slow_addition(1, 1)
        end = time.time()
        self.assertGreaterEqual(end - start, 0.5)  # Ensure at least 0.5s delay

# Run the tests
if __name__ == "__main__":
    unittest.main()

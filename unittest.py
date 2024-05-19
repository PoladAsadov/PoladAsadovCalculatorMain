import unittest
from unittest import CalculatorOperations

class TestCalculatorOperations(unittest.TestCase):

    def setUp(self):
        self.calc = CalculatorOperations()

    def test_addition(self):
        self.assertEqual(self.calc.perform_operation("ADD", 1, 2), 3)

    def test_subtraction(self):
        self.assertEqual(self.calc.perform_operation("SUBTRACT", 5, 2), 3)

    def test_multiplication(self):
        self.assertEqual(self.calc.perform_operation("MULTIPLY", 3, 4), 12)

    def test_division(self):
        self.assertEqual(self.calc.perform_operation("DIVIDE", 10, 2), 5)

    def test_division_by_zero(self):
        self.assertEqual(self.calc.perform_operation("DIVIDE", 10, 0), 'Error')

    def test_operation_not_supported(self):
        with self.assertRaises(ValueError):
            self.calc.perform_operation("UNKNOWN", 10, 2)

if __name__ == '__main__':
    unittest.main()

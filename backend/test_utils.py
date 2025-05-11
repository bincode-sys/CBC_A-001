import unittest
from utils import validate_input

class TestValidateInput(unittest.TestCase):
    def test_valid_input(self):
        self.assertTrue(validate_input(1, 100, 500))

    def test_invalid_week(self):
        self.assertFalse(validate_input(0, 100, 500))

    def test_invalid_transport(self):
        self.assertFalse(validate_input(1, -100, 500))

    def test_invalid_energy(self):
        self.assertFalse(validate_input(1, 100, -500))

    def test_non_numeric_input(self):
        with self.assertRaises(TypeError):
            validate_input("1", 100, 500)

if __name__ == '__main__':
    unittest.main()
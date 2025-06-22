import unittest
from app.modules.toan_validation import ToanValidation

class TestToanValidation(unittest.TestCase):

    def setUp(self):
        self.validator = ToanValidation()

    def test_validate_correct_answer(self):
        self.assertTrue(self.validator.validate_answer(5, 5))
        self.assertTrue(self.validator.validate_answer("10", 10))

    def test_validate_incorrect_answer(self):
        self.assertFalse(self.validator.validate_answer(5, 6))
        self.assertFalse(self.validator.validate_answer("abc", 5))

if __name__ == "__main__":
    unittest.main()

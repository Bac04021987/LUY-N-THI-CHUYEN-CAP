import unittest
from app.modules.toan_module import ToanModule

class TestToanModule(unittest.TestCase):

    def setUp(self):
        self.module = ToanModule(language="vi")

    def test_get_tests_by_level_valid(self):
        tests = self.module.get_tests_by_level(1)
        self.assertIsInstance(tests, list)
        self.assertTrue(len(tests) > 0)

    def test_get_tests_by_level_invalid(self):
        tests = self.module.get_tests_by_level(99)
        self.assertEqual(tests, [])

    def test_find_test_by_id(self):
        test = self.module.find_test_by_id("toan1_001")
        self.assertIsNotNone(test)

    def test_process_math_problem(self):
        problem = "Tính tổng 2 + 3"
        response = self.module.process_math_problem(problem)
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

if __name__ == "__main__":
    unittest.main()

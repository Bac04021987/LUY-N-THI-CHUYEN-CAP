import unittest
from app.modules.tieng_viet_module import TiengVietModule

class TestTiengVietModule(unittest.TestCase):

    def setUp(self):
        self.module = TiengVietModule(language="vi")

    def test_get_tests_by_level(self):
        tests = self.module.get_tests_by_level(1)
        self.assertIsInstance(tests, list)

    def test_find_test_by_id(self):
        test = self.module.find_test_by_id("tv1_001")
        self.assertIsNotNone(test)

    def test_process_language_problem(self):
        problem = "Đọc đoạn văn và trả lời câu hỏi."
        response = self.module.process_language_problem(problem)
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

if __name__ == "__main__":
    unittest.main()

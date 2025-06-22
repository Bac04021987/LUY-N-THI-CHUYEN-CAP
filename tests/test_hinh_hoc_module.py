import unittest
from app.modules.hinh_hoc_module import HinhHocModule

class TestHinhHocModule(unittest.TestCase):

    def setUp(self):
        self.module = HinhHocModule(language="vi")

    def test_get_tests_by_level(self):
        tests = self.module.get_tests_by_level(1)
        self.assertIsInstance(tests, list)

    def test_find_test_by_id(self):
        test = self.module.find_test_by_id("hh1_001")
        self.assertIsNotNone(test)

    def test_process_geometry_problem(self):
        problem = "Xác định hình tam giác có 3 cạnh bằng nhau."
        response = self.module.process_geometry_problem(problem)
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

if __name__ == "__main__":
    unittest.main()

import unittest
from app.modules.toan_logic import ToanLogic

class TestToanLogic(unittest.TestCase):

    def setUp(self):
        self.logic = ToanLogic()

    def test_check_valid_problem(self):
        problem = {
            "id": "toan1_001",
            "title": "Test bài toán",
            "content": "Tính 2 + 3",
            "level": 1
        }
        self.assertTrue(self.logic.kiem_tra_tinh_hop_le_bai_toan(problem))

    def test_check_invalid_problem(self):
        problem = {
            "id": "toan1_002",
            "title": "Bài toán thiếu trường",
            "content": "",
            "level": 4
        }
        self.assertFalse(self.logic.kiem_tra_tinh_hop_le_bai_toan(problem))

if __name__ == "__main__":
    unittest.main()

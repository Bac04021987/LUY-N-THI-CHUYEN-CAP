import unittest
from app.modules.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):

    def setUp(self):
        self.loader = DataLoader()

    def test_load_data(self):
        data = self.loader.load_data("toan", 1)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)

    def test_load_invalid_data(self):
        data = self.loader.load_data("toan", 99)
        self.assertEqual(data, [])

if __name__ == "__main__":
    unittest.main()

import json
import os

class DataProcessing:
    def __init__(self, base_path='data/ngan_hang_de'):
        self.base_path = base_path

    def load_data(self, subject, level):
        """
        Load dữ liệu bài tập theo môn và cấp độ.
        """
        file_path = os.path.join(self.base_path, subject, f"cap_do_{level}", "bai_tap_1.json")
        if not os.path.exists(file_path):
            print(f"File không tồn tại: {file_path}")
            return []
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_data(self, subject, level, data):
        """
        Lưu dữ liệu bài tập vào file JSON theo môn và cấp độ.
        """
        dir_path = os.path.join(self.base_path, subject, f"cap_do_{level}")
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, "bai_tap_1.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

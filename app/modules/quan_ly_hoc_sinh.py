import json
import os

class QuanLyHocSinh:
    def __init__(self, filepath='data/hoc_sinh_data.json'):
        self.filepath = filepath
        self.data = self.load_data()

    def load_data(self):
        if not os.path.exists(self.filepath):
            return {}
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_data(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def them_hoc_sinh(self, ma_hoc_sinh, ten, lop, dob):
        if ma_hoc_sinh in self.data:
            raise ValueError("Mã học sinh đã tồn tại")
        self.data[ma_hoc_sinh] = {
            "name": ten,
            "class": lop,
            "dob": dob,
            "tien_do": []
        }
        self.save_data()

    def cap_nhat_tien_do(self, ma_hoc_sinh, ngay, mon, diem, comment=""):
        if ma_hoc_sinh not in self.data:
            raise ValueError("Không tìm thấy học sinh")
        self.data[ma_hoc_sinh]["tien_do"].append({
            "date": ngay,
            "subject": mon,
            "score": diem,
            "comment": comment
        })
        self.save_data()

    def lay_thong_tin_hoc_sinh(self, ma_hoc_sinh):
        return self.data.get(ma_hoc_sinh, None)

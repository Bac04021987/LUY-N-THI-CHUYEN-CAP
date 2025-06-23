import json
import os

DATA_FILE = "data/hoc_sinh_data.json"

def load_hoc_sinh_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_hoc_sinh_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_student_info(student_id):
    data = load_hoc_sinh_data()
    return data.get(student_id, {})

def update_student_info(student_id, info_dict):
    data = load_hoc_sinh_data()
    data[student_id] = info_dict
    save_hoc_sinh_data(data)

from app.modules.data_loader import DataLoader

class TiengVietModule:
    def __init__(self, language="vi"):
        self.language = language
        self.data_loader = DataLoader()
        self.tests = []

    def get_tests_by_level(self, level):
        self.tests = self.data_loader.load_data("tieng_viet", level)
        return self.tests

    def find_test_by_id(self, test_id):
        for test in self.tests:
            if test.get("id") == test_id:
                return test
        return None

    def process_language_problem(self, content):
        # Đây là chỗ gọi GPT hoặc xử lý logic
        # Tạm thời giả lập phản hồi
        return f"Đã nhận nội dung: {content}"

from typing import List, Dict, Optional
from app.modules.data_loader import DataLoader
from app.gpt_api import GPTClient
import logging

logger = logging.getLogger(__name__)

class ToanModule:
    """
    Module xử lý chức năng dành riêng cho môn Toán,
    hỗ trợ đa ngôn ngữ (mặc định tiếng Việt),
    bao gồm lấy đề thi theo cấp độ, tạo mô tả đề thi bằng AI,
    xử lý bài tập chi tiết, và validate đầu ra GPT.
    """

    def __init__(self, language: str = "vi"):
        """
        Khởi tạo module với ngôn ngữ mặc định là tiếng Việt.
        :param language: Mã ngôn ngữ (ví dụ: 'vi', 'en')
        """
        self.language = language.lower()
        self.data_loader = DataLoader()
        self.gpt_client = GPTClient()

    def _validate_gpt_output(self, output: str) -> bool:
        """
        Validate cơ bản đầu ra GPT: không rỗng, đủ dài, không phải lỗi hay cảnh báo.
        :param output: Chuỗi trả về từ GPT
        :return: True nếu hợp lệ, False nếu không
        """
        if not output:
            logger.warning("GPT output is empty.")
            return False
        if len(output) < 10:
            logger.warning("GPT output too short.")
            return False
        if any(bad in output.lower() for bad in ["error", "cannot", "not able", "xin lỗi", "không thể"]):
            logger.warning(f"GPT output contains error-like content: {output}")
            return False
        return True

    def get_tests_by_level(self, level: int) -> List[Dict]:
        """
        Lấy danh sách đề thi Toán theo cấp độ.
        :param level: Cấp độ bài tập (1, 2 hoặc 3)
        :return: List dict chứa đề thi, hoặc list rỗng nếu lỗi hoặc không hợp lệ
        """
        if level not in {1, 2, 3}:
            logger.warning(f"get_tests_by_level: Cấp độ không hợp lệ: {level}")
            return []

        subject_folder = "toan" if self.language == "vi" else f"toan_{self.language}"

        return self.data_loader.load_subject_level(subject_folder, level)

    def get_test_description(self, test: Dict) -> str:
        """
        Gọi GPT để tạo mô tả chi tiết cho đề thi Toán.
        :param test: Dict chứa thông tin đề thi, cần có ít nhất trường 'title'
        :return: Chuỗi mô tả do AI tạo hoặc thông báo lỗi
        """
        if not test or 'title' not in test:
            logger.warning("get_test_description: Dữ liệu đề thi không hợp lệ hoặc thiếu trường 'title'.")
            return "Dữ liệu đề thi không hợp lệ."

        try:
            title = test['title']
            system_prompt = {
                "vi": "Bạn là trợ lý giáo dục Toán lớp 5 chuẩn bị thi lên lớp 6.",
                "en": "You are a math tutor assistant for grade 5 students preparing for grade 6 entrance exams."
            }.get(self.language, "Bạn là trợ lý giáo dục Toán lớp 5 chuẩn bị thi lên lớp 6.")

            user_prompt = {
                "vi": f"Giúp tôi mô tả đề thi Toán sau: {title}",
                "en": f"Please describe the following math test: {title}"
            }.get(self.language, f"Giúp tôi mô tả đề thi Toán sau: {title}")

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            response = self.gpt_client.chat_completion(messages)

            if not self._validate_gpt_output(response):
                logger.warning(f"Mô tả đề thi không hợp lệ: {response}")
                return "Mô tả đề thi không đủ chi tiết hoặc không hợp lệ."

            return response

        except Exception as e:
            logger.error(f"Lỗi khi gọi GPT tạo mô tả đề thi: {e}")
            return "Không thể tạo mô tả đề thi vào lúc này."

    def find_test_by_id(self, test_id: str) -> Optional[Dict]:
        """
        Tìm đề thi Toán theo ID qua tất cả cấp độ.
        :param test_id: Chuỗi ID đề thi cần tìm
        :return: Dict đề thi nếu tìm thấy, None nếu không
        """
        if not test_id:
            logger.warning("find_test_by_id: test_id không được để trống.")
            return None

        subject_folder = "toan" if self.language == "vi" else f"toan_{self.language}"

        for level in range(1, 4):
            tests = self.get_tests_by_level(level)
            for test in tests:
                if test.get('id') == test_id:
                    return test
        logger.info(f"Không tìm thấy đề thi id={test_id} trong môn Toán.")
        return None

    def process_math_problem(self, problem_text: str) -> str:
        """
        Hàm mẫu xử lý bài toán chi tiết, có thể gọi GPT giải bài tập hoặc phân tích.
        :param problem_text: Văn bản bài toán cần xử lý
        :return: Lời giải hoặc phân tích của AI
        """
        try:
            system_prompt = {
                "vi": "Bạn là trợ lý giáo dục Toán lớp 5.",
                "en": "You are a grade 5 math tutor assistant."
            }.get(self.language, "Bạn là trợ lý giáo dục Toán lớp 5.")

            user_prompt = {
                "vi": f"Giải bài toán sau và giải thích chi tiết từng bước: {problem_text}",
                "en": f"Solve the following math problem and explain each step: {problem_text}"
            }.get(self.language, f"Giải bài toán sau và giải thích chi tiết từng bước: {problem_text}")

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            response = self.gpt_client.chat_completion(messages)

            if not self._validate_gpt_output(response):
                logger.warning(f"Lời giải bài tập không hợp lệ: {response}")
                return "Lời giải bài tập không đủ chi tiết hoặc không hợp lệ."

            return response
        except Exception as e:
            logger.error(f"Lỗi khi xử lý bài toán: {e}")
            return "Không thể giải bài toán vào lúc này."

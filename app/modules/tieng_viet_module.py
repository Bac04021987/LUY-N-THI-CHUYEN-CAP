from typing import List, Dict, Optional
from app.modules.data_loader import DataLoader
from app.gpt_api import GPTClient
import logging
import functools

logger = logging.getLogger(__name__)

class TiengVietModule:
    """
    Module xử lý chức năng dành riêng cho môn Tiếng Việt,
    hỗ trợ đa ngôn ngữ (mặc định tiếng Việt),
    bao gồm lấy đề thi theo cấp độ, tạo mô tả đề thi bằng AI,
    và xử lý bài tập chi tiết.
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

    @functools.lru_cache(maxsize=64)
    def get_tests_by_level(self, level: int) -> List[Dict]:
        """
        Lấy danh sách đề thi Tiếng Việt theo cấp độ.
        :param level: Cấp độ bài tập (1, 2 hoặc 3)
        :return: Danh sách đề thi hoặc list rỗng nếu không hợp lệ hoặc lỗi
        """
        if level not in {1, 2, 3}:
            logger.warning(f"get_tests_by_level: Cấp độ không hợp lệ: {level}")
            return []

        subject_folder = "tieng_viet" if self.language == "vi" else f"tieng_viet_{self.language}"

        return self.data_loader.load_subject_level(subject_folder, level)

    def get_test_description(self, test: Dict) -> str:
        """
        Tạo mô tả chi tiết cho đề thi Tiếng Việt bằng GPT.
        :param test: Đề thi dạng dict, cần có trường 'title'
        :return: Mô tả đề thi hoặc thông báo lỗi
        """
        if not test or 'title' not in test:
            logger.warning("get_test_description: Đề thi không hợp lệ hoặc thiếu trường 'title'.")
            return "Dữ liệu đề thi không hợp lệ."

        try:
            title = test['title']
            system_prompt = {
                "vi": "Bạn là trợ lý giáo dục Tiếng Việt lớp 5 chuẩn bị thi lên lớp 6.",
                "en": "You are a Vietnamese language tutor assistant for grade 5 students preparing for grade 6 exams."
            }.get(self.language, "Bạn là trợ lý giáo dục Tiếng Việt lớp 5 chuẩn bị thi lên lớp 6.")

            user_prompt = {
                "vi": f"Giúp tôi mô tả đề thi Tiếng Việt sau: {title}",
                "en": f"Please describe the following Vietnamese language test: {title}"
            }.get(self.language, f"Giúp tôi mô tả đề thi Tiếng Việt sau: {title}")

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
            logger.error(f"Lỗi khi tạo mô tả đề thi Tiếng Việt: {e}")
            return "Không thể tạo mô tả đề thi vào lúc này."

    def find_test_by_id(self, test_id: str) -> Optional[Dict]:
        """
        Tìm đề thi Tiếng Việt theo ID trong các cấp độ.
        :param test_id: ID đề thi cần tìm
        :return: Đề thi nếu tìm thấy, None nếu không
        """
        if not test_id:
            logger.warning("find_test_by_id: test_id không được để trống.")
            return None

        subject_folder = "tieng_viet" if self.language == "vi" else f"tieng_viet_{self.language}"

        for level in range(1, 4):
            tests = self.get_tests_by_level(level)
            for test in tests:
                if test.get('id') == test_id:
                    return test
        logger.info(f"Không tìm thấy đề thi id={test_id} trong môn Tiếng Việt.")
        return None

    def process_vietnamese_problem(self, problem_text: str) -> str:
        """
        Xử lý bài tập Tiếng Việt chi tiết bằng GPT.
        :param problem_text: Văn bản bài tập
        :return: Lời giải hoặc phân tích chi tiết
        """
        try:
            system_prompt = {
                "vi": "Bạn là trợ lý giáo dục Tiếng Việt lớp 5.",
                "en": "You are a Vietnamese language tutor assistant for grade 5 students."
            }.get(self.language, "Bạn là trợ lý giáo dục Tiếng Việt lớp 5.")

            user_prompt = {
                "vi": f"Giải bài tập Tiếng Việt sau và giải thích chi tiết: {problem_text}",
                "en": f"Solve the following Vietnamese language exercise and explain in detail: {problem_text}"
            }.get(self.language, f"Giải bài tập Tiếng Việt sau và giải thích chi tiết: {problem_text}")

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
            logger.error(f"Lỗi khi xử lý bài tập Tiếng Việt: {e}")
            return "Không thể giải bài tập vào lúc này."

    def run_unit_tests(self):
        """
        Khung hàm đơn giản để phát triển bộ test tự động cho module.
        Hiện chưa có test thực thi, bạn có thể mở rộng theo nhu cầu.
        """
        logger.info("Chạy unit test mẫu cho TiengVietModule...")
        # Ví dụ test lấy đề cấp độ 1
        tests = self.get_tests_by_level(1)
        assert isinstance(tests, list), "get_tests_by_level phải trả về list"
        logger.info(f"Test get_tests_by_level(1): OK, tìm thấy {len(tests)} đề thi.")

        # Thêm test khác khi cần
        logger.info("Unit test hoàn tất. Bạn hãy thêm test cụ thể vào hàm này.")

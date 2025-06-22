from typing import List, Dict

class PromptBuilder:
    """
    Module hỗ trợ xây dựng prompt cho các nhiệm vụ gửi GPT,
    giúp chuẩn hóa và tái sử dụng cấu trúc prompt.
    """

    @staticmethod
    def build_math_description_prompt(title: str, language: str = "vi") -> List[Dict]:
        """
        Tạo prompt mô tả đề thi Toán.
        :param title: Tiêu đề đề thi
        :param language: Ngôn ngữ ('vi' hoặc 'en')
        :return: Danh sách message theo định dạng API Chat
        """
        system_content = {
            "vi": "Bạn là trợ lý giáo dục Toán lớp 5 chuẩn bị thi lên lớp 6.",
            "en": "You are a grade 5 math tutor assistant preparing for grade 6 exams."
        }.get(language, "Bạn là trợ lý giáo dục Toán lớp 5 chuẩn bị thi lên lớp 6.")

        user_content = {
            "vi": f"Giúp tôi mô tả đề thi Toán sau: {title}",
            "en": f"Please describe the following math test: {title}"
        }.get(language, f"Giúp tôi mô tả đề thi Toán sau: {title}")

        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    @staticmethod
    def build_vietnamese_description_prompt(title: str, language: str = "vi") -> List[Dict]:
        """
        Tạo prompt mô tả đề thi Tiếng Việt.
        :param title: Tiêu đề đề thi
        :param language: Ngôn ngữ ('vi' hoặc 'en')
        :return: Danh sách message theo định dạng API Chat
        """
        system_content = {
            "vi": "Bạn là trợ lý giáo dục Tiếng Việt lớp 5 chuẩn bị thi lên lớp 6.",
            "en": "You are a Vietnamese language tutor assistant for grade 5 preparing for grade 6 exams."
        }.get(language, "Bạn là trợ lý giáo dục Tiếng Việt lớp 5 chuẩn bị thi lên lớp 6.")

        user_content = {
            "vi": f"Giúp tôi mô tả đề thi Tiếng Việt sau: {title}",
            "en": f"Please describe the following Vietnamese language test: {title}"
        }.get(language, f"Giúp tôi mô tả đề thi Tiếng Việt sau: {title}")

        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    @staticmethod
    def build_geometry_description_prompt(title: str, language: str = "vi") -> List[Dict]:
        """
        Tạo prompt mô tả đề thi Hình học.
        :param title: Tiêu đề đề thi
        :param language: Ngôn ngữ ('vi' hoặc 'en')
        :return: Danh sách message theo định dạng API Chat
        """
        system_content = {
            "vi": "Bạn là trợ lý giáo dục môn Hình học lớp 5 chuẩn bị thi lên lớp 6.",
            "en": "You are a geometry tutor assistant for grade 5 preparing for grade 6 exams."
        }.get(language, "Bạn là trợ lý giáo dục môn Hình học lớp 5 chuẩn bị thi lên lớp 6.")

        user_content = {
            "vi": f"Giúp tôi mô tả bài tập Hình học sau: {title}",
            "en": f"Please describe the following geometry problem: {title}"
        }.get(language, f"Giúp tôi mô tả bài tập Hình học sau: {title}")

        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

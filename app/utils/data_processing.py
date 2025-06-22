import re
import logging

logger = logging.getLogger(__name__)

class DataProcessing:
    """
    Module xử lý dữ liệu thô, tiền xử lý văn bản, lọc và chuẩn hóa dữ liệu đầu vào.
    """

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Làm sạch văn bản: loại bỏ ký tự đặc biệt, khoảng trắng thừa.
        :param text: Chuỗi văn bản đầu vào
        :return: Chuỗi văn bản đã được làm sạch
        """
        try:
            text = text.strip()
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'[^\w\s.,?!]', '', text)
            return text
        except Exception as e:
            logger.error(f"Lỗi khi làm sạch văn bản: {e}")
            return text

    @staticmethod
    def split_sentences(text: str) -> list:
        """
        Tách văn bản thành các câu riêng biệt dựa trên dấu câu phổ biến.
        :param text: Chuỗi văn bản
        :return: Danh sách câu
        """
        try:
            sentences = re.split(r'(?<=[.!?]) +', text)
            return [s.strip() for s in sentences if s.strip()]
        except Exception as e:
            logger.error(f"Lỗi khi tách câu: {e}")
            return [text]

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Chuẩn hóa văn bản (ví dụ chuyển về chữ thường).
        :param text: Chuỗi văn bản
        :return: Văn bản chuẩn hóa
        """
        try:
            return text.lower()
        except Exception as e:
            logger.error(f"Lỗi khi chuẩn hóa văn bản: {e}")
            return text

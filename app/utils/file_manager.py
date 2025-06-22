import os
import logging

logger = logging.getLogger(__name__)

class FileManager:
    """
    Quản lý đọc ghi file tiện ích.
    """

    @staticmethod
    def read_text_file(path: str) -> str:
        if not os.path.exists(path):
            logger.warning(f"File không tồn tại: {path}")
            return ""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Lỗi đọc file {path}: {e}")
            return ""

    @staticmethod
    def write_text_file(path: str, content: str) -> bool:
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except Exception as e:
            logger.error(f"Lỗi ghi file {path}: {e}")
            return False

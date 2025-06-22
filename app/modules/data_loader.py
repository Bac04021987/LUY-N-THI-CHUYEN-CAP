import json
import os
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, base_path: str = 'data/ngan_hang_de'):
        self.base_path = base_path

    def load_subject_level(self, subject: str, level: int) -> List[Dict]:
        """
        Load danh sách đề thi hoặc bài tập theo môn và cấp độ.
        :param subject: 'toan' hoặc 'tieng_viet'
        :param level: 1, 2 hoặc 3
        :return: danh sách đề thi dạng list dict, hoặc list rỗng nếu lỗi
        """
        dir_path = os.path.join(self.base_path, subject, f'cap_do_{level}')
        file_path = os.path.join(dir_path, 'de_thi.json')
        if not os.path.exists(file_path):
            logger.error(f"File đề thi không tồn tại: {file_path}")
            return []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Validate dữ liệu cơ bản
            if not isinstance(data, list):
                logger.error(f"Dữ liệu đề thi không đúng định dạng list: {file_path}")
                return []
            for item in data:
                if not isinstance(item, dict) or 'id' not in item or 'title' not in item:
                    logger.warning(f"Đề thi thiếu trường bắt buộc id hoặc title: {item}")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Lỗi đọc file JSON: {file_path} - {e}")
            return []

    def load_answer_key(self, subject: str, level: int) -> Dict:
        """
        Load lời giải tương ứng theo môn và cấp độ.
        :return: dict id_bai_tap -> loi_giai, hoặc dict rỗng nếu lỗi
        """
        dir_path = os.path.join(self.base_path, subject, f'cap_do_{level}')
        file_path = os.path.join(dir_path, 'loi_giai.json')
        if not os.path.exists(file_path):
            logger.error(f"File lời giải không tồn tại: {file_path}")
            return {}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                answers = json.load(f)
            if not isinstance(answers, dict):
                logger.error(f"Dữ liệu lời giải không đúng định dạng dict: {file_path}")
                return {}
            return answers
        except json.JSONDecodeError as e:
            logger.error(f"Lỗi đọc file JSON lời giải: {file_path} - {e}")
            return {}

    def find_test_by_id(self, subject: str, test_id: str) -> Optional[Dict]:
        """
        Tìm đề thi theo test_id trong tất cả cấp độ của môn.
        :return: dict đề thi nếu tìm thấy, None nếu không
        """
        for level in range(1, 4):
            tests = self.load_subject_level(subject, level)
            for test in tests:
                if test.get('id') == test_id:
                    return test
        logger.info(f"Không tìm thấy đề thi id={test_id} trong môn {subject}")
        return None

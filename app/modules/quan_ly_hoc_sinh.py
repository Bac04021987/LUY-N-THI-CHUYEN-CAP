import logging
from typing import Dict, List, Optional
import json
import os

logger = logging.getLogger(__name__)

class QuanLyHocSinh:
    """
    Module quản lý thông tin học sinh, lịch sử học tập và tiến độ.
    """

    def __init__(self, data_path: str = "data/hoc_sinh_data.json"):
        """
        Khởi tạo module với đường dẫn lưu trữ dữ liệu học sinh.
        :param data_path: Đường dẫn file JSON lưu thông tin học sinh.
        """
        self.data_path = data_path
        self.hoc_sinh_data = self._load_data()

    def _load_data(self) -> Dict[str, Dict]:
        """
        Đọc dữ liệu học sinh từ file JSON.
        :return: dict với key là mã học sinh, value là thông tin chi tiết.
        """
        if not os.path.exists(self.data_path):
            logger.info(f"File dữ liệu học sinh không tồn tại: {self.data_path}, tạo file mới.")
            return {}

        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception as e:
            logger.error(f"Lỗi đọc file dữ liệu học sinh: {e}")
            return {}

    def _save_data(self):
        """
        Lưu dữ liệu học sinh vào file JSON.
        """
        try:
            with open(self.data_path, "w", encoding="utf-8") as f:
                json.dump(self.hoc_sinh_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Lỗi lưu file dữ liệu học sinh: {e}")

    def them_hoc_sinh(self, ma_hoc_sinh: str, thong_tin: Dict):
        """
        Thêm học sinh mới hoặc cập nhật thông tin học sinh.
        :param ma_hoc_sinh: Mã định danh học sinh
        :param thong_tin: dict chứa thông tin học sinh (tên, lớp, ngày sinh,...)
        """
        self.hoc_sinh_data[ma_hoc_sinh] = thong_tin
        self._save_data()
        logger.info(f"Đã thêm/cập nhật học sinh: {ma_hoc_sinh}")

    def lay_thong_tin_hoc_sinh(self, ma_hoc_sinh: str) -> Optional[Dict]:
        """
        Lấy thông tin chi tiết học sinh theo mã.
        :param ma_hoc_sinh: Mã định danh học sinh
        :return: dict thông tin học sinh hoặc None nếu không tồn tại
        """
        return self.hoc_sinh_data.get(ma_hoc_sinh)

    def cap_nhat_tien_do(self, ma_hoc_sinh: str, tien_do_moi: Dict):
        """
        Cập nhật tiến độ học tập cho học sinh.
        :param ma_hoc_sinh: Mã định danh học sinh
        :param tien_do_moi: dict tiến độ mới (ví dụ bài đã làm, điểm số, ngày)
        """
        if ma_hoc_sinh not in self.hoc_sinh_data:
            logger.warning(f"Học sinh {ma_hoc_sinh} không tồn tại để cập nhật tiến độ.")
            return

        tien_do = self.hoc_sinh_data[ma_hoc_sinh].get("tien_do", [])
        tien_do.append(tien_do_moi)
        self.hoc_sinh_data[ma_hoc_sinh]["tien_do"] = tien_do
        self._save_data()
        logger.info(f"Cập nhật tiến độ học tập cho học sinh: {ma_hoc_sinh}")

    def lay_tien_do(self, ma_hoc_sinh: str) -> Optional[List[Dict]]:
        """
        Lấy lịch sử tiến độ học tập của học sinh.
        :param ma_hoc_sinh: Mã định danh học sinh
        :return: List tiến độ học tập hoặc None nếu không tồn tại
        """
        if ma_hoc_sinh not in self.hoc_sinh_data:
            logger.warning(f"Học sinh {ma_hoc_sinh} không tồn tại để lấy tiến độ.")
            return None

        return self.hoc_sinh_data[ma_hoc_sinh].get("tien_do", [])


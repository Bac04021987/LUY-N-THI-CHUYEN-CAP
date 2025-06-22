import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DanhGiaNangLuc:
    """
    Module đánh giá năng lực học sinh dựa trên kết quả làm bài tập, điểm số và tiến độ học tập.
    """

    def __init__(self):
        pass

    def phan_loai_nang_luc(self, diem_trung_binh: float) -> str:
        """
        Phân loại năng lực dựa trên điểm trung bình.
        :param diem_trung_binh: điểm trung bình (0-10)
        :return: Chuỗi phân loại năng lực: 'Yếu', 'Trung bình', 'Khá', 'Giỏi'
        """
        if diem_trung_binh < 0 or diem_trung_binh > 10:
            logger.warning(f"Điểm trung bình không hợp lệ: {diem_trung_binh}")
            return "Không hợp lệ"

        if diem_trung_binh < 4:
            return "Yếu"
        elif diem_trung_binh < 6.5:
            return "Trung bình"
        elif diem_trung_binh < 8.5:
            return "Khá"
        else:
            return "Giỏi"

    def danh_gia_theo_bai_lam(self, ket_qua_bai_lam: Dict[str, Any]) -> Dict[str, Any]:
        """
        Đánh giá năng lực dựa trên kết quả bài làm chi tiết.
        Ví dụ `ket_qua_bai_lam` có thể chứa:
        {
            'so_bai_lam': 10,
            'so_bai_dung': 8,
            'diem_tong': 80,
            'diem_trung_binh': 8.0,
            'thoi_gian_lam': 120  # đơn vị phút
        }
        :return: dict bổ sung thêm phân loại năng lực và nhận xét
        """
        diem_tb = ket_qua_bai_lam.get('diem_trung_binh')
        if diem_tb is None:
            logger.warning("Dữ liệu kết quả bài làm thiếu điểm trung bình.")
            return {"phan_loai": "Không xác định", "nhan_xet": "Thiếu điểm trung bình"}

        phan_loai = self.phan_loai_nang_luc(diem_tb)
        nhan_xet = self._tao_nhan_xet(phan_loai, ket_qua_bai_lam)

        ket_qua_bai_lam['phan_loai'] = phan_loai
        ket_qua_bai_lam['nhan_xet'] = nhan_xet

        return ket_qua_bai_lam

    def _tao_nhan_xet(self, phan_loai: str, ket_qua_bai_lam: Dict[str, Any]) -> str:
        """
        Tạo nhận xét theo phân loại năng lực và kết quả bài làm.
        """
        if phan_loai == "Yếu":
            return "Cần cố gắng hơn, ôn tập kỹ kiến thức cơ bản."
        elif phan_loai == "Trung bình":
            return "Đã nắm được kiến thức cơ bản, nên luyện tập thêm."
        elif phan_loai == "Khá":
            return "Hiệu quả học tập tốt, tiếp tục phát huy."
        elif phan_loai == "Giỏi":
            return "Xuất sắc, bạn có nền tảng vững chắc và kỹ năng tốt."
        else:
            return "Không có nhận xét phù hợp."


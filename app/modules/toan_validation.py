import logging
from typing import Any

logger = logging.getLogger(__name__)

class ToanValidation:
    """
    Module kiểm tra và xác thực dữ liệu, đáp án môn Toán.
    """

    def __init__(self):
        pass

    def kiem_tra_dap_an_so(self, dap_an_nguoi_dung: Any, dap_an_chuan: Any) -> bool:
        """
        Kiểm tra đáp án của học sinh có đúng hay không (dạng số).
        :param dap_an_nguoi_dung: Đáp án học sinh trả về (có thể số int hoặc float)
        :param dap_an_chuan: Đáp án chuẩn
        :return: True nếu đúng, False nếu sai
        """
        try:
            if isinstance(dap_an_chuan, (int, float)) and isinstance(dap_an_nguoi_dung, (int, float)):
                # So sánh với độ chính xác nhất định
                return abs(dap_an_chuan - dap_an_nguoi_dung) < 1e-6
            else:
                logger.warning(f"Kiểm tra đáp án số: kiểu dữ liệu không hợp lệ: {dap_an_nguoi_dung}, {dap_an_chuan}")
                return False
        except Exception as e:
            logger.error(f"Lỗi khi kiểm tra đáp án số: {e}")
            return False

    def kiem_tra_dap_an_trac_nghiem(self, dap_an_nguoi_dung: str, dap_an_chuan: str) -> bool:
        """
        Kiểm tra đáp án trắc nghiệm (ký tự, chuỗi).
        :param dap_an_nguoi_dung: Đáp án học sinh trả về (ký tự như 'A', 'B', ...)
        :param dap_an_chuan: Đáp án chuẩn
        :return: True nếu đúng, False nếu sai
        """
        try:
            return str(dap_an_nguoi_dung).strip().upper() == str(dap_an_chuan).strip().upper()
        except Exception as e:
            logger.error(f"Lỗi khi kiểm tra đáp án trắc nghiệm: {e}")
            return False

    def kiem_tra_dap_an_tong_quat(self, dap_an_nguoi_dung: Any, dap_an_chuan: Any) -> bool:
        """
        Kiểm tra đáp án tổng quát, tự động nhận diện kiểu và so sánh.
        Hỗ trợ số và trắc nghiệm.
        """
        if isinstance(dap_an_chuan, (int, float)):
            return self.kiem_tra_dap_an_so(dap_an_nguoi_dung, dap_an_chuan)
        elif isinstance(dap_an_chuan, str):
            return self.kiem_tra_dap_an_trac_nghiem(dap_an_nguoi_dung, dap_an_chuan)
        else:
            logger.warning(f"Kiểm tra đáp án tổng quát: loại dữ liệu đáp án chuẩn không được hỗ trợ: {type(dap_an_chuan)}")
            return False

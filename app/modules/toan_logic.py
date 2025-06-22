import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ToanLogic:
    """
    Module xử lý các hàm logic toán học nâng cao,
    giúp phân tích bài toán, kiểm tra tính hợp lệ và hỗ trợ xử lý dữ liệu toán.
    """

    def __init__(self):
        pass

    def kiem_tra_tinh_hop_le_bai_toan(self, bai_toan: Dict[str, Any]) -> bool:
        """
        Kiểm tra tính hợp lệ của bài toán.
        Ví dụ: kiểm tra có đủ các trường cần thiết, định dạng đúng, các giá trị trong phạm vi hợp lệ...
        :param bai_toan: dict chứa thông tin bài toán
        :return: True nếu hợp lệ, False nếu không
        """
        required_fields = ['id', 'title', 'content', 'level']
        for field in required_fields:
            if field not in bai_toan:
                logger.warning(f"Bài toán thiếu trường bắt buộc: {field}")
                return False

        # Ví dụ kiểm tra độ khó level trong phạm vi 1-3
        if bai_toan.get('level') not in {1, 2, 3}:
            logger.warning(f"Bài toán có level không hợp lệ: {bai_toan.get('level')}")
            return False

        # Kiểm tra nội dung không rỗng
        if not bai_toan.get('content'):
            logger.warning("Bài toán có nội dung rỗng.")
            return False

        return True

    def phan_tich_bai_toan(self, bai_toan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phân tích bài toán, tách thành các phần (ví dụ đề bài, dữ kiện, yêu cầu).
        Đây là hàm mẫu, có thể mở rộng thêm sau.
        :param bai_toan: dict chứa bài toán
        :return: dict phân tích chi tiết
        """
        if not self.kiem_tra_tinh_hop_le_bai_toan(bai_toan):
            logger.error("Bài toán không hợp lệ, không thể phân tích.")
            return {}

        # Giả sử bài toán có trường 'content' dạng text, ta tách bằng câu.
        content = bai_toan.get('content', '')
        cau_chi = [c.strip() for c in content.split('.') if c.strip()]

        phan_tich = {
            'de_bai': cau_chi[0] if len(cau_chi) > 0 else '',
            'du_lieu': cau_chi[1:-1] if len(cau_chi) > 2 else [],
            'yeu_cau': cau_chi[-1] if len(cau_chi) > 1 else ''
        }

        return phan_tich

    def tinh_toan_bai_toan(self, phan_tich: Dict[str, Any]) -> Any:
        """
        Hàm mẫu tính toán kết quả bài toán dựa trên phân tích.
        Hiện để trống, sẽ bổ sung sau tùy bài toán cụ thể.
        """
        # TODO: Triển khai thuật toán tính toán cụ thể cho từng dạng bài toán
        logger.info("Hàm tính toán bài toán chưa được triển khai.")
        return None

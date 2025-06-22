import matplotlib.pyplot as plt
import io
import base64
import logging

logger = logging.getLogger(__name__)

class Visualization:
    """
    Module hỗ trợ tạo hình ảnh minh họa và biểu đồ.
    """

    @staticmethod
    def plot_score_progression(dates, scores):
        """
        Vẽ biểu đồ tiến trình điểm số của học sinh theo thời gian.
        :param dates: Danh sách ngày tháng (dạng chuỗi)
        :param scores: Danh sách điểm số tương ứng
        :return: Chuỗi base64 của hình ảnh PNG để dễ dàng nhúng vào web hoặc app
        """
        try:
            plt.figure(figsize=(8, 4))
            plt.plot(dates, scores, marker='o', linestyle='-', color='blue')
            plt.title("Tiến trình điểm số theo thời gian")
            plt.xlabel("Ngày")
            plt.ylabel("Điểm số")
            plt.xticks(rotation=45)
            plt.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            buf.seek(0)

            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            return img_base64
        except Exception as e:
            logger.error(f"Lỗi khi tạo biểu đồ tiến trình điểm số: {e}")
            return None

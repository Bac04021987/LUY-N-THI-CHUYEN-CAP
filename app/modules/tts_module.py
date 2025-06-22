import logging
from typing import Optional
# Giả sử dùng thư viện pyttsx3 để chuyển text thành speech offline
# Bạn có thể thay thế bằng dịch vụ TTS online như Google TTS, Amazon Polly, v.v.
import pyttsx3

logger = logging.getLogger(__name__)

class TTSModule:
    """
    Module chuyển văn bản thành giọng nói (Text-to-Speech).
    """

    def __init__(self, voice_rate: int = 150, voice_volume: float = 1.0):
        """
        Khởi tạo engine TTS.
        :param voice_rate: Tốc độ đọc (mặc định 150)
        :param voice_volume: Âm lượng (0.0 đến 1.0)
        """
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', voice_rate)
            self.engine.setProperty('volume', voice_volume)
        except Exception as e:
            logger.error(f"Lỗi khởi tạo TTS engine: {e}")
            self.engine = None

    def text_to_speech(self, text: str, output_file: Optional[str] = None) -> Optional[str]:
        """
        Chuyển văn bản thành giọng nói.
        Nếu output_file được chỉ định, lưu ra file audio (.mp3, .wav).
        Nếu không, phát trực tiếp giọng nói.

        :param text: Văn bản cần chuyển
        :param output_file: Đường dẫn file lưu âm thanh (tuỳ chọn)
        :return: Đường dẫn file âm thanh nếu lưu, None nếu phát trực tiếp hoặc lỗi
        """
        if not self.engine:
            logger.error("TTS engine chưa được khởi tạo.")
            return None
        try:
            if output_file:
                self.engine.save_to_file(text, output_file)
                self.engine.runAndWait()
                logger.info(f"Lưu file âm thanh thành công: {output_file}")
                return output_file
            else:
                self.engine.say(text)
                self.engine.runAndWait()
                logger.info("Phát giọng nói trực tiếp thành công.")
                return None
        except Exception as e:
            logger.error(f"Lỗi khi chuyển text thành speech: {e}")
            return None

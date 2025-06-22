import unittest
from app.modules.tts_module import TTSModule

class TestTTSModule(unittest.TestCase):

    def setUp(self):
        self.tts = TTSModule()

    def test_text_to_speech(self):
        text = "Xin chào, đây là test chuyển văn bản thành giọng nói."
        audio = self.tts.text_to_speech(text)
        self.assertIsNotNone(audio)
        self.assertIsInstance(audio, bytes)

if __name__ == "__main__":
    unittest.main()

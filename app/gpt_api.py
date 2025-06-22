import os
from typing import Optional, List, Dict
from openai import OpenAI
from openai.error import OpenAIError

class GPTClient:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key OpenAI chưa được cấu hình!")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def chat_completion(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """
        Gửi yêu cầu chat completion tới OpenAI GPT
        :param messages: List các message dạng dict {"role": "user/assistant/system", "content": "..."}
        :param temperature: Độ sáng tạo
        :param max_tokens: Giới hạn token trả về
        :return: Chuỗi text phản hồi của AI
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except OpenAIError as e:
            print(f"Lỗi khi gọi OpenAI API: {e}")
            return "Xin lỗi, hiện tại tôi không thể xử lý yêu cầu này."

# Ví dụ sử dụng nhanh
if __name__ == "__main__":
    client = GPTClient()
    messages = [
        {"role": "system", "content": "Bạn là trợ lý giáo dục Toán và Tiếng Việt lớp 5."},
        {"role": "user", "content": "Cho tôi một bài toán đơn giản về số học."}
    ]
    print(client.chat_completion(messages))

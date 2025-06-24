import os
import openai

class GPTClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Bạn cần thiết lập biến môi trường OPENAI_API_KEY")
        openai.api_key = api_key

    def chat(self, messages, model="gpt-4o-mini", temperature=0.7, max_tokens=1500):
        """
        Gửi yêu cầu chat đến OpenAI GPT và trả về phản hồi.
        messages: list các dict theo định dạng chat completion.
        """
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            content = response.choices[0].message.content
            print(f"GPT Response: {content}")
            return content
        except Exception as e:
            error_msg = f"Lỗi khi gọi API OpenAI: {e}"
            print(error_msg)
            return error_msg

# Ví dụ sử dụng:
if __name__ == "__main__":
    gpt = GPTClient()
    test_messages = [
        {"role": "system", "content": "Bạn là trợ lý giáo dục."},
        {"role": "user", "content": "Xin chào, hãy giúp tôi trả lời câu hỏi sau."}
    ]
    result = gpt.chat(test_messages)
    print("Phản hồi từ GPT:", result)

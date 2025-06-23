import os
from openai import OpenAI
from openai.error import OpenAIError

# Khởi tạo client OpenAI, đọc key từ biến môi trường
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_chat_completion(messages, model="gpt-4o-mini", temperature=0.7):
    """
    Gọi OpenAI Chat Completion API với messages dạng list dict
    messages = [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."},
        ...
    ]
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        print(f"[GPT API Error]: {e}")
        return None

from app.gpt_api import call_chat_completion
from app.utils.prompt_builder import build_tiengviet_prompt

def solve_tiengviet(question):
    prompt = build_tiengviet_prompt(question)
    answer = call_chat_completion(prompt)
    return answer or "Xin lỗi, tôi chưa trả lời được câu hỏi này."

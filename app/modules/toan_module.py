from app.gpt_api import call_chat_completion
from app.utils.prompt_builder import build_toan_prompt

def solve_toan(question):
    prompt = build_toan_prompt(question)
    answer = call_chat_completion(prompt)
    return answer or "Xin lỗi, tôi chưa trả lời được câu hỏi này."

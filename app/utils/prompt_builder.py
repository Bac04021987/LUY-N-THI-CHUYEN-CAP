def build_toan_prompt(question_text):
    return [
        {"role": "system", "content": "Bạn là trợ lý AI giúp học sinh lớp 5-6 giải Toán."},
        {"role": "user", "content": question_text},
    ]

def build_tiengviet_prompt(question_text):
    return [
        {"role": "system", "content": "Bạn là trợ lý AI giúp học sinh lớp 5-6 học môn Tiếng Việt."},
        {"role": "user", "content": question_text},
    ]

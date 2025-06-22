from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.modules.data_loader import DataLoader
from app.gpt_api import GPTClient

app = FastAPI(title="AI Agent Lớp 5 lên 6")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gpt_client = GPTClient()
data_loader = DataLoader()

@app.post("/api/get_test/")
async def get_test(request: Request):
    """
    API nhận yêu cầu lấy đề thi theo môn và cấp độ.
    """
    data = await request.json()
    subject = data.get("subject", "toan").lower()  # Mặc định Toán
    level = data.get("level", 1)  # Mặc định cấp độ 1

    if subject not in ["toan", "tieng_viet"]:
        return JSONResponse({"error": "Môn học không hợp lệ. Vui lòng chọn 'toan' hoặc 'tieng_viet'."}, status_code=400)

    tests = data_loader.load_subject_level(subject, level)
    if not tests:
        return JSONResponse({"error": f"Không tìm thấy đề thi phù hợp cho môn {subject} cấp độ {level}."}, status_code=404)

    test = tests[0]  # Lấy đề đầu tiên làm ví dụ

    messages = [
        {"role": "system", "content": f"Bạn là trợ lý giáo dục {subject.capitalize()} lớp 5 chuẩn bị thi lên lớp 6."},
        {"role": "user", "content": f"Giúp tôi mô tả đề thi {subject.capitalize()} cấp độ {level} với nội dung: {test.get('title', 'Không có tiêu đề')}"}
    ]

    response = gpt_client.chat_completion(messages)

    return {
        "subject": subject,
        "level": level,
        "test_id": test.get("id", "unknown"),
        "description": response
    }

@app.get("/")
async def root():
    return {"message": "Chào mừng đến với AI Agent ôn thi lớp 5 lên 6!"}

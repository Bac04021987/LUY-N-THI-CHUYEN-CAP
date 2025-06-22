from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.modules.data_loader import DataLoader
from app.gpt_api import GPTClient

app = FastAPI(title="AI Agent Lớp 5 lên 6")

# Cho phép truy cập từ frontend khác domain (nếu cần)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Khởi tạo client GPT và DataLoader
gpt_client = GPTClient()
data_loader = DataLoader()

@app.post("/api/get_math_test/")
async def get_math_test(request: Request):
    """
    API nhận yêu cầu lấy đề thi Toán theo cấp độ.
    """
    data = await request.json()
    level = data.get("level", 1)  # Mặc định cấp độ 1
    subject = "toan"

    # Load đề thi từ data_loader
    tests = data_loader.load_subject_level(subject, level)
    if not tests:
        return JSONResponse({"error": "Không tìm thấy đề thi phù hợp."}, status_code=404)

    # Lấy đề thi đầu tiên (ví dụ)
    test = tests[0]

    # Tạo prompt gửi GPT để mô tả đề thi
    messages = [
        {"role": "system", "content": "Bạn là trợ lý giáo dục Toán lớp 5 chuẩn bị thi lên lớp 6."},
        {"role": "user", "content": f"Giúp tôi mô tả đề thi Toán cấp độ {level} với nội dung: {test['title']}"}
    ]

    response = gpt_client.chat_completion(messages)

    return {"test_id": test.get("id", "unknown"), "description": response}

@app.get("/")
async def root():
    return {"message": "Chào mừng đến với AI Agent ôn thi lớp 5 lên 6!"}

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.modules.data_loader import DataLoader
from app.gpt_api import GPTClient
import logging

app = FastAPI(title="AI Agent Lớp 5 lên 6")

# Cấu hình logging cơ bản
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gpt_client = GPTClient()
data_loader = DataLoader()

VALID_SUBJECTS = {"toan", "tieng_viet"}
VALID_LEVELS = {1, 2, 3}

@app.post("/api/get_test/")
async def get_test(request: Request):
    """
    API nhận yêu cầu lấy đề thi theo môn và cấp độ.
    """
    try:
        data = await request.json()
        subject = data.get("subject", "toan").lower()
        level = data.get("level", 1)

        if subject not in VALID_SUBJECTS:
            logging.warning(f"Yêu cầu môn không hợp lệ: {subject}")
            return JSONResponse({"error": "Môn học không hợp lệ. Vui lòng chọn 'toan' hoặc 'tieng_viet'."}, status_code=400)

        if not isinstance(level, int) or level not in VALID_LEVELS:
            logging.warning(f"Yêu cầu cấp độ không hợp lệ: {level}")
            return JSONResponse({"error": "Cấp độ không hợp lệ. Vui lòng chọn cấp độ 1, 2 hoặc 3."}, status_code=400)

        tests = data_loader.load_subject_level(subject, level)
        if not tests:
            logging.info(f"Không tìm thấy đề thi phù hợp cho {subject} cấp độ {level}")
            return JSONResponse({"error": f"Không tìm thấy đề thi phù hợp cho môn {subject} cấp độ {level}."}, status_code=404)

        # Có thể trả về toàn bộ danh sách đề, hiện trả về đề đầu tiên
        test = tests[0]

        messages = [
            {"role": "system", "content": f"Bạn là trợ lý giáo dục {subject.capitalize()} lớp 5 chuẩn bị thi lên lớp 6."},
            {"role": "user", "content": f"Giúp tôi mô tả đề thi {subject.capitalize()} cấp độ {level} với nội dung: {test.get('title', 'Không có tiêu đề')}"}
        ]

        response = gpt_client.chat_completion(messages)

        return {
            "subject": subject,
            "level": level,
            "test_id": test.get("id", "unknown"),
            "description": response,
            "full_test": test  # Trả luôn toàn bộ đề nếu muốn
        }

    except Exception as e:
        logging.error(f"Lỗi xử lý yêu cầu /api/get_test/: {e}")
        return JSONResponse({"error": "Đã xảy ra lỗi trong quá trình xử lý."}, status_code=500)

@app.get("/")
async def root():
    return {"message": "Chào mừng đến với AI Agent ôn thi lớp 5 lên 6!"}

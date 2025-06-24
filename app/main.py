from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import logging
import time
from app.modules.data_loader import DataLoader
from app.gpt_api import GPTClient
import os

app = FastAPI(title="AI Agent Lớp 5 lên 6")

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

# Cấu hình thư mục chứa templates (HTML)
templates = Jinja2Templates(directory="app/ui/templates")

# Rate limiting đơn giản
rate_limit_window = 10
rate_limit_max = 5
rate_limit_data = {}

def rate_limit(ip: str):
    now = time.time()
    window_start = now - rate_limit_window
    if ip not in rate_limit_data:
        rate_limit_data[ip] = []
    rate_limit_data[ip] = [t for t in rate_limit_data[ip] if t > window_start]
    if len(rate_limit_data[ip]) >= rate_limit_max:
        return False
    rate_limit_data[ip].append(now)
    return True

def check_api_key(x_api_key: str = Header(None)):
    # Thay YOUR_SECRET_API_KEY bằng key thật trong biến môi trường API_KEY
    if x_api_key != os.getenv("API_KEY", "YOUR_SECRET_API_KEY"):
        raise HTTPException(status_code=401, detail="API Key không hợp lệ")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/get_test/")
async def get_test(request: Request, x_api_key: str = Header(None)):
    check_api_key(x_api_key)
    client_ip = request.client.host
    if not rate_limit(client_ip):
        logging.warning(f"Rate limit exceeded for IP: {client_ip}")
        return JSONResponse({"error": "Quá nhiều yêu cầu, vui lòng thử lại sau."}, status_code=429)

    try:
        data = await request.json()
        logging.info(f"Yêu cầu get_test từ IP {client_ip}: {data}")

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

        result = [{"id": t.get("id", "unknown"), "title": t.get("title", "Không có tiêu đề")} for t in tests]

        logging.info(f"Trả về danh sách đề thi: {result}")

        return {"subject": subject, "level": level, "tests": result}

    except Exception as e:
        logging.error(f"Lỗi xử lý yêu cầu /api/get_test/: {e}", exc_info=True)
        return JSONResponse({"error": "Đã xảy ra lỗi trong quá trình xử lý."}, status_code=500)

@app.post("/api/get_test_description/")
async def get_test_description(request: Request, x_api_key: str = Header(None)):
    check_api_key(x_api_key)
    client_ip = request.client.host
    if not rate_limit(client_ip):
        logging.warning(f"Rate limit exceeded for IP: {client_ip}")
        return JSONResponse({"error": "Quá nhiều yêu cầu, vui lòng thử lại sau."}, status_code=429)

    try:
        data = await request.json()
        logging.info(f"Yêu cầu get_test_description từ IP {client_ip}: {data}")

        subject = data.get("subject", "toan").lower()
        test_id = data.get("test_id")
        title = data.get("title") or data.get("test", {}).get("title")

        logging.info(f"subject={subject}, test_id={test_id}, title={title}")

        if subject not in VALID_SUBJECTS:
            return JSONResponse({"error": "Môn học không hợp lệ.

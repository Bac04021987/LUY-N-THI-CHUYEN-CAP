import os
import logging
from flask import Flask, request, jsonify, render_template, abort
from app.modules.toan_module import ToanModule
from app.modules.tieng_viet_module import TiengVietModule
from app.modules.hinh_hoc_module import HinhHocModule

# Thiết lập logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Khởi tạo Flask app
app = Flask(__name__)

# Khởi tạo các module môn học
toan = ToanModule()
tieng_viet = TiengVietModule()
hinh_hoc = HinhHocModule()

# API key lấy từ biến môi trường hoặc mặc định
API_KEY = os.getenv("API_KEY", "123456")

def check_api_key():
    key = request.headers.get("x-api-key")
    if not key or key != API_KEY:
        logger.warning("API key không hợp lệ hoặc thiếu.")
        abort(401, description="Unauthorized: API key missing or invalid")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/get_test_description", methods=["POST"])
def get_test_description():
    # Bật xác thực API key nếu muốn
    # check_api_key()

    data = request.json
    subject = data.get("subject")
    test = data.get("test")
    language = data.get("language", "vi").lower()

    if not subject or not test:
        return jsonify({"error": "Thiếu trường 'subject' hoặc 'test'"}), 400

    title = test.get("title")
    if not title:
        return jsonify({"error": "Trường 'title' trong 'test' không được để trống"}), 400

    try:
        if subject == "toan":
            toan.language = language
            description = toan.get_test_description(test)
        elif subject == "tieng_viet":
            tieng_viet.language = language
            description = tieng_viet.get_test_description(test)
        elif subject == "hinh_hoc":
            hinh_hoc.language = language
            description = hinh_hoc.get_test_description(test)
        else:
            return jsonify({"error": "Môn học không hợp lệ"}), 400

        return jsonify({"description": description})
    except Exception as e:
        logger.error(f"Lỗi xử lý API get_test_description: {e}")
        return jsonify({"error": "Lỗi server"}), 500

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)

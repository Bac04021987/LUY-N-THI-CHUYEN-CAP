from flask import Flask, request, jsonify, render_template_string
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load biến môi trường từ .env (nếu có)
load_dotenv()

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise Exception("Bạn chưa đặt biến môi trường OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# Giao diện HTML đơn giản với chọn môn học, input, nút gửi và vùng hiển thị kết quả
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8" />
    <title>AI Agent - Luyện thi Toán & Tiếng Việt lớp 5,6</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 30px; background: #f9f9f9; }
        h1 { text-align: center; }
        select, input[type=text] {
            width: 100%; padding: 10px; margin: 10px 0; box-sizing: border-box; font-size: 16px;
        }
        button {
            width: 100%; padding: 12px; background: #007bff; color: white; font-size: 18px;
            border: none; border-radius: 5px; cursor: pointer;
        }
        button:hover { background: #0056b3; }
        #responseBox {
            margin-top: 20px; padding: 15px; background: white; min-height: 150px;
            border: 1px solid #ccc; border-radius: 5px; white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <h1>AI Agent - Luyện thi Toán & Tiếng Việt lớp 5,6</h1>

    <label for="subject">Chọn môn học:</label>
    <select id="subject">
        <option value="toan">Toán</option>
        <option value="tieng_viet">Tiếng Việt</option>
    </select>

    <input type="text" id="prompt" placeholder="Nhập câu hỏi..." />

    <button id="sendBtn">Gửi</button>

    <div id="responseBox">Không có phản hồi.</div>

    <script>
        document.getElementById("sendBtn").addEventListener("click", async () => {
            const subject = document.getElementById("subject").value;
            const prompt = document.getElementById("prompt").value.trim();
            const responseBox = document.getElementById("responseBox");

            if (!prompt) {
                alert("Vui lòng nhập câu hỏi.");
                return;
            }

            responseBox.textContent = "Đang xử lý...";

            try {
                const res = await fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ subject, prompt })
                });

                const data = await res.json();
                if (data.response) {
                    responseBox.textContent = data.response;
                } else if (data.error) {
                    responseBox.textContent = "Lỗi: " + data.error;
                } else {
                    responseBox.textContent = "Không có phản hồi.";
                }
            } catch (error) {
                responseBox.textContent = "Lỗi kết nối: " + error.message;
            }
        });
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    subject = data.get("subject", "").strip()
    prompt = data.get("prompt", "").strip()

    if subject not in ("toan", "tieng_viet"):
        return jsonify({"error": "Môn học không hợp lệ."}), 400
    if not prompt:
        return jsonify({"error": "Không có câu hỏi."}), 400

    # Tạo nội dung system message dựa trên môn học
    system_msg = f"Bạn là trợ lý AI luyện thi {subject}. Hãy trả lời câu hỏi sau rõ ràng, ngắn gọn."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({"response": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

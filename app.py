from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise Exception("Bạn chưa đặt biến môi trường OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Không có câu hỏi"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Bạn là trợ lý AI."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        answer = response.choices[0].message.content
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return """
    <h2>AI Agent đơn giản trên Render</h2>
    <form id="chatForm">
      <input type="text" name="prompt" placeholder="Nhập câu hỏi..." style="width:300px" required />
      <button type="submit">Gửi</button>
    </form>
    <pre id="result"></pre>
    <script>
      const form = document.getElementById('chatForm');
      const result = document.getElementById('result');
      form.addEventListener('submit', async e => {
        e.preventDefault();
        const prompt = form.prompt.value;
        const res = await fetch('/chat', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({prompt})
        });
        const data = await res.json();
        if(data.response) result.textContent = data.response;
        else result.textContent = "Lỗi: " + (data.error || "Không rõ");
      });
    </script>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

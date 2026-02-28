import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = Flask(__name__)

SYSTEM_PROMPT = """
Sen Altınyıldız için çalışan kıdemli AI entegrasyon mimarısın.

Şu formatta cevap ver:

1. İhtiyaç Analizi
2. Profesyonel Prompt
3. Entegrasyon Planı
4. Teknik Mimari
"""

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    if request.method == "POST":
        user_input = request.form.get("user_input")
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        response_text = completion.choices[0].message.content
    return render_template("index.html", response=response_text)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_input = data.get("user_input", "")
    return jsonify({"content": user_input})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
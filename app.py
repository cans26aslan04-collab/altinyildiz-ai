import os
from flask import Flask, render_template, request
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
    sonuc = ""

    if request.method == "POST":
        fikir = request.form["fikir"]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": fikir}
            ]
        )

        sonuc = response.choices[0].message.content

    return render_template("index.html", sonuc=sonuc)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "Kullanıcıya net, araştırma önerisi vermeden doğrudan detaylı bilgi ver. Akademik ama anlaşılır anlat."
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
)
{
  "role": "system",
  "content": "Kullanıcı istediğinde başlık ve madde madde slayt formatında içerik üret. Her slaytı ayrı başlıkla yaz."
}
from flask import Flask, render_template, request
from openai import OpenAI
import requests
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def home():
    response_text = None

    if request.method == "POST":
        user_input = request.form["user_input"]

        # --- Canlı veri çekme (hayali moda API) ---
        try:
            api_response = requests.get("https://modaapi.com/trends?category=jacket")
            api_data = api_response.json()  # Örnek: {"trends": ["Oversize", "Leather", "Bomber"]}
        except Exception as e:
            api_data = {"trends": ["Oversize", "Leather", "Bomber"]}  # fallback
            print("API hatası:", e)

        # --- Modeli bilgilendir ve direkt cevap üretmesini sağla ---
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sen moda uzmanısın. Kullanıcıya sorulan konuda "
                        "doğrudan, detaylı ve net cevap ver. "
                        "Veriyi kaynağından almış gibi sun. "
                        "Asla 'araştırabilirsin' veya 'kontrol et' deme."
                    )
                },
                {
                    "role": "user",
                    "content": f"{user_input}\nGüncel trendler: {api_data['trends']}"
                }
            ]
        )

        response_text = completion.choices[0].message.content

    return render_template("index.html", response=response_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
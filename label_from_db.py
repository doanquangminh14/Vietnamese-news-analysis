import time
import json
import re
from groq import Groq
from dotenv import load_dotenv
import os

from data import get_unprocessed_articles, insert_processed_article

# ================= CONFIG =================
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

VALID_SENTIMENT = ["Positive", "Negative", "Neutral"]
VALID_INTENT = ["Informational", "Warning", "Promotional"]


def build_prompt(text):
    return f"""
    Trả về JSON:

    {{
      "sentiment": "Positive | Negative | Neutral",
      "intent": "Informational | Warning | Promotional"
    }}

    Chỉ trả JSON.

    Bài báo:
    {text}
    """

def parse_json(text):
    try:
        match = re.search(r'\{.*?\}', text, re.DOTALL)
        if not match:
            return "Unknown", "Unknown"

        data = json.loads(match.group())

        s = data.get("sentiment", "").capitalize()
        i = data.get("intent", "").capitalize()

        if s not in VALID_SENTIMENT:
            s = "Unknown"
        if i not in VALID_INTENT:
            i = "Unknown"

        return s, i
    except:
        return "Unknown", "Unknown"

def get_label(content):
    try:
        res = client.chat.completions.create(
            messages=[{"role": "user", "content": build_prompt(content[:1000])}],
            model="llama-3.1-8b-instant",
            temperature=0
        )
        return parse_json(res.choices[0].message.content)
    except Exception as e:
        print("LLM lỗi:", e)
        return "Error", "Error"

def run():
    print(" Bắt đầu labeling từ DB...")

    rows = get_unprocessed_articles(limit=20)

    if not rows:
        print(" Không còn bài nào cần xử lý")
        return

    for row in rows:
        article_id = row[0]
        title = row[1]
        content = row[2]

        print(f" Đang xử lý ID {article_id}")

        sentiment, intent = get_label(content)

        insert_processed_article(article_id, sentiment, intent)

        time.sleep(2)

    print(" Done labeling!")

if __name__ == "__main__":
    run()
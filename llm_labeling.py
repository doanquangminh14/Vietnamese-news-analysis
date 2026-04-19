import pandas as pd 
import google.generativeai as genai
import crawler 
import os 
import time
from groq import Groq
from dotenv import load_dotenv

def build_prompt(text, category):
    if category == "Thể thao":
        instruction = """
        Phân loại cảm xúc:
        - Khen
        - Chê
        - Trung lập
        """
    elif category == "Kinh doanh":
        instruction = """
        Bài báo có mang tính quảng bá / định hướng mua sản phẩm không:
        - Có
        - Không
        """
    elif category == "Sức khỏe":
        instruction = """
        Phân loại:
        - Cảnh báo
        - Thông tin
        - Tích cực
        """
    else:  # Thế giới
        instruction = """
        Phân loại tone:
        - Tích cực
        - Tiêu cực
        - Trung lập
        """
        
    prompt = f"""
    Bạn là chuyên gia phân tích báo chí.
    {instruction}
    Quy tắc:
    - Chỉ trả về đúng 1 nhãn
    - Không giải thích
    Bài báo:
    {text}
    """
    return prompt



load_dotenv() 
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


def get_label(text, category):
    text_short = str(text)[:1000]
    prompt = build_prompt(text_short, category)
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant", 
            temperature=0,
        )
        return chat_completion.choices[0].message.content.strip().capitalize()
    except Exception as e:
        print(f"Lỗi Groq: {e}")
        return "Lỗi"


#Index = Số thứ tự của hàng (0, 1, 2...).

#Column = Tên của các cột (Category, Title...).

#Row = Chứa cả NỘI DUNG và BIẾT RÕ nội dung đó thuộc CỘT NÀO. Đó là lý do bạn có thể gõ row['Category'] để lôi chữ "Thể thao" ra ngoài!
    
def run():
    input_file = os.path.join("data_output", "vnexpress_data_clean.csv")
    df = pd.read_csv(input_file)
    print("Đang đọc dữ liệu!!!")
    labels = []
    for index, row in df.iterrows():
        print(f"Đang xử lý bài {index}...")
        label = get_label(row['Text_Segmented'], row['Category'])
        labels.append(label)
        time.sleep(4)
    df['AI_Insight'] = labels
    
    output_file = os.path.join("data_output", "vnexpress_ai_insight.csv")
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print("\n--- KẾT QUẢ PHÂN TÍCH ---")
    print(df[['Category', 'AI_Insight', 'Title']].head(10))
    
if __name__ == "__main__":
    run()
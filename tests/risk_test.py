import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

clause = "使用者上傳之內容，本公司有權永久保存並用於商業用途。"

prompt = f"""請依以下規則分析這段條文是否「須注意」或為「一般資訊」，並說明原因。

【須注意】
- 條文包含不公平條款、限制使用者權利、強制授權、免責、或個資利用，請標示為「須注意」

【一般資訊】
- 條文若僅是描述、規格、聲明、定義等常見內容，則標示為「一般資訊」

請使用以下 JSON 格式回覆：
{{
  "clause": "{clause}",
  "risk_level": "須注意 / 一般資訊",
  "type": "類型簡述",
  "reason": "簡要說明"
}}
"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "你是一個合約條款判讀工具"},
        {"role": "user", "content": prompt}
    ],
    temperature=0.3
)

print("GPT 回傳：")
print(response.choices[0].message.content)

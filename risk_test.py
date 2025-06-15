import openai
import os
from dotenv import load_dotenv

# 載入 .env 檔案中的 API 金鑰
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = api_key

# 測試條款句子
clause = "使用者上傳之內容，本公司有權永久保存並用於商業用途。"

# Prompt 模板
prompt = f"""請判斷以下條款是否存在使用者風險，若有請標示風險等級（高、中），說明理由與風險類型；
若無風險，請說明為何屬於一般正常條款，並標示為「無風險」。

條款：「{clause}」

請用以下 JSON 格式回覆：
{{
  "risk_level": "高 / 中 / 無風險",
  "risk_type": "（風險類型或無）",
  "reason": "簡要說明原因",
  "clause_text": "{clause}",
  "language": "zh"
}}"""

# 呼叫 GPT
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "你是一個合約條款風險判讀工具"},
        {"role": "user", "content": prompt}
    ],
    temperature=0.3
)

print("GPT 回傳：")
print(response.choices[0].message.content)

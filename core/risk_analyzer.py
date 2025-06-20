# risk_analyzer.py（整合 GPT 分析）
import os
import json
import openai
from dotenv import load_dotenv

# 載入 .env 環境變數
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 提示語讀取（中英文）
def load_prompt(lang):
    prompt_path = f"prompts/prompt_template_{lang}.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

# 呼叫 OpenAI 分析條文
def gpt_analyze(clause, lang):
    prompt = load_prompt(lang)
    full_prompt = f"{prompt}\n\n條文：{clause}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一位條款風險分析助手"},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.3,
            timeout=10
        )
        text = response['choices'][0]['message']['content']
        print("📥 GPT 回傳內容：", text)  # 除錯用
        result = json.loads(text)
        result["clause"] = clause  # 確保原文保留
        return result
    except Exception as e:
        print(f"⚠️ GPT API 分析失敗，使用模擬模式：{e}")
        return mock_analyze(clause, lang)

# 模擬模式（備用）
def mock_analyze(clause, lang):
    return {
        "clause": clause,
        "risk_level": "中",
        "type": "已同意權",
        "reason": "模擬風險結果（未連接 GPT）"
    }

# 對外函式

def analyze_clause(clause, lang):
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return gpt_analyze(clause, lang)
    else:
        return mock_analyze(clause, lang)

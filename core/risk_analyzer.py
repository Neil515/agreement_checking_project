# risk_analyzer.py（整合 GPT 分析）
import os
import json
import re
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

# 判斷是否為上下文句子（非條款類）
def is_contextual_sentence(sentence: str) -> bool:
    if sentence.isupper():
        return True
    if re.match(r'^\s*(Definitions|Section|Contact|Welcome|This agreement)', sentence, re.I):
        return True
    if len(sentence) < 15 and not re.search(r'\b(is|are|shall|must|will)\b', sentence):
        return True
    if re.search(r'visit our website|for more info', sentence, re.I):
        return True
    return False

# 判斷是否缺乏高風險關鍵組合（中英文分流）
KEYWORD_COMBINATIONS_EN = [
    ["terminate", "without"],
    ["release", "liability"],
    ["solely", "liable"],
    ["not", "responsible"],
    ["grant", "permission"],
    ["exclusive", "rights"],
    ["without", "consent"],
    ["agree", "indemnify"]
]

KEYWORD_COMBINATIONS_ZH = [
    ["終止", "契約"],
    ["違約", "金"],
    ["解除", "合約"],
    ["賠償", "責任"],
    ["不再", "追償"]
]

def lacks_high_risk_combinations(sentence: str, lang: str) -> bool:
    sentence_lower = sentence.lower()
    keyword_combos = KEYWORD_COMBINATIONS_ZH if lang == "zh" else KEYWORD_COMBINATIONS_EN
    for combo in keyword_combos:
        if all(word in sentence_lower for word in combo):
            return False
    return True

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
        text = response['choices'][0]['message']['content'].strip()
        # 自動去除包裹的程式碼區塊符號（強化）
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)

        print("📅 GPT 回傳內容：", text)  # 除錯用
        result = json.loads(text)
        result["clause"] = clause  # 確保原文保留

        # 套用 highlight 標記邏輯
        if result.get("risk_level") in ["高", "須注意"]:
            result["risk_level"] = "須注意"
            result["highlight"] = True
        else:
            result["risk_level"] = "一般資訊"
            result["highlight"] = False

        return result
    except Exception as e:
        print(f"⚠️ GPT API 分析失敗，使用模擬模式：{e}")
        return mock_analyze(clause, lang)

# 模擬模式（備用）
def mock_analyze(clause, lang):
    return {
        "clause": clause,
        "risk_level": "須注意",
        "type": "已同意權",
        "reason": "模擬風險結果（未連接 GPT）",
        "highlight": True
    }

# 對外函式
def analyze_clause(clause, lang):
    if is_contextual_sentence(clause):
        return {
            "clause": clause,
            "risk_level": "一般資訊",
            "type": "Contextual",
            "reason": "Contextual sentence (e.g., definition, heading, or background info)",
            "highlight": False
        }

    if lacks_high_risk_combinations(clause, lang):
        return {
            "clause": clause,
            "risk_level": "一般資訊",
            "type": "Informative",
            "reason": "No high-risk keyword combinations detected",
            "highlight": False
        }

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return gpt_analyze(clause, lang)
    else:
        return mock_analyze(clause, lang)

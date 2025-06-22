# core/risk_analyzer.py（改為動態 few-shot 組合範例）
import os
import json
import re
import openai
from dotenv import load_dotenv

# 載入 .env 環境變數
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 固定說明語（不含範例）
INSTRUCTION_ZH = """
請你協助判斷以下條文是否屬於「須注意」的合約條款。
分析標準如下：
- 僅當條文對某一方施加了明確的不公平條件、過度義務、限制權利，或存在潛在法律爭議時，才視為「須注意」。
- 其他屬於常規描述、背景說明、常見資訊者，請標記為「一般資訊」。
回傳格式：{\"clause\":..., \"risk_level\":..., \"type\":..., \"reason\":...}
"""

# 範例清單（Few-shot）
FEW_SHOT_EXAMPLES_ZH = [
    {
        "clause": "本契約雙方應善意協商處理合約未盡事宜。",
        "risk_level": "一般資訊",
        "type": "常規義務",
        "reason": "為常見合作條款，未涉及單方限制或風險"
    },
    {
        "clause": "甲方有權隨時修改本服務條款，並不另行通知乙方。",
        "risk_level": "須注意",
        "type": "單方變更條款",
        "reason": "條款允許甲方片面變更合約內容，且未保障乙方知情權"
    },
    {
        "clause": "乙方同意授權甲方無償使用其上傳資料用於行銷用途。",
        "risk_level": "須注意",
        "type": "資訊使用授權",
        "reason": "授權條款用途過於廣泛，且無償，可能造成資訊控制不對等"
    }
]

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

# 關鍵組合過濾（略）
KEYWORD_COMBINATIONS_ZH = [["終止", "契約"], ["違約", "金"], ["解除", "合約"], ["賠償", "責任"], ["不再", "追償"]]

def lacks_high_risk_combinations(sentence: str, lang: str) -> bool:
    sentence_lower = sentence.lower()
    for combo in KEYWORD_COMBINATIONS_ZH if lang == "zh" else []:
        if all(word in sentence_lower for word in combo):
            return False
    return True

# GPT 分析主程式（用動態 few-shot prompt）
def gpt_analyze(clause, lang):
    if lang != "zh":
        raise ValueError("目前僅支援中文模式")

    few_shot_prompt = INSTRUCTION_ZH.strip() + "\n\n"
    for ex in FEW_SHOT_EXAMPLES_ZH:
        few_shot_prompt += f"條文：{ex['clause']}\n輸出：{json.dumps(ex, ensure_ascii=False)}\n\n"
    few_shot_prompt += f"條文：{clause}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一位條款風險分析助手"},
                {"role": "user", "content": few_shot_prompt.strip()}
            ],
            temperature=0.3,
            timeout=10
        )
        text = response['choices'][0]['message']['content'].strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\\s*", "", text)
            text = re.sub(r"\\s*```$", "", text)
        print("📅 GPT 回傳內容：", text)
        result = json.loads(text)
        result["clause"] = clause
        result["risk_level"] = "須注意" if result.get("risk_level") in ["高", "須注意"] else "一般資訊"
        result["highlight"] = result["risk_level"] == "須注意"
        return result

    except Exception as e:
        print(f"⚠️ GPT API 分析失敗，使用模擬模式：{e}")
        return mock_analyze(clause, lang)

# 模擬模式

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
            "reason": "Contextual sentence (e.g., heading or background info)",
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
    return gpt_analyze(clause, lang)

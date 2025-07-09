import os
import json
import re
import openai
from dotenv import load_dotenv

# 載入 .env 環境變數
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 讀取風險類型對照表
with open("data/risk_type_mapping.json", encoding="utf-8") as f:
    TYPE_MAPPING_DICT = json.load(f)

# 讀取主分類對照表
with open("data/standard_type_mapping.json", encoding="utf-8") as f:
    STANDARD_TYPE_MAPPING = json.load(f)

# 固定說明語（不含範例）
INSTRUCTION_ZH = """
請你協助判斷以下條文是否屬於「須注意」的合約條款。
分析標準如下：
- 僅當條文對某一方施加了明確的不公平條件、過度義務、限制權利，或存在潛在法律爭議時，才視為「須注意」。
- 其他屬於常規描述、背景說明、常見資訊者，請標記為「一般資訊」。
回傳格式：{\"clause\":..., \"risk_level\":..., \"type\":..., \"reason\":...}
"""

INSTRUCTION_EN = """
Please help assess whether the following clause is a "Risky Clause".
Evaluation criteria:
- Only clauses that clearly impose unfair conditions, excessive obligations, restrict rights, or pose potential legal issues should be marked as "Risky".
- Clauses that are common, informative, or standard legal language should be marked as "General Information".
Return format: {"clause":..., "risk_level":..., "type":..., "reason":...}
"""

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

FEW_SHOT_EXAMPLES_EN = [
    {
        "clause": "The parties agree to act in good faith to resolve any matters not covered by this agreement.",
        "risk_level": "General Information",
        "type": "Standard Obligation",
        "reason": "This is a typical cooperation clause without imposing one-sided risks."
    },
    {
        "clause": "The Company reserves the right to modify these terms at any time without prior notice.",
        "risk_level": "Risky",
        "type": "Unilateral Modification",
        "reason": "Clause allows unilateral changes without informing the user, which may be unfair."
    },
    {
        "clause": "User grants the service provider a perpetual, royalty-free license to use uploaded content for marketing purposes.",
        "risk_level": "Risky",
        "type": "Data Usage",
        "reason": "The usage scope is too broad and royalty-free, possibly causing imbalance in information control."
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

# GPT 分析主程式（已優化）
def gpt_analyze(clause, lang):
    instruction = INSTRUCTION_ZH if lang == "zh" else INSTRUCTION_EN
    examples = FEW_SHOT_EXAMPLES_ZH if lang == "zh" else FEW_SHOT_EXAMPLES_EN

    prompt = instruction.strip() + "\n\n"
    for ex in examples:
        prompt += f"Clause: {ex['clause']}\nOutput: {json.dumps(ex, ensure_ascii=False)}\n\n"
    prompt += f"Clause: {clause}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a contract clause risk analysis assistant."},
                {"role": "user", "content": prompt.strip()}
            ],
            temperature=0.3,
            timeout=20
        )
        text = response['choices'][0]['message']['content'].strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\\s*", "", text)
            text = re.sub(r"\\s*```$", "", text)
        print("📅 GPT 回傳內容：", text)
        result = json.loads(text)
        result["clause"] = clause

        RISK_LEVEL_MAP = {
            "Risky": {"zh": "須注意", "en": "Risky"},
            "General Information": {"zh": "一般資訊", "en": "General Information"},
            "須注意": {"zh": "須注意", "en": "Risky"},
            "一般資訊": {"zh": "一般資訊", "en": "General Information"}
        }

        raw_risk = result.get("risk_level", "")
        raw_type = result.get("type", "")
        result["risk_level"] = RISK_LEVEL_MAP.get(raw_risk, {"zh": raw_risk, "en": raw_risk})
        is_risky = result["risk_level"]["zh"] == "須注意"

        if is_risky:
            type_info = TYPE_MAPPING_DICT.get(raw_type)
            if not type_info:
                print(f"⚠️ 無法在 risk_type_mapping.json 中找到類型對應：{raw_type}")
            type_en = type_info["en"] if type_info else "Unmapped"
            type_main = map_to_main_type(raw_type)
            type_main_en = STANDARD_TYPE_MAPPING.get(type_main, {}).get("en") or "Unmapped"
        else:
            type_en = raw_type
            type_main = None
            type_main_en = None

        result["type"] = {"zh": raw_type, "en": type_en}
        result["type_main"] = {"zh": type_main, "en": type_main_en} if type_main else None
        result["highlight"] = is_risky

        return result

    except Exception as e:
        print(f"⚠️ GPT API 分析失敗，使用模擬模式：{e.__class__.__name__}: {str(e)}")
        return mock_analyze(clause, lang)

# 模擬模式
def mock_analyze(clause, lang):
    return {
        "clause": clause,
        "risk_level": {"zh": "須注意", "en": "Risky"},
        "type": {"zh": "模擬結果", "en": "Mock Result"},
        "reason": "模擬風險結果（未連接 GPT）",
        "highlight": True,
        "type_main": {"zh": "模擬分類", "en": "Mock Category"}
    }

# 風險類型 → 主分類 對應
def map_to_main_type(risk_type):
    if not isinstance(risk_type, str):
        return None
    for keyword, main in {
        "單方": "單方決策與變更條款",
        "變更": "單方決策與變更條款",
        "定價": "單方決策與變更條款",
        "終止": "單方決策與變更條款",
        "付款": "付款與退費條款",
        "退款": "付款與退費條款",
        "費用": "付款與退費條款",
        "資訊": "資料與帳號權限",
        "資料": "資料與帳號權限",
        "帳號": "資料與帳號權限",
        "創作": "智慧財產與使用授權",
        "IP": "智慧財產與使用授權",
        "內容": "智慧財產與使用授權",
        "賠償": "法律責任與賠償",
        "責任": "法律責任與賠償",
        "法律": "法律責任與賠償",
        "消費者": "權益剝奪與限制",
        "放棄": "權益剝奪與限制",
        "限制": "權益剝奪與限制",
        "言論": "內容與言論審查",
        "爭議": "解釋與爭議解決",
        "條文": "解釋與爭議解決",
        "選擇權": "特殊角色條款"
    }.items():
        if keyword in risk_type:
            return main
    return None

# 對外函式
def analyze_clause(clause, lang):
    if is_contextual_sentence(clause):
        return {
            "clause": clause,
            "risk_level": {"zh": "一般資訊", "en": "General Information"},
            "type": {"zh": "上下文內容", "en": "Contextual"},
            "reason": "Contextual sentence (e.g., heading or background info)",
            "highlight": False,
            "type_main": None
        }
    return gpt_analyze(clause, lang)

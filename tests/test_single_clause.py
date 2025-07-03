from core.lang_detect import detect_language
from core.risk_analyzer import analyze_clause

# ✅ 測試條文（你可以換成中文條文試試）
clause = "甲方有權單方面終止本合約，且無需說明理由或提前通知乙方，乙方應無條件接受此結果。"

# 🔍 自動判斷語言
language = detect_language(clause)
print(f"Detected language: {language}")

# 🧠 執行 GPT 條文分析
result = analyze_clause(clause, language)

# 📋 印出分析結果
from pprint import pprint
print("\nAnalysis Result:")
pprint(result)

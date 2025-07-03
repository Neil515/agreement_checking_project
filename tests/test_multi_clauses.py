import os
import json
from core.lang_detect import detect_language
from core.risk_analyzer import analyze_clause
from core.split_text import split_into_clauses

# ✅ 載入測試原始條文檔案（純文字）
INPUT_PATH = "tests/full_agreement.txt"
OUTPUT_PATH = "outputs/full_agreement_analysis.json"

with open(INPUT_PATH, encoding="utf-8") as f:
    full_text = f.read()

# 🧩 自動切段（可改為自定義分段）
clauses = split_into_clauses(full_text)

results = []

for i, clause in enumerate(clauses, 1):
    if len(clause.strip()) < 10:
        continue
    lang = detect_language(clause)
    result = analyze_clause(clause, lang)
    result["clause_id"] = f"C{i}"
    results.append(result)

# 💾 儲存分析結果為 JSON
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"✅ 分析完成，共處理 {len(results)} 條條文，結果已儲存至 {OUTPUT_PATH}")

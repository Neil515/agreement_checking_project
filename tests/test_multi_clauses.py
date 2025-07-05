import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from core.lang_detect import detect_language
from core.risk_analyzer import analyze_clause
from core.split_text import split_sentences

# ✅ 載入測試原始條文檔案（純文字）
INPUT_PATH = "tests/full_agreement-2.txt"
OUTPUT_PATH = "outputs/full_agreement_analysis.json"

with open(INPUT_PATH, encoding="utf-8") as f:
    full_text = f.read()

# 🧩 偵測語言並切段
lang = detect_language(full_text)
clauses = split_sentences(full_text, lang)
print(f"📄 原始段落數：{len(clauses)}")  # 斷句前提示

results = []

for i, clause in enumerate(clauses, 1):
    if len(clause.strip()) < 10:
        continue
    try:
        result = analyze_clause(clause, lang)
        result["clause_id"] = f"C{i}"
        results.append(result)
    except Exception as e:
        print(f"❌ 條文分析失敗（C{i}）：{e}")
        continue

# 💾 儲存分析結果為 JSON
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"✅ 分析完成，共處理 {len(results)} 條條文（略過短句與異常），結果已儲存至 {OUTPUT_PATH}")

# 🔍 預覽前兩筆結果
print(json.dumps(results[:2], ensure_ascii=False, indent=2))

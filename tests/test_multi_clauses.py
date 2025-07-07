import sys
import os
import json
from core.lang_detect import detect_language
from core.risk_analyzer import analyze_clause
from core.split_text import split_sentences

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ✅ 測試檔案路徑
INPUT_PATH = "tests/full_agreement-2.txt"
OUTPUT_PATH = "outputs/full_agreement_analysis_debug.json"

with open(INPUT_PATH, encoding="utf-8") as f:
    full_text = f.read()

# 🧩 語言偵測與切句
lang = detect_language(full_text)
clauses = split_sentences(full_text, lang)
print(f"📄 原始段落數：{len(clauses)}")

results = []

for i, clause in enumerate(clauses, 1):
    clause = clause.strip()
    if len(clause) < 10:
        continue

    result = {
        "clause_id": f"C{i}",
        "clause_text": clause,
        "language": lang,
        "flag": ""
    }

    try:
        analysis = analyze_clause(clause, lang)
        result.update(analysis)

        # 自動標記可疑錯誤（示例：句子太短、未含關鍵動詞等）
        if len(clause) < 20:
            result["flag"] = "句長過短，可能被誤切"
        elif clause.count("。") > 2 or clause.count("；") > 2:
            result["flag"] = "句子可能未切分"

    except Exception as e:
        result["risk_level"] = "ERROR"
        result["reason"] = str(e)
        result["flag"] = "分析失敗"

    results.append(result)

# 💾 存成 JSON 方便人檢查
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"✅ 分析完成，共 {len(results)} 條條文，結果存至 {OUTPUT_PATH}")
print(json.dumps(results[:2], ensure_ascii=False, indent=2))

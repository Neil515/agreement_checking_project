import json
import os

# 載入風險類型對照表
with open("data/risk_type_mapping.json", "r", encoding="utf-8") as f:
    en_to_zh = json.load(f)
    zh_to_en = {v: k for k, v in en_to_zh.items()}

# 要處理的檔案清單
files = ["data/risk_examples.json", "data/whitelist_examples.json"]

for path in files:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        original_type = entry.get("type")

        if isinstance(original_type, dict):
            zh = original_type.get("zh", "")
            en = original_type.get("en", "")
            if zh in zh_to_en:
                en = zh_to_en[zh]
            elif en in en_to_zh:
                zh = en_to_zh[en]
            entry["type"] = {"zh": zh, "en": en}

        elif isinstance(original_type, str):
            zh = original_type if original_type in zh_to_en else "未知"
            en = zh_to_en.get(zh, original_type)
            entry["type"] = {"zh": zh, "en": en}

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ {path} 已轉換完成")

import json

# 風險類型對照表（中文為 key）
with open("data/risk_type_mapping.json", "r", encoding="utf-8") as f:
    zh_type_map = json.load(f)

zh_to_en_type = {zh: v["en"] for zh, v in zh_type_map.items()}

# 風險等級對照表
risk_level_mapping = {
    "須注意": "Warning",
    "一般資訊": "Informational",
    "高風險": "High Risk"
}

# 要處理的檔案清單
files = ["data/risk_examples.json", "data/whitelist_examples.json"]

for path in files:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        # 轉換 type 欄位
        original_type = entry.get("type")
        if isinstance(original_type, dict):
            zh = original_type.get("zh", "")
            en = zh_to_en_type.get(zh, original_type.get("en", "Unknown"))
            entry["type"] = {"zh": zh, "en": en}
        elif isinstance(original_type, str):
            zh = original_type
            en = zh_to_en_type.get(zh, "Unknown")
            entry["type"] = {"zh": zh, "en": en}

        # 轉換 risk_level 欄位
        original_level = entry.get("risk_level")
        en_level = risk_level_mapping.get(original_level, "Unknown")
        entry["risk_level"] = {"zh": original_level, "en": en_level}

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ {path} 已轉換完成")

import json

# 分類名稱對照表：將多種同義分類合併為統一名稱
TYPE_MAPPING = {
    "不對等賠償責任": "賠償條款",
    "過度賠償義務": "賠償條款",
    "資訊使用授權": "資訊再利用",
    "內容再利用條款": "資訊再利用",
    "資料再利用條款": "資訊再利用",
    "智慧財產權轉讓": "創作內容權利",
    "創作成果歸屬不當": "創作內容權利",
    "單方裁量條款": "單方決定條款",
    "單方修正條款": "單方決定條款",
    "單方替換條款": "單方決定條款",
    "強制更新條款": "強制升級條款",
    "模糊懲處條款": "單方決定條款",
    "資料控制限制": "資料限制條款",
    "帳號控制權過度": "帳號與資料權限",
    "帳號資料刪除": "帳號與資料權限",
    "退款權全面放棄": "消費者權益剝奪",
    "消保權限縮小": "消費者權益剝奪",
    "語言優先條款": "法律適用偏向",
    "法律適用排除": "法律適用偏向",
    "全面免責條款": "責任限制條款",
    "不可抗力責任擴張": "責任限制條款",
    "使用者貢獻轉讓": "創作內容權利",
    "建議權益剝奪": "創作內容權利",
    "言論限制條款": "言論限制條款",
    "資訊監控條款": "監控與資訊條款",
    "語音監控條款": "監控與資訊條款",
    "通訊紀錄用途不當": "監控與資訊條款",
    "資料保存無限制": "資料限制條款",
    "廣告插入權利": "使用介面控制",
    "客服處理限制": "使用者支援限制",
    "溯及變更條款": "單方決定條款",
    "內容保存禁令": "資料限制條款",
    "個人肖像授權": "個資與肖像權",
    "解釋排除條款": "條文解釋限制",
    "默示同意條款": "條文解釋限制",
    "訴訟權限制": "法律救濟限制",
    "資源限制條款": "使用限制條款",
    "過度責任轉嫁": "賠償條款",
    "公開處分條款": "單方決定條款",
    "過度權利保留": "單方決定條款",
    "推薦責任排除": "責任限制條款",
    "投訴排除條款": "使用者支援限制",
    "政策可溯及修正": "單方變更條款",
    "開發者專屬條款": "特殊角色優待",
    "類型待確認": "待人工審核",
    "類型混用": "待人工審核",
    "類型不明確": "待人工審核"
}

with open("data/risk_examples.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    original_type = item.get("type", "")
    mapped_type = TYPE_MAPPING.get(original_type, original_type)
    item["type"] = mapped_type

with open("data/risk_examples_mapped.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ 分類名稱已標準化並輸出為 risk_examples_mapped.json")

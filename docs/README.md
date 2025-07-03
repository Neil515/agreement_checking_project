# AI 合約條款風險分析工具

這是一個基於 GPT 模型的自動合約條款風險偵測工具，協助使用者快速分析中英文合約條文，辨識潛在須注意條款，並以 JSON 格式回傳結果。支援語言辨識、風險分類標註、中英對照輸出，前後端報表可切換語系顯示，適合用於風險預警與可視化分析。

---

## ✅ 最新進度整理（更新：2025-07-02）

### 📌 今日進度總結

1. **核心模組改寫支援中英文格式**：
   - `risk_analyzer.py` 輸出 `type` 與 `risk_level` 改為 `{zh, en}` 結構
   - 類型欄位從 `risk_type_mapping.json` 自動補上英文名稱，未對應者會 log 警示

2. **建立兩套測試腳本：**
   - `test_single_clause.py`：手動貼單條條文做格式確認（適合 Debug 測試）
   - `test_multi_clauses.py`：可分析整段或整篇 `.txt` 條文，自動切句與分析，輸出 JSON 結果

3. **保留 `test_risk_cases_runner_dual.py` 作為測資驗證工具**：
   - 僅適用已分類好的測資（如黑白名單）
   - 可比對 GPT 分類與預期類型

4. **風險類型對照資料更新：**
   - `risk_type_mapping.json` 新增「單方終止條款」對應英文名稱：`Unilateral Termination Clause`

---

## 📁 專案架構概覽

```
├── core/                  # 核心模組：clean_text, lang_detect, risk_analyzer
├── prompts/              # GPT 提示語模板（中英文）
├── data/                 # 測資來源與類型對照表
├── tools/                # 欄位補齊與格式轉換工具
├── tests/                # 單條測試、多條分析、黑白名單驗證模組
├── outputs/              # 分析結果儲存 JSON
├── report_template.html  # 結果報表，支援語言切換與欄位呈現
└── README.md             # 專案說明與進度追蹤文件
```

---

## 🔜 下一階段任務（2025-07-03 起）

1. 🧪 分析實際段落／整篇條款：測試 `test_multi_clauses.py` 對長條文的準確度與格式一致性
2. 📁 黑名單擴充至 100 條以上，補齊 `type.zh/en`、`risk_level.zh/en`、`reason`、`tags`
3. ✅ 預計將分析結果轉為測資，進一步用 `test_risk_cases_runner_dual.py` 比對驗證

---

本專案已完成分類結構與雙語顯示功能，進入條文解析與資料擴充階段，歡迎熟悉契約條款或 NLP 應用者參與貢獻。

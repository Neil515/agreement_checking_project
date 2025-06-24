## ✅ 明天優先處理任務（2025/06/25）

### 1. **建立風險條文黑名單（risk\_examples.json）**

* 背景：目前 whitelist 條文用來告訴 GPT 什麼內容是正常、不需標示風險的。
* 目標：建立一份「對照用」的黑名單 JSON，列出實際應被標記為高風險的條文。

**明日任務：**

* 規劃黑名單資料格式（類似 whitelist，加入 risk\_level: 高風險、type）
* 初步彙整10\~20條實際風險條文樣本（可從 clickwrap, 隱私條款, NDA 中擷取）
* 存入 `data/risk_examples.json`

---

### 2. **擴充 convert\_to\_whitelist.py 功能模組（CLI 支援）**

* 背景：目前轉檔程式功能完整但缺乏進階操作彈性

**明日任務：**

* ✅ 自動分類 `type` 欄位：依條文關鍵詞分類為授權、付款、責任、資料使用等
* ✅ 標記來源檔案：每條條文加入 `source: filename.docx` 欄位
* ✅ 統計總結：顯示條文數量、中英文比例、各 type 分布
* ✅ CLI 參數支援：使用者可加 `--auto-tag`、`--summary` 控制是否啟用這些功能

---

### 其他備註：

* whitelist.json 保持 `risk_level: 一般資訊` 不動，作為 GPT 的安全條文樣本
* 明天可視狀況安排 `test_risk_cases_runner.py` 是否引入黑名單比對測試

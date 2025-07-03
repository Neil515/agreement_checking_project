# AI 合約條款風險分析工具

這是一個使用 GPT 模型的條款風險分析工具，幫助使用者自動檢測合約內容中可能須注意的條款。本工具支援中文與英文條文的判斷，並提供簡潔的 JSON 輸出與視覺化報告。

---

## ✅ 最新進度整理（更新：2025-07-02）

### 📌 今日進度總結（2025-07-02）

#### ✅ 實作與測試成果

1. **新增 `test_single_clause.py` 進行條文逐筆測試**：
   - 可快速貼上條文，直接觀察 `language`、`type`、`risk_level` 是否分類正確
   - 支援 `detect_language()` 自動偵測語系

2. **改寫 `risk_analyzer.py`：
   - `type` 與 `risk_level` 改為 `{zh, en}` 雙語格式
   - `type` 自動比對 `risk_type_mapping.json`，並補上英文對應名稱
   - 若無對應則在 console 顯示警告 log，方便補充資料表

3. **建立 `test_multi_clauses.py` 支援整段或整篇條文分析**：
   - 載入 `.txt` 檔案 → 自動斷句 → 多條呼叫 `analyze_clause()`
   - 結果統一儲存為 JSON，可做為未來黑名單來源

4. **維持 `test_risk_cases_runner_dual.py` 作為測資比對用工具**：
   - 僅適用於格式化後的 JSON 測資（含預期 `type`, `risk_level`）
   - 明日測試可接續分析結果後轉測資用

5. **更新黑名單對照表**：
   - `risk_type_mapping.json` 補上「單方終止條款」對應：`Unilateral Termination Clause`

---

## 🔜 下一階段任務（2025-07-05 起）

1. 🧪 測試整段與整篇條文分析流程：
   - 使用 `test_multi_clauses.py` 測試合約 `.txt` 或 `.docx` 清理後輸入
   - 檢查輸出結構與欄位是否齊全

2. 📁 擴充黑名單測資至 100 條：
   - 補齊每條：`type.zh/en`, `risk_level.zh/en`, `reason`, `tags`
   - 使用 `fix_risk_format.py` 確保縮排與欄位一致性
   - 測試抽樣結果是否分類正確

---

## ✅ 現有功能

* 條文語言自動判斷與清理工具
* GPT 條文分析與分類轉換
* 測資格式化與風險欄位補齊工具
* 測試快取與 CLI 驗證框架
* 雙語風險分類結構與視覺化報表
* 自動類型對應（讀取 `risk_type_mapping.json`）與缺漏警示

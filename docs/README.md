# AI 合約條款風險分析工具

這是一個基於 GPT 模型的自動合約條款風險傷別工具，用於分析中英文合約條文，自動辨識「須注意」條款，輸出 JSON 格式。支援語言分析、精準分類、雙語編譯、分頁報表顯示，適合用於風險預警與可視化分析。

---

## ✅ 最新進度整理（更新：2025-07-05）

### 一、根據合約分類重新建立主類別 standard\_types.json

* 合容現有 30+ 簡體精緻類型，清構分類 15 個主類別
* 新增 `standard_type_mapping.json` 用於中英對照，整合 `map_to_main_type()` 連動

### 二、圖像認知與推理清理

* GPT 返回介於自由格式，會出現 `type.en` 是中文或 null
* 重新編譯\u `core/risk_analyzer.py`，確保 `type.zh`/、`type.en`/、`type_main.zh`/、`type_main.en`均為精準值，未對應時 fallback 為 `Unmapped`

### 三、對比模組功能完成

* 新增 `test_risk_cases_runner_dual.py`，用於點名測試 GPT 能否判讀正確
* `risk_type_mapping.json` 、`standard_type_mapping.json` 兩種管理檔輸出
* `split_into_clauses()` 判認是否是 contextual sentence 還有 bug，繼續原有檢測方式

---

## 📅 明日任務預告

### ✅ 工作 1：測試條文切句準確性

* 檢查目前的切句策略，是否會:

  * 把完整條文誤切成碎片
  * 把不同週載條文合併為一句
* 推薦挑選 2\~3 份條款密集的範例文件，觀察 `split_into_clauses()` 處理結果是否符合實務

### ✅ 工作 2：建立 clause\_id 與條號對應維護

* 目前每條 clause 都會自動生成 `clause_id` (C1, C2...)，但無法和原始合約中的範例條號對應
* 推薦新增一個 `source_ref` 層，例如 "第十條 第3段"，依證資清楚還原資料對應強

---

此工具已進入體系管理與分類網絡化階段，歡迎繼續優化。

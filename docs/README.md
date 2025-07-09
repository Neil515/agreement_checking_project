# AI 合約條款風險分析工具

這是一個基於 GPT 模型的合約條款風險辨識工具，用於分析中英文合約條文，自動辨識「須注意」條款，輸出 JSON 結果。支援條文斷句、風險分類、主類別對應、雙語標註與視覺化分析，適用於風險預警、法律審閱輔助與合約教育場域。

---

## ✅ 最新進度整理（更新：2025-07-09）

### 一、Chrome Extension MVP 啟動

* 建立 Flask API `/analyze`，支援自動語言辨識與條文切分。
* 成功整合 GPT 模型進行條文風險等級與類型判定。
* 開發測試程式 `test_api_post.py`，可模擬傳入條文並回傳 JSON 結果。
* 處理 GPT API timeout 問題，延長至 30 秒並顯示完整錯誤訊息。

### 二、風險分類輸出結構優化

* `type.zh`、`type.en`、`type_main.zh`、`type_main.en` 全面支援
* 若無法對應，標記為 `Unmapped`
* 使用 `risk_type_mapping.json` 與 `standard_type_mapping.json` 提供中英對照

### 三、下一階段後端強化項目（依優先順序）

* 前端顯示「分析中」提示
* Celery + Redis 非同步任務處理 queue
* 支援一次分析多條（Batch 模式）

---

## 🧩 第二階段預備事項（尚未實作）

### 目標：支援非網頁來源條款，例如 Word、PDF、圖片等文件

* 文件上傳 API：支援 .docx、.pdf 檔案處理（python-docx、PyMuPDF）
* 圖像 OCR 模組：導入 Tesseract 或 Google Vision，含預處理與切段
* 文件 → 條文 → 分析結果的整合流程
* 設計簡易前端上傳介面與進度提示模組

---

## ✅ 使用流程簡介

1. 輸入條文（貼上、上傳、擷取）
2. 系統自動判別語言與切句
3. 每條傳送至 GPT 分析模型
4. 回傳結果：風險等級、風險類型、主分類、中英文對應與標註

---

## 🔍 測試與驗證模組

* 測試檔案：`test_risk_analyzer.py`、`test_single_clause.py` 等
* 測試資料：黑白名單 `risk_examples.json`、`whitelist_examples.json`

---

✅ 本工具已進入 Chrome Extension MVP 開發階段，將逐步完成條文擷取、風險提示、介面整合等核心功能，後續亦可擴展支援文件與 OCR 條文來源。

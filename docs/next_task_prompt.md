## ✅ 明日工作任務規劃（延續 MVP 階段）

### 🔰 MVP 第一階段：主打 Chrome Extension「一鍵分析網站條款」

#### 下一個具體步驟：

* [ ] 設計 Chrome Extension 前端操作邏輯（popup UI / content script 擷取條文）
* [ ] 決定擷取條文的方式（例如：content script 擷取網頁內容 / shadow DOM / iframe）
* [ ] 將擷取的條文透過 fetch POST 至 Flask API `/analyze`
* [ ] 顯示回傳結果（條文、風險等級、類型）於前端 popup 或側欄
* [ ] 製作簡易測試用網頁（包含條款段落）作為擷取對象進行模擬

---

### 🧩 強化後端處理效能與使用者體驗（依優先順序）

#### ✅ 1. 前端顯示「分析中」狀態

* [ ] 條文尚未分析完時，呈現 Loading Spinner 或 "分析中..."
* [ ] 分析完成後動態替換顯示結果

#### ✅ 2. 加入非同步處理 queue（建議 Celery + Redis）

* [ ] 安裝並設置 Celery 背景任務框架
* [ ] 修改 `/analyze` API：將分析請求丟入 Celery 任務
* [ ] 提供另一支查詢任務狀態的 API（/status/\<task\_id>）

#### ✅ 3. 支援 batch 分析（一次 3-5 條）

* [ ] 修改 prompt 設計：允許同時分析多條條文
* [ ] 解析 GPT 回傳陣列，對應每條條文結果
* [ ] 測試多條回傳格式穩定性與錯誤率

---


✅ 備註：以上工作皆可配合現有的 `/analyze` 結構進行改版與擴充，MVP 重點仍以 Chrome Extension 使用體驗為主，第二階段開始支援更多文件來源的實務場景。

# AI 合約條款風險分析工具

這是一個使用 GPT 模型的條款風險分析工具，幫助使用者自動檢測合約內容中可能須注意的條款。本工具支援中文與英文條文的判斷，並提供簡潔的 JSON 輸出與視覺化報告。

---

## 🔧 專案架構

```
├── core/                  # 核心功能模組
│   ├── clean_text.py         # 條文清理
│   ├── lang_detect.py        # 自動語言偵測
│   ├── split_text.py         # 條文分句
│   └── risk_analyzer.py      # GPT 風險分析主模組
│
├── prompts/              # GPT 提示語（中英文）
│   ├── prompt_template_zh.txt
│   └── prompt_template_en.txt
│
├── tests/                # 測試資料與指令
│   ├── full_doc_tester.py    # 全檔分析指令
│   ├── test_risk_analyzer.py # 單句分析測試
│   └── zh_sample_test.txt    # 範例測試條文
│
├── outputs/              # 分析結果儲存位置
│   └── zh_sample_test_output.json
│
├── report_template.html  # 條款風險視覺化 HTML 報告
│
├── .env                  # 儲存 OpenAI API 金鑰
├── start_server.bat      # Windows 一鍵啟動 HTML 報告（需裝簡易伺服器）
└── README.md             # 使用說明
```

---

## ✅ 功能說明

### 條款分類邏輯（最新版本）

目前採用「二元分類」：

* `須注意`：條文可能存在不公平條件、過度義務、權利限制、責任移轉、資訊授權等
* `一般資訊`：不構成風險的常見條款，如背景描述、雙方約定、聯絡資訊等

每條結果會附上類型（如：責任限制、授權條款等）與簡要說明。

### 中文與英文支援

系統會自動判斷條文語言，並套用對應的提示語與關鍵字規則。

---

## 🔍 使用方法

### （1）安裝套件

```
pip install -r requirements.txt
```

### （2）設定 API 金鑰

在 `.env` 中設定 OpenAI 金鑰：

```
OPENAI_API_KEY=sk-xxx
```

### （3）進行測試分析

```
python tests/full_doc_tester.py tests/zh_sample_test.txt --output outputs/zh_sample_test_output.json
```

### （4）開啟視覺化報告

打開 `report_template.html`，可看到彩色條款分析報告。
如需自架伺服器，可使用：

```
python -m http.server
```

---

## 🧠 模型與提示語

* 採用 GPT-4（或 GPT-4o）進行條文理解與分類
* 分析前會進行清洗、語言判斷、句子切分
* 提示語設計清楚指示模型如何辨別「須注意 / 一般資訊」

---

## 🧪 測試模組

* `test_risk_analyzer.py`：驗證輸出格式正確性
* `full_doc_tester.py`：整批文件測試

---

## 📈 開發紀錄與未來計畫

* 已完成：二元分類邏輯整合、中英文 prompt 重寫、highlight 機制整合、HTML 報表視覺標示
* 計畫中：

  * 支援自訂敏感詞庫
  * 分析結果匯出 PDF
  * 契約版本比較功能

---

若有建議或需求，歡迎與開發者討論。

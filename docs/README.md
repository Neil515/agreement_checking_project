# AI 合約風險條款分析工具

本專案目的是開發一個具備風險辨識能力的合約條款分析工具，能自動對使用者提供的合約或使用者協議進行分句、清理與風險分類，並以可視化方式呈現風險結果，支援繁中與英文條款分析。

---

## 📦 專案結構

```
agreement_checking_project/
├── core/                # 核心模組（分析主邏輯）
│   ├── clean_text.py
│   ├── lang_detect.py
│   ├── risk_analyzer.py
│   ├── split_text.py
│   └── prompts/         # 風險分析提示詞模板
│       ├── prompt_template_zh.txt
│       └── prompt_template_en.txt
├── tests/               # 測試與工具程式
│   ├── sample_clause.txt
│   ├── full_doc_tester.py
│   └── test_openai.py
├── outputs/             # 分析結果儲存位置（.json）
├── frontend/            # 前端（HTML + JS）
│   └── report_template.html
├── .env                 # API 金鑰與環境變數
├── start_server.bat     # 快速啟動伺服器的批次檔
└── README.md
```

---

## 🔧 功能模組說明

### 1. 條文前處理

* `clean_text.py`：統一格式、去除空白雜訊
* `lang_detect.py`：自動辨識語言（中 / 英）
* `split_text.py`：將條款依語言切分成單句（已優化英文句點誤切問題）

### 2. GPT 分析模組

* `risk_analyzer.py`：根據 prompt 分析條文風險，回傳風險等級、類型與理由
* 支援 GPT 模擬模式與真實 API 模式（由 `.env` 中 `OPENAI_API_KEY` 控制）

### 3. 可視化前端

* `report_template.html`：讀取分析結果並視覺化條文
* 支援高 / 中 / 無風險條文切換、摘要跳轉、語言切換（實作中）

---

## 🧪 如何執行測試

### ✅ 測試一份條款：

```bash
python tests/full_doc_tester.py tests/full_agreement.txt --output outputs/full_agreement_analysis.json
```

### ✅ 啟動前端伺服器：

```bash
start_server.bat
```

（或手動執行 `python -m http.server 8000`）

---

## ✅ 目前進展（截至 2025/06/21）

### 🧠 分析引擎：

* ✅ 已串接 GPT-4 API，能回傳風險等級、類別與理由
* ✅ 英文 prompt 已優化，降低誤判常見描述句為風險
* ⏳ 中文 prompt 模板仍為初版，待進一步優化

### 📈 表現觀察：

* 初期誤判偏高（地址/標題誤列中風險）
* 已改善英文切句策略（re 模式修正）
* 正在開發：上下文/段落結構輔助判斷機制

### 🌍 多語系支援：

* 分析支援中英文
* 前端語系切換（en/zh）機制已設計，尚待實作

---

## 🔜 待辦與未來規劃

1. 批次 API 請求（提升分析效率）
2. 段落等級風險再加權（上下文判斷）
3. 可自訂風險規則 / 關鍵字（進階）
4. 用戶上傳檔案介面（前端）
5. 可導出 PDF 報告格式（後續）

---

## 🤖 測試使用條款說明

目前測試所用條款內容以 Gowalla 的使用者協議為基礎，此為過去實際存在的網路服務條款，但目前多用作 GPT 訓練或模型驗證示範，條文內容涵蓋完整但未刻意堆疊風險語句。

---

## 🙋 常見錯誤處理

* ❌ `openai.ChatCompletion` 錯誤 → 表示使用的是新版本 openai 套件，請降版：

```bash
pip install openai==0.28.0
```

* ❌ `prompt_template_xx.txt` 找不到 → 確保 `core/prompts` 目錄下有中英文 prompt 檔

* ❌ 無法連 GPT API → 檢查 .env 中 `OPENAI_API_KEY` 是否正確設定

---

## 📩 聯絡 / 貢獻

如有建議改進或想協助開發，可透過 GitHub Issues 回報或直接提 PR，感謝！

# AI 合約條款風險分析工具

這是一個使用 GPT 模型的條款風險分析工具，幫助使用者自動檢測合約內容中可能須注意的條款。本工具支援中文與英文條文的判斷，並提供簡潔的 JSON 輸出與視覺化報告。

---

## ✅ 最新進度整理（更新：2025-06-25）

### 📌 今日進度總結（2025-06-25）

#### ✅ `risk_analyzer.py` 改寫完成

* 支援中英文語言動態判斷，`gpt_analyze()` 會根據 `lang` 自動選擇對應提示語與範例
* 中英文 few-shot 提示範例皆已內嵌，無須外部載入
* 增加 `Risky` 判斷關鍵字對應中文「須注意」，避免語意遺漏

#### ✅ 雙測資測試 runner 架構完成

* `test_risk_cases_runner_dual.py` 可同時讀取白名單與黑名單測資進行驗證
* 內建快取系統（`results_cache.json`），分析結果會儲存以加速重複測試
* 快取根據條文原文與語言做索引，避免重複請求 GPT

#### ✅ 測資與資料優化

* 白名單改以 `whitelist_examples.json` 作為唯一資料來源，不再需多餘轉換檔案
* 測資自動讀取中英欄位，自動調用語言模式
* 未來 `risk_examples.json` 將做為黑名單來源

### 📌 whitelist 條文建構與英文支援進展

* 完成 convert_to_whitelist.py 強化：新增中英文語言判斷、自動過濾非條文片段（如標題、短語）
* 合併短段為段落式條文，避免碎裂句誤判
* 每條自動標記語言（language: zh/en），保留 risk_level: "一般資訊"
* 成功加入英文條文白名單樣本，作為 GPT 提示時的反例參考

### 📌 下一階段任務預告

1. 建立高風險條文樣本集 `risk_examples.json`

2. 優化測試執行工具 `test_risk_cases_runner_dual.py`

   * 增加兩個功能：
     - 若條文分類錯誤，顯示 GPT 判斷的 `type` 和 `reason`，協助快速了解錯誤原因
     - 加入 CLI 參數：
       - `--no-cache`：每次都重新送出條文，不使用先前快取
       - `--limit 50`：只測試前 50 筆，適合快速調整與驗證

3. 自動標記條文類型（type）模組（第一版）

   * 新增檔案 `core/auto_tag_type.py`
   * 利用簡單的關鍵字規則判斷條文類型，例如：
     - 含「付款」「利息」 → type: "付款"
     - 含「授權」「資料使用」 → type: "授權"
     - 含「終止」「解約」 → type: "解約"
     - 含「保密」「資訊揭露」 → type: "保密"
     - 含「損害」「賠償」「責任」 → type: "責任"
   * 可以用來比對 GPT 輸出的 type 是否一致，作為交叉驗證工具

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
├── data/                 # 白名單與未來風險樣本資料
│   ├── whitelist_examples.json
│   └── risk_examples.json （預計加入）
│
├── tools/                # 🔄 條文轉換與前處理腳本
│   └── convert_to_whitelist.py
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

### 條款分類邏輯

目前採用「二元分類」：

* `須注意`：條文可能存在不公平條件、過度義務、權利限制、責任移轉、資訊授權等
* `一般資訊`：不構成風險的常見條款，如背景描述、雙方約定、聯絡資訊等

未來將擴充風險層級（高／中／低）與明確 `type` 分類欄位。

### 中文與英文支援

* 自動偵測語言（使用 Unicode 判斷）
* 條文篩選標準針對語言個別設計（避免中文條文被誤判為無效）

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

## 📄 白名單（Whitelist）機制介紹

為避免 GPT 誤將正常條文判為風險條款，我們建立了 whitelist 條文庫（`whitelist_examples.json`）：

* 條文皆為合理、常見、不具風險特性的法律用語
* 系統分析時會自動比對並載入相似樣本，作為模型反例參照
* 提升 GPT 判斷精確性與穩定性

---

## 📈 開發進度追蹤

* ✅ 已完成：

  * 中英文條文合併處理
  * 條文清理 + 自動語言判斷
  * 條文格式統一與轉換工具
  * whitelist 自動過濾與合併短段

* 🔜 即將完成：

  * 黑名單 JSON 建立與範例擴充
  * 條文類型自動標記（type 欄位）
  * CLI 擴充：來源檔名、統計摘要、分類標籤

---

歡迎開發者或法律專業者加入，共同優化風險條款標記工具。

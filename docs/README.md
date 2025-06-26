# AI 合約條款風險分析工具

這是一個使用 GPT 模型的條款風險分析工具，幫助使用者自動檢測合約內容中可能須注意的條款。本工具支援中文與英文條文的判斷，並提供簡潔的 JSON 輸出與視覺化報告。

---

## ✅ 最新進度整理（更新：2025-06-26）

### 📌 近期完成項目

#### ✅ 快取機制擴充

* 快取檔 `results_cache.json` 以 `clause + language` 為索引鍵
* 支援 CLI：

  * `--no-cache` 不讀寫快取
  * `--limit N` 限制測試數量
* 有效避免重複送出 GPT 請求，加速測試

#### ✅ 黑白名單格式統一

* 所有條文均具備 `clause`, `risk_level`, `type`, `language`, `reason`, `tags` 欄位
* 補上空白 `reason`、統一 `type` 欄位結構
* 提供格式修正工具：

  * `tools/fix_risk_format.py`
  * `tools/fix_whitelist_format.py`

#### ✅ CLI 測試與測資更新

* `test_risk_cases_runner_dual.py` 可同時分析白／黑名單條文並比對 GPT 結果
* 加入 20 筆新測資，錯誤比對機制完整：`risk_level`、未來將支援 `type`

---

## 🔜 下一階段任務

* `--check-type`：新增 GPT 分析結果與測資 type 欄位一致性比對
* `--summary`：統計條文語言比例、風險等級與類型分布
* 擴充黑名單測資至 100 條以上，完整標記欄位
* 建立視覺化報表資料輸出（供 `report_template.html` 使用）

---

## 🔧 專案架構

```
├── core/                  # 核心模組
│   ├── clean_text.py         # 條文清理
│   ├── lang_detect.py        # 自動語言偵測
│   ├── split_text.py         # 條文分句
│   └── risk_analyzer.py      # GPT 分析主模組
│
├── prompts/              # GPT 提示語（中英文）
│   ├── prompt_template_zh.txt
│   └── prompt_template_en.txt
│
├── data/                 # 測資來源
│   ├── whitelist_examples.json
│   └── risk_examples.json
│
├── tools/                # 前處理與格式統一腳本
│   ├── convert_to_whitelist.py
│   ├── fix_risk_format.py
│   └── fix_whitelist_format.py
│
├── tests/                # 測試程式與測資檔
│   ├── full_doc_tester.py
│   ├── test_risk_analyzer.py
│   ├── test_risk_cases_runner_dual.py
│   ├── zh_sample_test.txt
│   └── full_agreement.txt
│
├── outputs/              # 測試結果輸出 JSON
│   ├── zh_sample_test_output.json
│   └── full_agreement_analysis.json
│
├── report_template.html  # 視覺化分析報告 HTML
├── .env                  # OpenAI API 金鑰
├── start_server.bat      # Windows 一鍵開伺服器工具
└── README.md             # 使用說明
```

---

## ✅ 功能說明

### 條款分類邏輯

目前採用二元分類：

* `須注意`：包含風險、不公平條件、過度授權等
* `一般資訊`：無風險的合約描述性內容

後續將擴充明確風險層級（高／中／低）與類型分類（type）

### 多語支援與提示優化

* 自動偵測條文語言
* 中英文提示語各自對應範例與 few-shot 設計

### CLI 工具與快取支援

* 測試 CLI 提供快速測資驗證，支援快取、限制筆數、結果比對
* 使用者可加入新測資，快取會自動管理避免重複分析

---

## 📈 開發里程碑追蹤

✅ 條文快取與 CLI 參數整合
✅ 黑白名單格式統一與修復工具建置
✅ 測資初步驗證與快取資料建立
🔜 擴充測資與型別驗證功能
🔜 建立報告輸出與視覺化整合

---

歡迎法律背景或開發者共同參與，優化條款風險標記流程！

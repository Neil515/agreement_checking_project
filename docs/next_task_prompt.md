## ✅ 明天優先處理任務（2025/06/30）

1. 📁 擴充黑名單測資：

   * 目標條文數量擴充至 100 條以上
   * 每筆補齊以下欄位：`type`、`reason`、`tags`
   * 使用 `fix_risk_format.py` 工具確保格式一致
   * 檢查是否含中文與英文版本混雜內容

2. 🌐 支援風險類型中英文版本（初步建置）

```
[1] 建立風險類型中英文對照表
    |
    └─→ 新增：data/risk_type_mapping.json
         範例：
         {
           "Waiver of Rights": "消費者權益剝奪",
           "Privacy and Data Retention": "監控與資訊條款",
           ...
         }

[2] 更新 Prompt，統一 GPT 輸出類型名稱
    |
    └─→ 修改：prompts/prompt_template_en.txt
         - 加入英文風險類型選單提示
         - 指定從選單中選一項 type

[3] 修改測資檔案結構（所有 *.json 測資）
    |
    └─→ 更新以下四個檔案格式：
         - data/risk_examples.json
         - data/risk_examples_backup.json
         - data/risk_examples_mapped.json
         - data/whitelist_examples.json
         
         把：
         "type": "消費者權益剝奪"
         改成：
         "type": {
           "zh": "消費者權益剝奪",
           "en": "Waiver of Rights"
         }

[4] 修改分析與測試主程式，支援雙語型別讀取與比對
    |
    ├─→ 修改：core/risk_analyzer.py
    |     - 分析結果中加入英文 `type` 與對應中文（或相反）
    |     - 載入 risk_type_mapping.json 做轉換
    |
    └─→ 修改：tests/test_risk_cases_runner_dual.py
          - 改用雙語型別做比對，例如：
            actual_type = result['type']['en']
            expected_type = expected['type']['en']

[5] 修改報表與 UI 顯示邏輯
    |
    └─→ 修改：report_template.html
         - 根據使用者語言設定，顯示 `type.zh` 或 `type.en`
         - 加入語言切換選單（如：中 / 英）
```
(
data\risk_type_mapping.json
tools\convert_to_bilingual_type.py
我保留了以上這兩支沒有刪，除外全部回復到昨天的狀態。
)
---

🔍 非優先但可提前準備項目：

* 分析類型錯誤的主要模式（如：Legal Reference vs. Legal Precedent）
* 評估是否需擴充 `analyze_clause` 回傳的標準類型集
* 規劃分類提示語彙標籤強化（type tags）
* 確認 `results_cache.json` 是否持續更新正常

## ✅ 明天優先處理任務（2025/06/28）

1. 🧪 測試條文 41-50：

   * 執行 `test_risk_cases_runner_dual.py --offset 40 --limit 10 --check-type`
   * 確認風險等級與類型比對結果
   * 特別注意黑白名單中的預期與 GPT 判斷是否一致

2. 📁 擴充黑名單測資：

   * 目標條文數量擴充至 100 條以上
   * 每筆補齊以下欄位：`type`、`reason`、`tags`
   * 使用 `fix_risk_format.py` 工具確保格式一致
   * 檢查是否含中文與英文版本混雜內容

---

🔍 非優先但可提前準備項目：

* 分析類型錯誤的主要模式（如：Legal Reference vs. Legal Precedent）
* 評估是否需擴充 `analyze_clause` 回傳的標準類型集
* 規劃分類提示語彙標籤強化（type tags）
* 確認 `results_cache.json` 是否持續更新正常

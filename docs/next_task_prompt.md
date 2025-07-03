## ✅ 明天優先處理任務（2025/07/05）

1. 🧪 測試段落與整篇合約條款：

   * 選取中英文合約樣本（來源：`assets/clause examples/`）
   * 用 `split_text.py` 或手動切段，模擬一整段或整篇合約的分析流程
   * 測試分析器能否逐條解析並標記：
     - `language` 自動判斷
     - `type.zh` / `type.en` 對照是否正確
     - `risk_level.zh` / `risk_level.en` 判斷一致性
   * 確認 `results_cache.json` 快取是否能辨識每條條文
   * 執行 CLI 模式：如 `--limit`、`--no-cache`、`--check-type` 測試效果

2. 📁 擴充黑名單至 100 條：

   * 將現有條文補齊至至少 **100 條以上**
   * 每筆欄位需完整：`type`（中英）、`risk_level`（中英）、`reason`（原文語言）、`tags`
   * 使用 `tools/fix_risk_format.py` 確保 JSON 結構與縮排正確
   * 測試 10 條隨機條文，確認 GPT 輸出與分類一致

---

🔍 非優先但可準備項目：

* 若 `type` 無對應英文名稱，補入 `risk_type_mapping.json`
* 測試 `risk_analyzer.py` 的 debug log，確認缺漏項提示正常
* 為每筆黑名單條文加上來源與段號備註（供追溯）

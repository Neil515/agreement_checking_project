## ✅ 明天優先處理任務（2025/06/27）

1. 🧪 建立 GPT 與測資 `type` 一致性驗證功能：

   * 新增 `--check-type` 參數
   * 檢查 GPT 輸出之 `type` 是否與測資中標記一致
   * 若不一致，輸出錯誤項目、條文與雙方 type
   * 忽略 `type = "待分類"` 的條文

2. 📊 新增 `--summary` 功能：

   * 統計黑白名單條文總數
   * 顯示中英文比例
   * 顯示各風險類型（type）與風險等級（risk\_level）分布

3. 🔍 準備 GUI 報表輸出格式：

   * 條文原文
   * GPT 判定結果（風險等級、type、reason）
   * 是否分類正確、來自黑或白名單
   * 統一輸出成 JSON 檔供報表讀取

4. 🚀 擴充黑名單測資：

   * 目標總數達 100 條以上
   * 每條補齊 `type`, `reason`, `tags` 欄位
   * 可用 `fix_risk_format.py` 工具統一欄位格式

5. ⏱️ 增加快取內容：

   * 再執行一次 `--limit 10` 測試，擴充 `results_cache.json` 資料量
   * 確保新加入條文順利寫入快取

---

✅ 現有功能已完成：

* CLI 參數 `--no-cache`、`--limit N` 功能正常
* 快取格式為 `clause + lang`，已避免語言混淆
* 黑白名單欄位格式已統一（含 type, reason, tags）
* `fix_risk_format.py`、`fix_whitelist_format.py` 工具已備妥

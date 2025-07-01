## ✅ 明天優先處理任務（2025/07/02）

1. 🧪 測試實際合約條款分析：

   * 匯入真實中英文條文範例（docx 或 txt）
   * 使用現有流程執行完整分析
   * 檢查輸出格式是否包含正確的：
     - `language`
     - `type.zh` / `type.en`
     - `risk_level.zh` / `risk_level.en`
     - 條文與 reason 是否符合語言與邏輯預期
   * 確認報表語言切換功能正常
   
2. 📁 擴充黑名單測資：

   * 目標條文數量擴充至 **100 條以上**
   * 每筆補齊以下欄位：`type`（中英）、`risk_level`（中英）、`reason`、`tags`
   * 使用 `fix_risk_format.py` 工具確保欄位與縮排格式一致
   * 確認混合語言條文也正確標記 `language` 欄位
   * 匯出後重新測試 10 條以驗證分類正確

3. 🛠️ 修改核心與測試模組支援中英文格式：

   * `core/risk_analyzer.py`：將 GPT 輸出 `type` 比對後補上中英文欄位
   * `tests/test_risk_cases_runner_dual.py`：改為比對 `type['en']` 和 `risk_level['en']`

---

🔍 非優先但可提前準備項目：

* 補上 `reason.en` 空欄位結構，準備未來雙語顯示（選填）
* 將報表加入欄位過濾（ex: 只看某類型 / 只看英文條款）
* 自動標記來源檔案與條號（供全文追蹤）

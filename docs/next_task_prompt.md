## ✅ 明天優先處理任務（2025/06/23）

### 1. **風險判定標準再調整**

* 目標：避免「過度標示須注意條款」，提升實用性與信賴度。
* 建議行動：

  * 檢視現有 `test_risk_cases.json` 中爭議分類（如條文9、10）
  * 在 prompt 加入更多 whitelist 條文，說明哪些「明確不構成風險」
  * 可考慮新增 `risk_sensitivity` 參數：控制敏感度（高、中、低）

### 2. **whitelist\_examples.json 擴充與動態應用**

* 擴充目前 `Whitelist Examples` 至 20 條以上，滿足更多合法常見條款
* 開始開發：

  * ☑ `core/similarity_selector.py`：可依關鍵詞或語義找出近似 whitelist 條文
  * ☑ 修改 `gpt_analyze()`：每次帶入 2–3 條最接近的 whitelist 條文於 prompt 中，引導分類更精準

### 3. **測試增強與自動驗證機制**

* 為 `test_risk_cases_runner.py` 增加對應 whitelist 模式的測試組
* 建議為 prompt 改動設定專用測試集（可名為 `test_prompt_effect.json`）
* 考慮未來自動比較多次 GPT 結果，計算風險標示穩定性指標

### 4. **前端與語系功能同步啟動**

* 可進入前端支援：

  * 語系切換（zh/en）
  * 顯示條款類別類型選擇
* 後端支援：

  * 傳回 `risk_level` 同時附中英文對照

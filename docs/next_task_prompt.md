## ✅ 明天優先處理任務（2025/06/26）

2. 🔧 優化 test_risk_cases_runner_dual.py：
若失敗，標示 GPT 判定的 type 和 reason

支援 CLI 參數：

--no-cache 強制不使用快取

--limit 50 測試指定數量條文（便於快速迭代）

3. 📄 條文標記 type 自動分類機制（第一版）
新增 core/auto_tag_type.py

根據關鍵字簡單 rule-based 分類為：「付款」、「授權」、「責任」、「解約」、「保密」等類型

可與 GPT 輸出比對一致性

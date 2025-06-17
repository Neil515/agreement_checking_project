## 🚀 下一步工作建議（2025-06-18）

### ✅ 任務名稱：實作 risk\_analyzer.py (使用 GPT 分析風險)

🔹 任務目的：

* 將分割得來的單句條款一條條供 GPT 分析，返回風險分類 JSON
* 是整個條款分析的核心模組，也是 report\_generator 線上呈現的基礎

🔹 任務內容：

1. 設計出口函式 `analyze_clause(text: str, lang: str) -> dict`
2. 從 `prompt_template_zh.txt` 讀取提示語，取代對應條款
3. 呼叫 OpenAI API （首次可先 mock 回復格式）
4. 返回格式為:

```json
{
  "clause": "...",
  "risk_level": "高／中／無",
  "reason": "...",
  "type": "資料使用/已同意權/..."
}
```

5. 製作測試檔 `test_risk_analyzer.py` ，對中文條款進行例項測試 (3※5 條)

🔹 供應指導：

* 可從 `full_doc_tester.py` 模擬一系列條款進行 batch 處理
* 可先使 `print()` 確認接受與回傳格式無誤

🚨 初始階段可 mock 以下資料，以助於展開模組格式與交接週期：

```python
{
  "clause": text,
  "risk_level": "中",
  "reason": "有可能潛在的已同意權條款",
  "type": "已同意權"
}
```

---

這是你已完成 clean\_text 、lang\_detect 、split\_text 之後，接近核心 AI 分析功能的關鍵步驟。

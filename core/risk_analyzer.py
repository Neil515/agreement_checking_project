import os

def load_prompt_template(path="prompts/prompt_template_zh.txt") -> str:
    """
    讀取提示語模板檔案。
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"找不到提示語模板：{path}")
    
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def analyze_clause(text: str, lang: str = "zh") -> dict:
    """
    接收一段條款文字，套用提示語模板並模擬 GPT 回傳結果。
    """
    prompt_template = load_prompt_template("prompts/prompt_template_zh.txt")
    prompt = prompt_template.replace("{{clause}}", text)

    # 這裡可以加入 GPT 呼叫，現在先用 mock 回傳資料
    print("[DEBUG] 套用提示語如下：\n", prompt)

    return {
        "clause": text,
        "risk_level": "中",
        "reason": "有可能潛在的已同意權條款",
        "type": "已同意權"
    }

# 單獨執行本檔案時，進行簡單測試
if __name__ == "__main__":
    test_clause = "使用者同意本公司得擷取其聯絡資訊以提供更個人化的服務。"
    result = analyze_clause(test_clause)
    print("[模擬回傳結果]", result)

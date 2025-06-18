def load_prompt_template(path="prompt_template_zh.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def analyze_clause(text: str, lang: str = "zh") -> dict:
    # 讀取提示語模板
    prompt_template = load_prompt_template()

    # 將條款代入模板
    prompt = prompt_template.replace("{{clause}}", text)

    print(f"[提示語輸出]：\n{prompt}\n")  # 可用來 debug 檢查輸出

    # TODO：之後這裡改成呼叫 GPT，目前先回傳模擬資料
    return {
        "clause": text,
        "risk_level": "中",
        "reason": "有可能潛在的已同意權條款",
        "type": "已同意權"
    }

# 範例用法（你可以暫時直接在這個檔案底部測試）
if __name__ == "__main__":
    test_clause = "使用者同意本公司得擷取其聯絡資訊以提供更個人化的服務。"
    result = analyze_clause(test_clause)
    print(result)

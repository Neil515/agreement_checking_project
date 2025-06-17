import os
from pathlib import Path

# 假設將來這些模組都會實作完成，先以函式名稱作為界面
from core.clean_text import clean_text
from core.lang_detect import detect_language
from core.split_text import split_sentences
from core.risk_analyzer import analyze_clause

# Prompt 模板載入器（未來可支援英文）
def load_prompt_template(language='zh'):
    if language == 'zh':
        with open('prompt_template_zh.txt', encoding='utf-8') as f:
            return f.read()
    else:
        raise NotImplementedError("目前僅支援中文條款")

# 主流程函式
def analyze_document(file_path):
    with open(file_path, encoding='utf-8') as f:
        raw_text = f.read()

    cleaned_text = clean_text(raw_text)
    language = detect_language(cleaned_text)
    sentences = split_sentences(cleaned_text, language)
    prompt_template = load_prompt_template(language)

    results = []
    for sentence in sentences:
        result = analyze_clause(sentence, prompt_template, language)
        results.append(result)

    return results

# 測試用（從命令列執行）
if __name__ == '__main__':
    test_file = 'example_clause.txt'  # 放一份測試條款
    output = analyze_document(test_file)
    for item in output:
        print(item)

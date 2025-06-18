import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core')))

from clean_text import clean_text
from lang_detect import detect_language
from split_text import split_sentences
from risk_analyzer import analyze_clause
import json

def load_test_clause(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def analyze_document(text: str) -> list:
    cleaned = clean_text(text)
    lang = detect_language(cleaned)
    sentences = split_sentences(cleaned, lang)
    
    results = []
    for sentence in sentences:
        if sentence.strip():  # 忽略空句
            result = analyze_clause(sentence, lang)
            results.append(result)
    return results

if __name__ == "__main__":
    # 範例：讀一個條款文字檔（你可改成實際檔案路徑）
    sample_path = "tests/sample_clause.txt"
    
    if not os.path.exists(sample_path):
        print(f"⚠️ 找不到測試檔案：{sample_path}")
        sys.exit(1)

    input_text = load_test_clause(sample_path)
    analysis_result = analyze_document(input_text)

    print(json.dumps(analysis_result, indent=2, ensure_ascii=False))

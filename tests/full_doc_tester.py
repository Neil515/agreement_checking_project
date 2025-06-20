import sys
import os
import json
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core')))

from clean_text import clean_text
from lang_detect import detect_language
from split_text import split_sentences
from risk_analyzer import analyze_clause

def load_test_clause(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def analyze_document(text: str) -> list:
    cleaned = clean_text(text)
    lang = detect_language(cleaned)
    sentences = split_sentences(cleaned, lang)
    #sentences = sentences[:10]  # 暫時只處理前 10 句


    results = []
    for sentence in sentences:
        if sentence.strip():  # 忽略空句
            result = analyze_clause(sentence, lang)
            results.append(result)
    return results

def save_json(results: list, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"✅ 分析結果已儲存到：{output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="tests/sample_clause.txt", help="輸入條款檔案路徑")
    parser.add_argument("--output", default="outputs/sample_analysis.json", help="輸出 JSON 路徑")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"⚠️ 找不到檔案：{args.input}")
        sys.exit(1)

    input_text = load_test_clause(args.input)
    analysis_result = analyze_document(input_text)

    print(json.dumps(analysis_result, indent=2, ensure_ascii=False))
    save_json(analysis_result, args.output)

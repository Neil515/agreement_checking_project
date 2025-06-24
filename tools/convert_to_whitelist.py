import os
import re
import json
import argparse
from docx import Document
import pandas as pd


def extract_from_docx(path):
    doc = Document(path)
    return [para.text.strip() for para in doc.paragraphs if para.text.strip()]


def extract_from_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return [p.strip() for p in content.split("\n\n") if p.strip()]


def extract_from_csv(path):
    df = pd.read_csv(path)
    text_col = next((col for col in df.columns if 'clause' in col or '條文' in col), df.columns[0])
    return df[text_col].dropna().astype(str).tolist()


def extract_from_md(path):
    return extract_from_txt(path)


def detect_language(text):
    if re.search(r"[\u4e00-\u9fff]", text):
        return "zh"
    return "en"


def is_valid_clause(text):
    if len(text.strip()) < 30:
        return False

    if detect_language(text) == "zh":
        keywords = ["同意", "承諾", "應", "不得", "授權", "願意", "保證"]
    else:
        keywords = ["shall", "agree", "must", "may", "is", "are", "will", "warrant", "consent", "authorize", "undertake"]

    if not any(kw in text for kw in keywords):
        return False

    return True


def merge_short_paragraphs(paragraphs, min_len=40):
    merged = []
    buffer = ""
    for para in paragraphs:
        para = para.strip()
        if len(para) < min_len:
            buffer += " " + para
        else:
            if buffer:
                para = buffer.strip() + " " + para
                buffer = ""
            merged.append(para.strip())
    if buffer:
        merged.append(buffer.strip())
    return merged


def to_whitelist_format(clauses):
    result = []
    merged_clauses = merge_short_paragraphs(clauses)
    for clause in merged_clauses:
        if is_valid_clause(clause):
            result.append({
                "clause": clause,
                "risk_level": "一般資訊",
                "type": "待分類",
                "language": detect_language(clause),
                "tags": ["人工確認"]
            })
    return result


def process_file(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        clauses = extract_from_docx(path)
    elif ext == ".txt":
        clauses = extract_from_txt(path)
    elif ext == ".csv":
        clauses = extract_from_csv(path)
    elif ext == ".md":
        clauses = extract_from_md(path)
    else:
        print(f"Unsupported file format: {path}")
        return []
    return to_whitelist_format(clauses)


def main(input_folder, output_file):
    all_entries = []
    for filename in os.listdir(input_folder):
        full_path = os.path.join(input_folder, filename)
        if os.path.isfile(full_path):
            print(f"Processing: {filename}")
            entries = process_file(full_path)
            all_entries.extend(entries)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_entries, f, ensure_ascii=False, indent=2)
    print(f"Output saved to {output_file} with {len(all_entries)} entries.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert clauses to whitelist format")
    parser.add_argument("--input", required=True, help="Input folder path")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    args = parser.parse_args()

    main(args.input, args.output)

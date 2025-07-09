import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from core.split_text import split_sentences
from core.lang_detect import detect_language
from core.risk_analyzer import analyze_clause

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text', '')
    lang = data.get('lang', 'auto')

    if not text.strip():
        return jsonify({"error": "No text provided."}), 400

    # 語言自動判斷
    if lang == 'auto':
        lang = detect_language(text)

    # 條文切分
    clauses = split_sentences(text, lang)
    results = []

    for clause in clauses:
        result = analyze_clause(clause, lang)
        result['text'] = clause  # 保留原文
        # 補上 risk_type 欄位（以中文為主）
        result['risk_type'] = result.get('type', {}).get('zh', None)
        results.append(result)

    return jsonify({"clauses": results})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

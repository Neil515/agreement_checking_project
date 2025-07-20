import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from flask_cors import CORS
from core.split_text import split_sentences
from core.lang_detect import detect_language
from core.risk_analyzer import analyze_clause

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text', '')
    lang = data.get('lang', 'auto')
    mode = data.get('mode', 'fast')  # 新增 mode 參數，預設為快速模式

    if not text.strip():
        return jsonify({"error": "No text provided."}), 400

    # 語言自動判斷
    if lang == 'auto':
        lang = detect_language(text)

    # 條文切分
    clauses = split_sentences(text, lang)
    results = []

    print(f"🎯 開始分析，模式：{mode}，語言：{lang}，條款數量：{len(clauses)}")

    for clause in clauses:
        # 傳遞 mode 參數給 analyze_clause 函式
        result = analyze_clause(clause, lang, mode)
        result['text'] = clause  # 保留原文
        # 補上 risk_type 欄位（以中文為主）
        result['risk_type'] = result.get('type', {}).get('zh', None)
        results.append(result)

    # 在回應中包含分析模式資訊
    response_data = {
        "clauses": results,
        "analysis_mode": mode,
        "language": lang,
        "total_clauses": len(clauses)
    }

    print(f"✅ 分析完成，模式：{mode}，處理條款：{len(results)} 個")
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

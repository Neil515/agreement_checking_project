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

    if not text:
        return jsonify({"error": "No text provided."}), 400

    # 語言自動判斷
    if lang == 'auto':
        # 如果是陣列，用第一條文判斷語言；如果是字串，直接判斷
        sample_text = text[0] if isinstance(text, list) else text
        lang = detect_language(sample_text)

    # 處理輸入格式：支援字串（向下相容）和陣列（批次分析）
    if isinstance(text, str):
        # 向下相容：字串輸入，進行條文切分
        clauses = split_sentences(text, lang)
        print(f"🎯 開始分析（字串模式），模式：{mode}，語言：{lang}，條款數量：{len(clauses)}")
    elif isinstance(text, list):
        # 批次分析：直接使用傳入的條文陣列
        clauses = text
        print(f"🎯 開始批次分析，模式：{mode}，語言：{lang}，條款數量：{len(clauses)}")
    else:
        return jsonify({"error": "Invalid text format. Expected string or array."}), 400

    results = []

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
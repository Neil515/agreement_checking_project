import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.risk_analyzer import analyze_clause

def load_test_cases(filepath="tests/test_risk_cases.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def run_tests():
    cases = load_test_cases()
    failed = 0
    lang = "zh"  # 根據測資語言設定

    for i, case in enumerate(cases, 1):
        result = analyze_clause(case["text"], lang)
        actual = result.get("risk_level", "未輸出")
        expected = case["expected_label"]

        if actual != expected:
            failed += 1
            print(f"❌ Case {i}: 應為『{expected}』，實際為『{actual}』")
            print(f"    條文: {case['text']}")
            print(f"    備註: {case['note']}")
        else:
            print(f"✅ Case {i}: 正確分類為『{actual}』")

    print(f"\n✅ 測試完畢，共 {len(cases)} 條，錯誤 {failed} 條。")

if __name__ == "__main__":
    run_tests()

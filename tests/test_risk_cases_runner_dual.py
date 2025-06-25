import json
import sys
import os
import re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.risk_analyzer import analyze_clause
from core.lang_detect import detect_language

TEST_FILES = [
    ("data/whitelist_examples.json", "一般資訊"),
    ("data/risk_examples.json", "須注意")
]

CACHE_FILE = "tests/results_cache.json"

def load_test_cases(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def run_tests():
    total = 0
    failed = 0
    cache = load_cache()
    updated = False

    for filepath, default_expected_level in TEST_FILES:
        print(f"\n🔍 測試檔案：{filepath}（預設預期：{default_expected_level}）")
        cases = load_test_cases(filepath)
        for i, case in enumerate(cases, 1):
            clause = case.get("clause", "")
            lang = case.get("language") or detect_language(clause)
            expected = case.get("risk_level", default_expected_level)

            # 如果條文不在快取中，進行分析並更新快取
            if clause not in cache:
                try:
                    result = analyze_clause(clause, lang)
                    updated = True  # 有新結果產生，標記更新
                    cache[clause] = result
                except Exception as e:
                    print(f"⚠️ 分析失敗: {e}")
                    result = {"clause": clause, "risk_level": "錯誤", "type": "錯誤", "reason": str(e)}
                    cache[clause] = result
                    updated = True  # 有新錯誤結果，仍然標記更新
            else:
                result = cache[clause]  # 讀取快取中的結果

            actual = result.get("risk_level", "未輸出")
            total += 1

            if actual != expected:
                failed += 1
                print(f"❌ Case {i}: 應為『{expected}』，實際為『{actual}』")
                print(f"    條文: {clause}")
                print(f"    類型: {result.get('type', '未提供')}")
            else:
                print(f"✅ Case {i}: 正確分類為『{actual}』")

    # 確保無論是否更新，都儲存快取
    if updated:
        print("⚡ 儲存快取...")
        save_cache(cache)

    print(f"\n✅ 測試完畢，共 {total} 條，錯誤 {failed} 條。")


if __name__ == "__main__":
    run_tests()

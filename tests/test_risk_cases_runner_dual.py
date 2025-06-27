import json
import sys
import os
import re
import argparse

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

def build_cache_key(clause, lang):
    return clause.strip() + "||" + lang

def run_tests(no_cache=False, limit=None, offset=0):
    total = 0
    failed = 0
    cache = {} if no_cache else load_cache()
    updated = False

    for filepath, default_expected_level in TEST_FILES:
        print(f"\n🔍 測試檔案：{filepath}（預設預期：{default_expected_level}）")
        cases = load_test_cases(filepath)
        if limit:
            cases = cases[offset:offset + limit]
        else:
            cases = cases[offset:]

        for i, case in enumerate(cases, offset + 1):
            clause = case.get("clause", "")
            lang = case.get("language") or detect_language(clause)
            expected = case.get("risk_level", default_expected_level)

            cache_key = build_cache_key(clause, lang)

            if cache_key not in cache:
                try:
                    result = analyze_clause(clause, lang)
                    if not no_cache:
                        cache[cache_key] = result
                        updated = True
                except Exception as e:
                    print(f"⚠️ 分析失敗: {e}")
                    result = {"clause": clause, "risk_level": "錯誤", "type": "錯誤", "reason": str(e)}
                    if not no_cache:
                        cache[cache_key] = result
                        updated = True
            else:
                result = cache[cache_key]

            actual = result.get("risk_level", "未輸出")
            total += 1

            if actual != expected:
                failed += 1
                print(f"❌ Case {i}: 應為『{expected}』，實際為『{actual}』")
                print(f"    條文: {clause}")
                print(f"    類型: {result.get('type', '未提供')}")
            else:
                print(f"✅ Case {i}: 正確分類為『{actual}』")

    if updated and not no_cache:
        print("⚡ 儲存快取...")
        save_cache(cache)

    print(f"\n✅ 測試完畢，共 {total} 條，錯誤 {failed} 條。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-cache", action="store_true", help="不使用快取")
    parser.add_argument("--limit", type=int, help="只測試 N 條")
    parser.add_argument("--offset", type=int, default=0, help="從第 N 筆開始測試（預設 0）")
    args = parser.parse_args()

    run_tests(no_cache=args.no_cache, limit=args.limit, offset=args.offset)

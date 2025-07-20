#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試本地規則初篩功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.risk_analyzer import local_rule_filter, analyze_clause

def test_local_rule_filter():
    """測試本地規則初篩功能"""
    print("🧪 開始測試本地規則初篩功能...")
    
    # 測試案例
    test_cases = [
        {
            "clause": "甲方有權隨時修改本服務條款，並不另行通知乙方。",
            "lang": "zh",
            "expected_risky": True,
            "description": "高風險條款 - 單方變更權"
        },
        {
            "clause": "乙方同意授權甲方無償使用其上傳資料用於行銷用途。",
            "lang": "zh", 
            "expected_risky": True,
            "description": "高風險條款 - 無償授權"
        },
        {
            "clause": "本契約雙方應善意協商處理合約未盡事宜。",
            "lang": "zh",
            "expected_risky": False,
            "description": "一般條款 - 善意協商"
        },
        {
            "clause": "The Company reserves the right to modify these terms at any time without prior notice.",
            "lang": "en",
            "expected_risky": True,
            "description": "高風險條款 - 英文單方變更"
        },
        {
            "clause": "User grants the service provider a perpetual, royalty-free license to use uploaded content.",
            "lang": "en",
            "expected_risky": True,
            "description": "高風險條款 - 英文永久授權"
        },
        {
            "clause": "The parties agree to act in good faith to resolve any matters not covered by this agreement.",
            "lang": "en",
            "expected_risky": False,
            "description": "一般條款 - 英文善意協商"
        }
    ]
    
    passed = 0
    total = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 測試案例 {i}: {test_case['description']}")
        print(f"條款: {test_case['clause']}")
        
        # 測試本地規則初篩
        result = local_rule_filter(test_case['clause'], test_case['lang'])
        
        print(f"結果: {result['risk_level']['zh'] if test_case['lang'] == 'zh' else result['risk_level']['en']}")
        print(f"類型: {result['type']['zh'] if test_case['lang'] == 'zh' else result['type']['en']}")
        print(f"理由: {result['reason']}")
        
        # 檢查結果
        is_risky = result['is_risky']
        expected_risky = test_case['expected_risky']
        
        if is_risky == expected_risky:
            print("✅ 通過")
            passed += 1
        else:
            print(f"❌ 失敗 - 期望: {expected_risky}, 實際: {is_risky}")
    
    print(f"\n📊 測試結果: {passed}/{total} 通過")
    return passed == total

def test_analyze_clause_modes():
    """測試 analyze_clause 函式的不同模式"""
    print("\n🧪 開始測試 analyze_clause 的不同模式...")
    
    test_clause = "甲方有權隨時修改本服務條款，並不另行通知乙方。"
    
    # 測試快速模式
    print("\n🚀 測試快速分析模式:")
    fast_result = analyze_clause(test_clause, "zh", mode="fast")
    print(f"分析模式: {fast_result.get('analysis_mode', 'N/A')}")
    print(f"風險等級: {fast_result['risk_level']['zh']}")
    print(f"類型: {fast_result['type']['zh']}")
    
    # 測試精準模式（如果沒有 API key 會使用模擬模式）
    print("\n🎯 測試精準分析模式:")
    accurate_result = analyze_clause(test_clause, "zh", mode="accurate")
    print(f"分析模式: {accurate_result.get('analysis_mode', 'N/A')}")
    print(f"風險等級: {accurate_result['risk_level']['zh']}")
    print(f"類型: {accurate_result['type']['zh']}")
    
    print("\n✅ 模式測試完成")

def test_performance():
    """測試性能"""
    print("\n⚡ 開始性能測試...")
    
    import time
    
    test_clause = "甲方有權隨時修改本服務條款，並不另行通知乙方。"
    
    # 測試快速模式性能
    start_time = time.time()
    for _ in range(100):
        local_rule_filter(test_clause, "zh")
    fast_time = time.time() - start_time
    
    print(f"快速模式 100 次分析耗時: {fast_time:.3f} 秒")
    print(f"平均每次: {fast_time/100*1000:.2f} 毫秒")
    
    print("✅ 性能測試完成")

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 本地規則初篩功能測試")
    print("=" * 60)
    
    # 執行測試
    success = test_local_rule_filter()
    test_analyze_clause_modes()
    test_performance()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 所有測試通過！本地規則初篩功能正常運作。")
    else:
        print("⚠️ 部分測試失敗，請檢查實作。")
    print("=" * 60) 
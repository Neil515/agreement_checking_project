#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
端到端測試：驗證前端與後端的完整整合
"""

import requests
import json
import time

def test_end_to_end_integration():
    """測試前端與後端的完整整合"""
    print("🧪 開始端到端整合測試...")
    
    # 模擬前端發送的請求
    test_cases = [
        {
            "name": "快速模式測試",
            "request": {
                "text": "甲方有權隨時修改本服務條款，並不另行通知乙方。",
                "lang": "auto",
                "mode": "fast"
            },
            "expected_mode": "fast",
            "expected_time": 5  # 期望在5秒內完成
        },
        {
            "name": "精準模式測試",
            "request": {
                "text": "乙方同意授權甲方無償使用其上傳資料用於行銷用途。",
                "lang": "auto",
                "mode": "accurate"
            },
            "expected_mode": "accurate",
            "expected_time": 10  # 期望在10秒內完成
        },
        {
            "name": "預設模式測試（不指定mode）",
            "request": {
                "text": "本契約雙方應善意協商處理合約未盡事宜。",
                "lang": "auto"
            },
            "expected_mode": "fast",  # 預設應該使用快速模式
            "expected_time": 5
        }
    ]
    
    api_url = "http://localhost:5000/analyze"
    passed = 0
    total = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 測試案例 {i}: {test_case['name']}")
        print(f"請求內容: {json.dumps(test_case['request'], ensure_ascii=False)}")
        
        start_time = time.time()
        try:
            response = requests.post(api_url, json=test_case['request'], timeout=test_case['expected_time'])
            
            if response.status_code == 200:
                data = response.json()
                elapsed_time = time.time() - start_time
                
                # 檢查回應格式
                print(f"✅ 請求成功")
                print(f"分析模式: {data.get('analysis_mode')}")
                print(f"語言: {data.get('language')}")
                print(f"條款數量: {data.get('total_clauses')}")
                print(f"耗時: {elapsed_time:.3f} 秒")
                
                # 驗證分析模式
                actual_mode = data.get('analysis_mode')
                expected_mode = test_case['expected_mode']
                
                if actual_mode == expected_mode:
                    print(f"✅ 分析模式正確: {actual_mode}")
                    passed += 1
                else:
                    print(f"❌ 分析模式錯誤: 期望 {expected_mode}, 實際 {actual_mode}")
                
                # 驗證回應時間
                if elapsed_time <= test_case['expected_time']:
                    print(f"✅ 回應時間正常: {elapsed_time:.3f}秒")
                else:
                    print(f"⚠️ 回應時間較長: {elapsed_time:.3f}秒")
                
                # 顯示分析結果
                for j, clause in enumerate(data.get('clauses', []), 1):
                    print(f"  條款 {j}: {clause.get('risk_type', 'N/A')} - {clause.get('text', '')[:30]}...")
                
            else:
                print(f"❌ 請求失敗: {response.status_code}")
                print(response.text)
                
        except requests.exceptions.Timeout:
            print(f"❌ 請求超時 (超過 {test_case['expected_time']} 秒)")
        except Exception as e:
            print(f"❌ 請求錯誤: {e}")
    
    print(f"\n📊 端到端測試結果: {passed}/{total} 通過")
    return passed == total

def test_api_server_running():
    """檢查 API 伺服器是否正在運行"""
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        return True
    except:
        return False

def test_frontend_simulation():
    """模擬前端行為測試"""
    print("\n🧪 模擬前端行為測試...")
    
    # 模擬前端發送的不同模式請求
    test_requests = [
        {"text": "甲方有權隨時修改本服務條款。", "mode": "fast"},
        {"text": "乙方同意授權甲方無償使用資料。", "mode": "accurate"},
        {"text": "本契約雙方應善意協商。", "mode": "fast"}
    ]
    
    api_url = "http://localhost:5000/analyze"
    success_count = 0
    
    for i, request_data in enumerate(test_requests, 1):
        print(f"\n🔄 模擬前端請求 {i}: {request_data['mode']} 模式")
        
        try:
            response = requests.post(api_url, json=request_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 前端請求成功")
                print(f"  模式: {data.get('analysis_mode')}")
                print(f"  條款數: {data.get('total_clauses')}")
                success_count += 1
            else:
                print(f"❌ 前端請求失敗: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 前端請求錯誤: {e}")
    
    print(f"\n📊 前端模擬測試: {success_count}/{len(test_requests)} 成功")
    return success_count == len(test_requests)

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 端到端整合測試")
    print("=" * 60)
    
    # 檢查伺服器是否運行
    if not test_api_server_running():
        print("⚠️ API 伺服器未運行，請先啟動伺服器：")
        print("   python tools/api_server.py")
        print("=" * 60)
        exit(1)
    
    # 執行測試
    e2e_success = test_end_to_end_integration()
    frontend_success = test_frontend_simulation()
    
    print("\n" + "=" * 60)
    if e2e_success and frontend_success:
        print("🎉 端到端測試全部通過！前端與後端整合成功。")
    else:
        print("⚠️ 部分測試失敗，請檢查整合問題。")
    print("=" * 60)
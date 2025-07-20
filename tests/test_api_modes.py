#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 API 端點的分析模式功能
"""

import requests
import json
import time

def test_api_modes():
    """測試 API 端點的不同分析模式"""
    print("🧪 開始測試 API 端點的分析模式功能...")
    
    # 測試資料
    test_text = """
    甲方有權隨時修改本服務條款，並不另行通知乙方。
    乙方同意授權甲方無償使用其上傳資料用於行銷用途。
    本契約雙方應善意協商處理合約未盡事宜。
    """
    
    api_url = "http://localhost:5000/analyze"
    
    # 測試快速模式
    print("\n🚀 測試快速分析模式:")
    start_time = time.time()
    try:
        response = requests.post(api_url, json={
            "text": test_text,
            "lang": "auto",
            "mode": "fast"
        }, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            fast_time = time.time() - start_time
            print(f"✅ 快速模式成功")
            print(f"分析模式: {data.get('analysis_mode')}")
            print(f"語言: {data.get('language')}")
            print(f"條款數量: {data.get('total_clauses')}")
            print(f"耗時: {fast_time:.3f} 秒")
            
            # 顯示分析結果
            for i, clause in enumerate(data.get('clauses', []), 1):
                print(f"  條款 {i}: {clause.get('risk_type', 'N/A')} - {clause.get('text', '')[:30]}...")
        else:
            print(f"❌ 快速模式失敗: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ 快速模式錯誤: {e}")
    
    # 測試精準模式
    print("\n🎯 測試精準分析模式:")
    start_time = time.time()
    try:
        response = requests.post(api_url, json={
            "text": test_text,
            "lang": "auto",
            "mode": "accurate"
        }, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            accurate_time = time.time() - start_time
            print(f"✅ 精準模式成功")
            print(f"分析模式: {data.get('analysis_mode')}")
            print(f"語言: {data.get('language')}")
            print(f"條款數量: {data.get('total_clauses')}")
            print(f"耗時: {accurate_time:.3f} 秒")
            
            # 顯示分析結果
            for i, clause in enumerate(data.get('clauses', []), 1):
                print(f"  條款 {i}: {clause.get('risk_type', 'N/A')} - {clause.get('text', '')[:30]}...")
        else:
            print(f"❌ 精準模式失敗: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ 精準模式錯誤: {e}")
    
    # 測試預設模式（應該使用快速模式）
    print("\n🔧 測試預設模式（不指定 mode）:")
    start_time = time.time()
    try:
        response = requests.post(api_url, json={
            "text": test_text,
            "lang": "auto"
        }, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            default_time = time.time() - start_time
            print(f"✅ 預設模式成功")
            print(f"分析模式: {data.get('analysis_mode')}")
            print(f"耗時: {default_time:.3f} 秒")
        else:
            print(f"❌ 預設模式失敗: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ 預設模式錯誤: {e}")

def test_api_server_running():
    """檢查 API 伺服器是否正在運行"""
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        return True
    except:
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 API 端點分析模式測試")
    print("=" * 60)
    
    # 檢查伺服器是否運行
    if not test_api_server_running():
        print("⚠️ API 伺服器未運行，請先啟動伺服器：")
        print("   python tools/api_server.py")
        print("=" * 60)
        exit(1)
    
    # 執行測試
    test_api_modes()
    
    print("\n" + "=" * 60)
    print("✅ API 端點分析模式測試完成")
    print("=" * 60) 
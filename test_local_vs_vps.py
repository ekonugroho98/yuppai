#!/usr/bin/env python3
"""
Test script untuk membandingkan local vs VPS dengan proxy yang sama
"""

import requests
import time
import json
from datetime import datetime

def test_proxy_connection(proxy_url, test_name="Test"):
    """Test koneksi dengan proxy"""
    print(f"\n{'='*50}")
    print(f"🔍 {test_name}")
    print(f"{'='*50}")
    
    session = requests.Session()
    
    if proxy_url:
        session.proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
        print(f"🌐 Proxy: {proxy_url}")
    else:
        print("🌐 No proxy (direct connection)")
    
    # Test 1: Check IP
    try:
        print("\n1. Checking IP...")
        r = session.get('https://httpbin.org/ip', timeout=10)
        ip_info = r.json()
        current_ip = ip_info.get('origin', 'unknown')
        print(f"   ✅ IP: {current_ip}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Basic Yupp.ai connection
    try:
        print("\n2. Testing Yupp.ai basic connection...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        r = session.get('https://yupp.ai', headers=headers, timeout=10)
        print(f"   ✅ Status: {r.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 3: API endpoint
    try:
        print("\n3. Testing Yupp.ai API endpoint...")
        r = session.get('https://yupp.ai/api/authentication/session', headers=headers, timeout=10)
        print(f"   ✅ Status: {r.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Streaming endpoint simulation
    try:
        print("\n4. Testing streaming endpoint...")
        headers.update({
            'content-type': 'text/plain;charset=UTF-8',
            'next-action': '7f48888536e2f0c0163640837db291777c39cc40c3'
        })
        
        # Simulate streaming request
        test_data = json.dumps(["test", "test", "test message", "$undefined", "$undefined", [], "$undefined", [], "none", False])
        
        r = session.post(
            'https://yupp.ai/chat/test?stream=true',
            headers=headers,
            data=test_data.encode('utf-8'),
            timeout=30,
            stream=True
        )
        
        print(f"   ✅ Status: {r.status_code}")
        
        if r.status_code == 429:
            print("   ⚠️  RATE LIMITED DETECTED!")
            return False
        elif r.status_code == 200:
            print("   ✅ Streaming endpoint accessible")
            return True
        else:
            print(f"   ⚠️  Unexpected status: {r.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("🚀 Local vs VPS Proxy Test")
    print("Testing proxy: http://23673857ee9ee25b9423:746b6cd758b190ee@gw.dataimpulse.com:10000")
    
    proxy_url = "http://23673857ee9ee25b9423:746b6cd758b190ee@gw.dataimpulse.com:10000"
    
    # Test 1: Without proxy
    test_proxy_connection(None, "Test WITHOUT Proxy")
    
    # Test 2: With proxy
    test_proxy_connection(proxy_url, "Test WITH Proxy")
    
    # Test 3: Multiple attempts with proxy
    print(f"\n{'='*50}")
    print("🔄 Multiple attempts with proxy")
    print(f"{'='*50}")
    
    for attempt in range(3):
        print(f"\n--- Attempt {attempt + 1}/3 ---")
        
        if test_proxy_connection(proxy_url, f"Attempt {attempt + 1}"):
            print("✅ SUCCESS!")
            break
        else:
            print("❌ FAILED!")
            
            if attempt < 2:
                delay = 30
                print(f"Waiting {delay} seconds before next attempt...")
                time.sleep(delay)
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 SUMMARY")
    print(f"{'='*50}")
    print("If you see RATE LIMITED in VPS but not in local:")
    print("1. IP proxy sudah diblokir untuk VPS region")
    print("2. Yupp.ai mendeteksi pola berbeda di VPS")
    print("3. Perlu ganti proxy atau VPS region")
    print("\nIf you see RATE LIMITED in both:")
    print("1. IP proxy sudah diblokir global")
    print("2. Perlu ganti proxy dengan IP baru")

if __name__ == "__main__":
    main()
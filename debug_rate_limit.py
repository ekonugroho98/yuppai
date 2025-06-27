#!/usr/bin/env python3
"""
Debug script untuk masalah rate limiting di VPS
"""

import requests
import time
import json
import random
from datetime import datetime

def test_connection_with_proxy(proxy_url=None):
    """Test koneksi dengan atau tanpa proxy"""
    print(f"\n🔍 Testing connection to Yupp.ai...")
    print(f"Proxy: {proxy_url if proxy_url else 'None'}")
    
    session = requests.Session()
    
    if proxy_url:
        session.proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
    
    # Test 1: Basic connection
    try:
        print("1. Testing basic connection...")
        r = session.get('https://yupp.ai', timeout=10)
        print(f"   ✅ Status: {r.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Check IP
    try:
        print("2. Checking current IP...")
        r = session.get('https://httpbin.org/ip', timeout=10)
        ip_info = r.json()
        print(f"   ✅ IP: {ip_info.get('origin', 'unknown')}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: API endpoint
    try:
        print("3. Testing API endpoint...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        r = session.get('https://yupp.ai/api/authentication/session', headers=headers, timeout=10)
        print(f"   ✅ Status: {r.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Streaming endpoint (simulation)
    try:
        print("4. Testing streaming endpoint...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'content-type': 'text/plain;charset=UTF-8',
        }
        
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

def test_multiple_proxies(proxy_list):
    """Test multiple proxies"""
    print(f"\n🔄 Testing {len(proxy_list)} proxies...")
    
    working_proxies = []
    
    for i, proxy in enumerate(proxy_list, 1):
        print(f"\n--- Testing Proxy {i}/{len(proxy_list)}: {proxy} ---")
        
        if test_connection_with_proxy(proxy):
            working_proxies.append(proxy)
            print(f"   ✅ Proxy {i} WORKING")
        else:
            print(f"   ❌ Proxy {i} FAILED")
        
        # Delay between tests
        if i < len(proxy_list):
            delay = random.randint(5, 15)
            print(f"   Waiting {delay} seconds before next test...")
            time.sleep(delay)
    
    return working_proxies

def load_proxies_from_file(filename="proxy_list.txt"):
    """Load proxy list from file"""
    try:
        with open(filename, 'r') as f:
            proxies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return proxies
    except FileNotFoundError:
        print(f"File {filename} not found. Create it with one proxy per line.")
        return []

def main():
    print("🚀 Yupp.ai Rate Limit Debug Tool")
    print("=" * 50)
    
    # Test without proxy first
    print("\n📡 Testing WITHOUT proxy...")
    if test_connection_with_proxy():
        print("✅ Connection works without proxy")
    else:
        print("❌ Connection fails without proxy")
    
    # Test with proxy if available
    proxy_list = load_proxies_from_file()
    
    if proxy_list:
        print(f"\n📡 Testing with {len(proxy_list)} proxies...")
        working_proxies = test_multiple_proxies(proxy_list)
        
        if working_proxies:
            print(f"\n✅ Found {len(working_proxies)} working proxies:")
            for proxy in working_proxies:
                print(f"   - {proxy}")
        else:
            print("\n❌ No working proxies found!")
    else:
        print("\n⚠️  No proxy list found. Create 'proxy_list.txt' with one proxy per line.")
    
    # Recommendations
    print("\n" + "=" * 50)
    print("💡 RECOMMENDATIONS:")
    print("1. If no proxy works: Change VPS region/provider")
    print("2. If some proxies work: Use only working proxies")
    print("3. If all fail: Wait 1-2 hours before retrying")
    print("4. Consider using residential proxies")
    print("5. Update cookies with fresh session")

if __name__ == "__main__":
    main() 
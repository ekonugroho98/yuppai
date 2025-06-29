#!/usr/bin/env python3
"""
Radical Solution untuk Bypass Aggressive Detection
"""

import requests
import time
import random
import json
import sys
import subprocess
import os

def test_mobile_emulation():
    """Test dengan mobile emulation"""
    print("📱 Testing Mobile Emulation")
    print("=" * 50)
    
    # Mobile headers
    mobile_headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1'
    }
    
    session = requests.Session()
    session.headers.update(mobile_headers)
    
    try:
        response = session.get('https://yupp.ai', timeout=15)
        print(f"📊 Mobile Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Mobile emulation working!")
            return True
        elif response.status_code == 429:
            print("❌ Mobile also rate limited")
            return False
        else:
            print(f"⚠️  Mobile status: {response.status_code}")
            return True
            
    except Exception as e:
        print(f"❌ Mobile test error: {e}")
        return False

def test_with_curl():
    """Test dengan curl (bypass Python requests)"""
    print("\n🔧 Testing with cURL")
    print("=" * 50)
    
    try:
        # Test basic connection with curl
        cmd = [
            'curl', '-s', '-o', '/dev/null', '-w', '%{http_code}',
            '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            '-H', 'Accept-Language: en-US,en;q=0.9,id;q=0.8',
            '-H', 'Accept-Encoding: gzip, deflate, br',
            '-H', 'Connection: keep-alive',
            '-H', 'Upgrade-Insecure-Requests: 1',
            'https://yupp.ai'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            status_code = result.stdout.strip()
            print(f"📊 cURL Status: {status_code}")
            
            if status_code == '200':
                print("✅ cURL working!")
                return True
            elif status_code == '429':
                print("❌ cURL also rate limited")
                return False
            else:
                print(f"⚠️  cURL status: {status_code}")
                return True
        else:
            print(f"❌ cURL error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ cURL test error: {e}")
        return False

def test_different_domain():
    """Test dengan domain yang berbeda"""
    print("\n🌐 Testing Different Domain")
    print("=" * 50)
    
    # Test if it's specific to yupp.ai domain
    test_domains = [
        'https://httpbin.org/ip',
        'https://api.ipify.org',
        'https://ifconfig.me'
    ]
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    for domain in test_domains:
        try:
            print(f"📡 Testing: {domain}")
            response = session.get(domain, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ {domain} working!")
            else:
                print(f"   ❌ {domain} failed")
                
        except Exception as e:
            print(f"   ❌ {domain} error: {e}")

def test_with_proxy_rotation():
    """Test dengan proxy rotation yang lebih aggressive"""
    print("\n🔄 Testing Aggressive Proxy Rotation")
    print("=" * 50)
    
    try:
        with open('proxy.txt', 'r') as f:
            proxies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not proxies:
            print("❌ No proxies available")
            return False
        
        # Test each proxy with different delays
        for i, proxy in enumerate(proxies[:3]):  # Test first 3
            print(f"🔧 Testing proxy {i+1}: {proxy[:50]}...")
            
            if not proxy.startswith(('http://', 'https://', 'socks5://', 'socks4://')):
                proxy = f"socks5://{proxy}"
            
            session = requests.Session()
            session.proxies.update({
                'http': proxy,
                'https': proxy
            })
            
            # Use different headers for each proxy
            headers = {
                'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{120-i}.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive'
            }
            
            session.headers.update(headers)
            
            try:
                response = session.get('https://yupp.ai', timeout=15)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"   ✅ Proxy {i+1} working!")
                    return True
                elif response.status_code == 429:
                    print(f"   ❌ Proxy {i+1} rate limited")
                else:
                    print(f"   ⚠️  Proxy {i+1} status: {response.status_code}")
                
                # Wait longer between proxies
                if i < 2:
                    wait_time = random.uniform(10, 20)
                    print(f"   ⏳ Waiting {wait_time:.1f}s before next proxy...")
                    time.sleep(wait_time)
                    
            except Exception as e:
                print(f"   ❌ Proxy {i+1} error: {e}")
        
        return False
        
    except Exception as e:
        print(f"❌ Proxy rotation error: {e}")
        return False

def suggest_radical_solutions():
    """Suggest radical solutions"""
    print("\n💡 RADICAL SOLUTIONS:")
    print("=" * 50)
    
    print("1. 🏠 RESIDENTIAL PROXY")
    print("   - Use residential IP addresses")
    print("   - Services: Bright Data, Oxylabs, SmartProxy")
    print("   - More expensive but harder to detect")
    
    print("\n2. 🌍 GEO-LOCATION CHANGE")
    print("   - Use proxy from different country")
    print("   - Try proxies from: US, UK, Germany, Japan")
    print("   - Some countries have less aggressive detection")
    
    print("\n3. 📱 MOBILE PROXY")
    print("   - Use mobile network proxies")
    print("   - Mobile IPs are less likely to be blocked")
    print("   - Services: 4G/5G mobile proxies")
    
    print("\n4. 🔄 BROWSER AUTOMATION")
    print("   - Use Selenium/Playwright instead of requests")
    print("   - Real browser automation is harder to detect")
    print("   - More complex but more reliable")
    
    print("\n5. ⏰ TIME-BASED APPROACH")
    print("   - Wait 24-48 hours before retry")
    print("   - Rate limits might reset after longer time")
    print("   - Try during off-peak hours")
    
    print("\n6. 🎭 MULTI-ACCOUNT STRATEGY")
    print("   - Use different accounts with different patterns")
    print("   - Rotate between multiple accounts")
    print("   - Each account has different behavior")

def main():
    """Main function"""
    print("🚀 RADICAL SOLUTION TESTER")
    print("=" * 60)
    
    print("🔍 Testing radical bypass methods...")
    
    # Test 1: Mobile emulation
    print("\n1️⃣ Mobile Emulation Test")
    success1 = test_mobile_emulation()
    
    # Test 2: cURL test
    print("\n2️⃣ cURL Test")
    success2 = test_with_curl()
    
    # Test 3: Different domains
    print("\n3️⃣ Different Domains Test")
    test_different_domain()
    
    # Test 4: Aggressive proxy rotation
    print("\n4️⃣ Aggressive Proxy Rotation")
    success4 = test_with_proxy_rotation()
    
    if success1 or success2 or success4:
        print("\n🎉 Radical solution found!")
        if success1:
            print("💡 Use mobile emulation")
        if success2:
            print("💡 Use cURL instead of Python requests")
        if success4:
            print("💡 Use aggressive proxy rotation")
    else:
        print("\n❌ All radical solutions failed")
        suggest_radical_solutions()
        
        print("\n💡 FINAL RECOMMENDATIONS:")
        print("1. Contact proxy provider for residential IPs")
        print("2. Wait 24-48 hours before retry")
        print("3. Consider using browser automation (Selenium)")
        print("4. Try from different VPS provider/location")

if __name__ == "__main__":
    main() 
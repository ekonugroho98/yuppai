#!/usr/bin/env python3
"""
Script untuk bypass rate limiting dengan proxy rotation
"""

import requests
import time
import random
import sys
import os

def load_all_proxies():
    """Load semua proxy dari proxy.txt"""
    try:
        with open('proxy.txt', 'r') as f:
            proxy_lines = f.readlines()
    except FileNotFoundError:
        print("❌ proxy.txt tidak ditemukan")
        return []
    
    # Filter out empty lines and comments
    proxy_lines = [line.strip() for line in proxy_lines if line.strip() and not line.strip().startswith('#')]
    
    if not proxy_lines:
        print("❌ Tidak ada proxy yang valid di proxy.txt")
        return []
    
    return proxy_lines

def test_proxy_for_rate_limit(proxy_line):
    """Test single proxy untuk rate limiting"""
    formatted_proxy = proxy_line
    if not proxy_line.startswith(('http://', 'https://', 'socks5://', 'socks4://')):
        formatted_proxy = f"socks5://{proxy_line}"
    
    proxy_config = {
        'http': formatted_proxy,
        'https': formatted_proxy
    }
    
    session = requests.Session()
    session.proxies.update(proxy_config)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    try:
        # Test basic connection
        response = session.get('https://yupp.ai', timeout=10)
        
        if response.status_code == 200:
            return {
                'proxy': proxy_line,
                'formatted': formatted_proxy,
                'status': 'working',
                'status_code': response.status_code
            }
        elif response.status_code == 429:
            return {
                'proxy': proxy_line,
                'formatted': formatted_proxy,
                'status': 'rate_limited',
                'status_code': response.status_code
            }
        else:
            return {
                'proxy': proxy_line,
                'formatted': formatted_proxy,
                'status': 'other_error',
                'status_code': response.status_code
            }
    except Exception as e:
        return {
            'proxy': proxy_line,
            'formatted': formatted_proxy,
            'status': 'connection_error',
            'error': str(e)
        }

def find_working_proxy():
    """Temukan proxy yang tidak rate limited"""
    print("🔍 Mencari proxy yang tidak rate limited...")
    print("=" * 60)
    
    proxies = load_all_proxies()
    if not proxies:
        return None
    
    print(f"📝 Testing {len(proxies)} proxies...")
    
    working_proxies = []
    rate_limited_proxies = []
    error_proxies = []
    
    for i, proxy in enumerate(proxies, 1):
        print(f"🔧 Testing proxy {i}/{len(proxies)}: {proxy[:50]}...")
        
        result = test_proxy_for_rate_limit(proxy)
        
        if result['status'] == 'working':
            print(f"✅ Working: {proxy[:50]}...")
            working_proxies.append(result)
        elif result['status'] == 'rate_limited':
            print(f"❌ Rate limited: {proxy[:50]}...")
            rate_limited_proxies.append(result)
        else:
            print(f"⚠️  Error: {proxy[:50]}... - {result.get('error', 'Unknown error')}")
            error_proxies.append(result)
        
        # Small delay between tests
        time.sleep(1)
    
    print(f"\n📊 Results:")
    print(f"   Working: {len(working_proxies)}")
    print(f"   Rate limited: {len(rate_limited_proxies)}")
    print(f"   Errors: {len(error_proxies)}")
    
    if working_proxies:
        print(f"\n🎉 Found {len(working_proxies)} working proxies!")
        return working_proxies[0]  # Return first working proxy
    else:
        print(f"\n❌ No working proxies found!")
        return None

def create_working_proxy_file(working_proxy):
    """Buat file dengan proxy yang berfungsi"""
    with open('working_proxy.txt', 'w') as f:
        f.write(working_proxy['proxy'])
    
    print(f"✅ Working proxy disimpan ke working_proxy.txt")
    print(f"📝 Proxy: {working_proxy['proxy']}")

def test_with_working_proxy():
    """Test bot dengan proxy yang berfungsi"""
    print("\n🧪 Testing bot dengan working proxy...")
    
    # Copy working proxy to proxy.txt
    try:
        with open('working_proxy.txt', 'r') as f:
            working_proxy = f.read().strip()
        
        with open('proxy.txt', 'w') as f:
            f.write(working_proxy)
        
        print(f"✅ Updated proxy.txt with working proxy")
        
        # Test basic connection
        session = requests.Session()
        if not working_proxy.startswith(('http://', 'https://', 'socks5://', 'socks4://')):
            working_proxy = f"socks5://{working_proxy}"
        
        session.proxies.update({
            'http': working_proxy,
            'https': working_proxy
        })
        
        response = session.get('https://yupp.ai', timeout=10)
        if response.status_code == 200:
            print("✅ Connection test successful!")
            return True
        else:
            print(f"❌ Connection test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing working proxy: {e}")
        return False

def suggest_alternatives():
    """Suggest alternatives jika semua proxy rate limited"""
    print("\n💡 Alternatives jika semua proxy rate limited:")
    print("1. Tunggu 30-60 menit sebelum test lagi")
    print("2. Gunakan proxy service yang berbeda")
    print("3. Test tanpa proxy (jika memungkinkan)")
    print("4. Gunakan VPN atau residential proxy")
    print("5. Contact proxy provider untuk IP rotation")

def main():
    """Main function"""
    print("🚀 Rate Limit Bypass Tool")
    print("=" * 60)
    
    # Find working proxy
    working_proxy = find_working_proxy()
    
    if working_proxy:
        print(f"\n🏆 Best working proxy: {working_proxy['proxy']}")
        
        # Save working proxy
        create_working_proxy_file(working_proxy)
        
        # Test with working proxy
        if test_with_working_proxy():
            print("\n🎉 Ready to run bot!")
            print("💡 Run: python3 main.py")
        else:
            print("\n❌ Working proxy test failed")
    else:
        print("\n❌ No working proxies found")
        suggest_alternatives()

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Script untuk bypass VPS detection
"""

import requests
import time
import random
import json
import sys

def get_realistic_headers():
    """Generate realistic browser headers"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    
    user_agent = random.choice(user_agents)
    
    headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Cache-Control': 'max-age=0'
    }
    
    return headers

def simulate_human_behavior():
    """Simulate human-like behavior"""
    # Random delays like human
    time.sleep(random.uniform(1, 3))
    
    # Sometimes longer delays
    if random.random() < 0.2:
        time.sleep(random.uniform(3, 8))

def test_with_realistic_headers():
    """Test dengan headers yang lebih realistic"""
    print("🧪 Testing with Realistic Browser Headers")
    print("=" * 60)
    
    session = requests.Session()
    
    # Set realistic headers
    headers = get_realistic_headers()
    session.headers.update(headers)
    
    print(f"📝 Using User-Agent: {headers['User-Agent'][:50]}...")
    
    try:
        # First, visit the main page like a real browser
        print("📡 Visiting main page...")
        simulate_human_behavior()
        
        response = session.get('https://yupp.ai', timeout=15)
        print(f"📊 Main page status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Main page loaded successfully")
            
            # Simulate some time on the page
            time.sleep(random.uniform(2, 5))
            
            # Now test API endpoint
            print("📡 Testing API endpoint...")
            simulate_human_behavior()
            
            api_headers = {
                **headers,
                'Accept': '*/*',
                'Content-Type': 'application/json',
                'Origin': 'https://yupp.ai',
                'Referer': 'https://yupp.ai/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin'
            }
            
            response = session.post(
                'https://yupp.ai/api/authentication/session',
                json={"userId": "test"},
                headers=api_headers,
                timeout=15
            )
            
            print(f"📊 API status: {response.status_code}")
            print(f"📊 Response: {response.text[:200]}...")
            
            if response.status_code == 200:
                print("✅ API endpoint working!")
                return True
            elif response.status_code == 429:
                print("❌ Still rate limited (429)")
                return False
            else:
                print(f"⚠️  API endpoint: {response.status_code}")
                return True
                
        elif response.status_code == 429:
            print("❌ Main page rate limited (429)")
            return False
        else:
            print(f"⚠️  Main page: {response.status_code}")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_with_proxy_realistic():
    """Test dengan proxy dan headers realistic"""
    print("\n🧪 Testing with Proxy + Realistic Headers")
    print("=" * 60)
    
    # Load proxy
    try:
        with open('proxy.txt', 'r') as f:
            proxy_line = f.readline().strip()
            if proxy_line and not proxy_line.startswith('#'):
                if not proxy_line.startswith(('http://', 'https://', 'socks5://', 'socks4://')):
                    proxy_line = f"socks5://{proxy_line}"
                
                proxy_config = {
                    'http': proxy_line,
                    'https': proxy_line
                }
                
                print(f"🌐 Using proxy: {proxy_line[:50]}...")
                
                session = requests.Session()
                session.proxies.update(proxy_config)
                
                # Set realistic headers
                headers = get_realistic_headers()
                session.headers.update(headers)
                
                print(f"📝 Using User-Agent: {headers['User-Agent'][:50]}...")
                
                # Test with realistic behavior
                simulate_human_behavior()
                
                response = session.get('https://yupp.ai', timeout=15)
                print(f"📊 Status: {response.status_code}")
                
                if response.status_code == 200:
                    print("✅ Proxy + Realistic headers working!")
                    return True
                elif response.status_code == 429:
                    print("❌ Still rate limited with realistic headers")
                    return False
                else:
                    print(f"⚠️  Status: {response.status_code}")
                    return True
                    
    except Exception as e:
        print(f"❌ Proxy test error: {e}")
        return False

def create_realistic_config():
    """Create configuration untuk bypass VPS detection"""
    print("\n🔧 Creating Realistic Configuration")
    print("=" * 60)
    
    config = {
        "realistic_headers": True,
        "human_behavior": True,
        "random_delays": True,
        "browser_simulation": True
    }
    
    with open('realistic_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Realistic configuration created")
    print("💡 This will be used by the bot to bypass VPS detection")

def main():
    """Main function"""
    print("🚀 VPS Detection Bypass Tool")
    print("=" * 60)
    
    print("🔍 Testing VPS detection bypass methods...")
    
    # Test 1: Realistic headers without proxy
    print("\n1️⃣ Testing without proxy + realistic headers")
    success1 = test_with_realistic_headers()
    
    # Test 2: Realistic headers with proxy
    print("\n2️⃣ Testing with proxy + realistic headers")
    success2 = test_with_proxy_realistic()
    
    if success1 or success2:
        print("\n🎉 VPS detection bypass successful!")
        create_realistic_config()
        print("\n💡 Next steps:")
        print("   1. Run: python3 main.py")
        print("   2. Bot will use realistic headers automatically")
        print("   3. Choose sequential mode for better results")
    else:
        print("\n❌ VPS detection bypass failed")
        print("\n💡 Additional solutions:")
        print("   1. Use residential proxy service")
        print("   2. Run bot from different location")
        print("   3. Contact proxy provider for IP rotation")
        print("   4. Wait 1-2 hours before retry")

if __name__ == "__main__":
    main() 
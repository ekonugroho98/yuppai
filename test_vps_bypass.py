#!/usr/bin/env python3
"""
Comprehensive VPS Detection Bypass Test
"""

import requests
import time
import random
import json
import sys

def test_complete_flow():
    """Test complete bot flow dengan VPS bypass"""
    print("🧪 Testing Complete Bot Flow with VPS Bypass")
    print("=" * 60)
    
    # Create realistic session
    session = requests.Session()
    
    # Set realistic headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
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
        'sec-ch-ua-platform': '"Windows"'
    }
    
    session.headers.update(headers)
    
    try:
        # Step 1: Visit main page
        print("📡 Step 1: Visiting main page...")
        time.sleep(random.uniform(2, 4))
        
        response = session.get('https://yupp.ai', timeout=15)
        print(f"   Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Failed to load main page")
            return False
        
        # Step 2: Simulate time on page
        print("📡 Step 2: Simulating time on page...")
        time.sleep(random.uniform(3, 6))
        
        # Step 3: Test session endpoint
        print("📡 Step 3: Testing session endpoint...")
        
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
        
        time.sleep(random.uniform(1, 3))
        
        response = session.post(
            'https://yupp.ai/api/authentication/session',
            json={"userId": "test-user"},
            headers=api_headers,
            timeout=15
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}...")
        
        if response.status_code == 200:
            print("   ✅ Session endpoint working!")
        elif response.status_code == 429:
            print("   ❌ Still rate limited")
            return False
        else:
            print(f"   ⚠️  Unexpected status: {response.status_code}")
        
        # Step 4: Test streaming endpoint
        print("📡 Step 4: Testing streaming endpoint...")
        
        chat_id = "test-chat-id"
        turn_id = "test-turn-id"
        message = "Hello, this is a test message"
        
        stream_headers = {
            **api_headers,
            'Content-Type': 'text/plain;charset=UTF-8',
            'Next-Action': '7f48888536e2f0c0163640837db291777c39cc40c3'
        }
        
        data_list = [chat_id, turn_id, message, "$undefined", "$undefined", [], "$undefined", [], "none", False]
        chat_stream_data = json.dumps(data_list)
        
        time.sleep(random.uniform(2, 4))
        
        response = session.post(
            f'https://yupp.ai/chat/{chat_id}?stream=true',
            headers=stream_headers,
            data=chat_stream_data.encode('utf-8'),
            stream=True,
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Streaming endpoint working!")
            return True
        elif response.status_code == 429:
            print("   ❌ Streaming rate limited")
            return False
        else:
            print(f"   ⚠️  Streaming status: {response.status_code}")
            return True
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_with_proxy():
    """Test dengan proxy"""
    print("\n🧪 Testing with Proxy")
    print("=" * 60)
    
    try:
        with open('proxy.txt', 'r') as f:
            proxy_line = f.readline().strip()
            if proxy_line and not proxy_line.startswith('#'):
                if not proxy_line.startswith(('http://', 'https://', 'socks5://', 'socks4://')):
                    proxy_line = f"socks5://{proxy_line}"
                
                print(f"🌐 Using proxy: {proxy_line[:50]}...")
                
                session = requests.Session()
                session.proxies.update({
                    'http': proxy_line,
                    'https': proxy_line
                })
                
                # Use same realistic headers
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
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
                    'sec-ch-ua-platform': '"Windows"'
                }
                
                session.headers.update(headers)
                
                # Test basic connection
                response = session.get('https://yupp.ai', timeout=15)
                print(f"📊 Status: {response.status_code}")
                
                if response.status_code == 200:
                    print("✅ Proxy + VPS bypass working!")
                    return True
                elif response.status_code == 429:
                    print("❌ Still rate limited with proxy")
                    return False
                else:
                    print(f"⚠️  Status: {response.status_code}")
                    return True
                    
    except Exception as e:
        print(f"❌ Proxy test error: {e}")
        return False

def main():
    """Main function"""
    print("🚀 VPS Detection Bypass Test")
    print("=" * 60)
    
    # Test without proxy
    print("1️⃣ Testing without proxy...")
    success1 = test_complete_flow()
    
    # Test with proxy
    print("\n2️⃣ Testing with proxy...")
    success2 = test_with_proxy()
    
    if success1 or success2:
        print("\n🎉 VPS detection bypass successful!")
        print("\n💡 Bot should now work with:")
        print("   - Realistic browser headers")
        print("   - Human-like behavior simulation")
        print("   - Proper request sequencing")
        print("   - Random delays")
        
        print("\n💡 Run bot with:")
        print("   python3 main.py")
        print("   Choose: Sequential mode, 1 account")
    else:
        print("\n❌ VPS detection bypass failed")
        print("\n💡 Additional solutions:")
        print("   1. Use residential proxy")
        print("   2. Run from different location")
        print("   3. Wait longer before retry")
        print("   4. Contact proxy provider")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Script untuk debug streaming response di VPS
"""

import requests
import json
import time
import sys

def test_streaming_connection():
    """Test koneksi streaming dan response format"""
    print("🔧 Testing streaming connection...")
    
    # Basic session setup
    session = requests.Session()
    session.headers.update({
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,id;q=0.8',
        'origin': 'https://yupp.ai',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    # Test cookies (you'll need to add your actual cookies here)
    test_cookies = {
        # Add your cookies here
    }
    session.cookies.update(test_cookies)
    
    # Test proxy if available
    proxy_config = None
    try:
        with open('proxy.txt', 'r') as f:
            proxy_line = f.read().strip()
            if proxy_line and not proxy_line.startswith('#'):
                # Parse proxy format
                if '@' in proxy_line:
                    # Format: protocol://username:password@host:port
                    if proxy_line.startswith(('http://', 'https://', 'socks5://', 'socks4://')):
                        proxy_config = {
                            'http': proxy_line,
                            'https': proxy_line
                        }
                    else:
                        # Assume socks5 if no protocol specified
                        proxy_config = {
                            'http': f'socks5://{proxy_line}',
                            'https': f'socks5://{proxy_line}'
                        }
                else:
                    # Format: host:port (no authentication)
                    if proxy_line.startswith(('http://', 'https://', 'socks5://', 'socks4://')):
                        proxy_config = {
                            'http': proxy_line,
                            'https': proxy_line
                        }
                    else:
                        # Assume http if no protocol specified
                        proxy_config = {
                            'http': f'http://{proxy_line}',
                            'https': f'http://{proxy_line}'
                        }
                
                if proxy_config:
                    print(f"🌐 Using proxy: {proxy_line[:50]}...")
                    session.proxies.update(proxy_config)
                    
                    # Test proxy connectivity first
                    print("🌐 Testing proxy connectivity...")
                    try:
                        proxy_test = session.get('https://httpbin.org/ip', timeout=10)
                        print(f"✅ Proxy test successful: {proxy_test.json()}")
                    except requests.exceptions.ProxyError as e:
                        print(f"❌ Proxy authentication failed: {e}")
                        print("💡 Check your proxy credentials in proxy.txt")
                        print("💡 Format should be: username:password@host:port")
                        return False
                    except Exception as e:
                        print(f"❌ Proxy connection failed: {e}")
                        return False
    except FileNotFoundError:
        print("🌐 No proxy.txt found, running without proxy")
    except Exception as e:
        print(f"🌐 Error reading proxy.txt: {e}")
        print("🌐 Running without proxy")
    
    # Test basic connection first
    try:
        print("📡 Testing basic connection to yupp.ai...")
        response = session.get('https://yupp.ai', timeout=10)
        print(f"✅ Basic connection successful: {response.status_code}")
    except Exception as e:
        print(f"❌ Basic connection failed: {e}")
        return False
    
    # Test API endpoints
    try:
        print("📡 Testing API endpoints...")
        user_id = "37cf0952-9403-4d29-bf7a-1d1c08368a4a"
        response = session.post('https://yupp.ai/api/authentication/session', 
                              json={"userId": user_id}, timeout=10)
        print(f"✅ Session endpoint: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Session endpoint failed: {e}")
    
    # Test streaming endpoint
    try:
        print("📡 Testing streaming endpoint...")
        chat_id = "test-chat-id"
        turn_id = "test-turn-id"
        message = "Hello, this is a test message"
        
        chat_stream_headers = {
            **session.headers,
            'content-type': 'text/plain;charset=UTF-8',
            'next-action': '7f48888536e2f0c0163640837db291777c39cc40c3'
        }
        
        data_list = [chat_id, turn_id, message, "$undefined", "$undefined", [], "$undefined", [], "none", False]
        chat_stream_data = json.dumps(data_list)
        
        print(f"📤 Sending data: {chat_stream_data[:100]}...")
        
        response_stream = session.post(
            f'https://yupp.ai/chat/{chat_id}?stream=true',
            headers=chat_stream_headers,
            data=chat_stream_data.encode('utf-8'),
            stream=True,
            timeout=30
        )
        
        print(f"📡 Streaming response status: {response_stream.status_code}")
        print(f"📡 Response headers: {dict(response_stream.headers)}")
        
        if response_stream.status_code == 200:
            print("📡 Reading streaming response...")
            line_count = 0
            for line in response_stream.iter_lines():
                if line:
                    line_count += 1
                    decoded_line = line.decode('utf-8')
                    print(f"📝 Line {line_count}: {decoded_line[:200]}...")
                    
                    if line_count >= 10:  # Only show first 10 lines
                        print("📝 ... (showing only first 10 lines)")
                        break
        else:
            print(f"❌ Streaming failed with status: {response_stream.status_code}")
            try:
                error_text = response_stream.text
                print(f"❌ Error response: {error_text[:500]}...")
            except:
                pass
                
    except Exception as e:
        print(f"❌ Streaming test failed: {e}")
        import traceback
        traceback.print_exc()
    
    return True

if __name__ == "__main__":
    print("🚀 Streaming Debug Test")
    print("=" * 50)
    
    success = test_streaming_connection()
    
    if success:
        print("\n✅ Debug test completed")
    else:
        print("\n❌ Debug test failed")
        sys.exit(1) 
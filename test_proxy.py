#!/usr/bin/env python3
"""
Script untuk test proxy configuration
"""

import requests
import sys
import os

def test_proxy_configuration():
    """Test proxy configuration dari proxy.txt"""
    print("🔧 Testing Proxy Configuration")
    print("=" * 50)
    
    # Read proxy configuration
    try:
        with open('proxy.txt', 'r') as f:
            proxy_lines = f.readlines()
    except FileNotFoundError:
        print("❌ proxy.txt tidak ditemukan")
        return False
    
    # Filter out empty lines and comments
    proxy_lines = [line.strip() for line in proxy_lines if line.strip() and not line.strip().startswith('#')]
    
    if not proxy_lines:
        print("❌ proxy.txt kosong atau hanya berisi komentar")
        return False
    
    # Use only the first proxy line
    proxy_line = proxy_lines[0]
    print(f"📝 Using first proxy line: {proxy_line}")
    
    if len(proxy_lines) > 1:
        print(f"⚠️  Found {len(proxy_lines)} proxy lines, using only the first one")
        print(f"   Other lines: {proxy_lines[1:3]}..." if len(proxy_lines) > 3 else f"   Other lines: {proxy_lines[1:]}")
    
    # Parse proxy format
    if '@' in proxy_line:
        print("🔍 Format: Proxy dengan authentication")
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
        print("🔍 Format: Proxy tanpa authentication")
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
    
    print(f"🔧 Parsed config: {proxy_config}")
    
    # Test proxy
    session = requests.Session()
    session.proxies.update(proxy_config)
    
    # Test 1: Basic connectivity
    print("\n🌐 Test 1: Basic connectivity...")
    try:
        response = session.get('https://httpbin.org/ip', timeout=10)
        print(f"✅ Success: {response.json()}")
    except requests.exceptions.ProxyError as e:
        print(f"❌ Proxy Error: {e}")
        if "407" in str(e):
            print("💡 Error 407: Authentication required")
            print("💡 Check username:password format in proxy.txt")
        elif "407 NO_USER" in str(e):
            print("💡 Error 407 NO_USER: Username missing or incorrect")
            print("💡 Format should be: username:password@host:port")
        return False
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False
    
    # Test 2: Test with yupp.ai
    print("\n🌐 Test 2: Connection to yupp.ai...")
    try:
        response = session.get('https://yupp.ai', timeout=10)
        print(f"✅ Success: Status {response.status_code}")
    except requests.exceptions.ProxyError as e:
        print(f"❌ Proxy Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False
    
    # Test 3: Test API endpoint
    print("\n🌐 Test 3: API endpoint test...")
    try:
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,id;q=0.8',
            'origin': 'https://yupp.ai',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = session.post('https://yupp.ai/api/authentication/session', 
                              json={"userId": "test"}, 
                              headers=headers,
                              timeout=10)
        print(f"✅ Success: Status {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
    except requests.exceptions.ProxyError as e:
        print(f"❌ Proxy Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False
    
    print("\n🎉 All proxy tests passed!")
    return True

def show_proxy_formats():
    """Show supported proxy formats"""
    print("\n📋 Supported Proxy Formats:")
    print("1. socks5://username:password@host:port")
    print("2. socks4://username:password@host:port")
    print("3. http://username:password@host:port")
    print("4. https://username:password@host:port")
    print("5. username:password@host:port (assumes socks5)")
    print("6. host:port (no authentication, assumes http)")

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == '--formats':
        show_proxy_formats()
        return
    
    success = test_proxy_configuration()
    
    if not success:
        print("\n❌ Proxy test failed!")
        print("\n💡 Troubleshooting tips:")
        print("1. Check proxy.txt format")
        print("2. Verify username:password")
        print("3. Test proxy manually with curl")
        print("4. Run: python3 test_proxy.py --formats")
        sys.exit(1)
    else:
        print("\n✅ Proxy is working correctly!")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Script untuk test proxy validation dan SOCKS support
"""

import sys
import os

# Add current directory to path to import from main.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_socks_import():
    """Test import SOCKS library"""
    try:
        import socks
        import socket
        print("✅ SOCKS library berhasil diimport")
        return True
    except ImportError as e:
        print(f"❌ SOCKS library tidak tersedia: {e}")
        return False

def test_proxy_validation():
    """Test proxy validation function"""
    try:
        # Import functions from main.py
        from main import validate_proxy_config, load_proxy_config
        
        print("\n🧪 Testing Proxy Validation...")
        
        # Test HTTP proxy
        http_proxy = {
            'http': 'http://user:pass@host:port',
            'https': 'http://user:pass@host:port'
        }
        print(f"HTTP Proxy: {validate_proxy_config(http_proxy)}")
        
        # Test SOCKS5 proxy
        socks5_proxy = {
            'http': 'socks5://user:pass@host:port',
            'https': 'socks5://user:pass@host:port'
        }
        print(f"SOCKS5 Proxy: {validate_proxy_config(socks5_proxy)}")
        
        # Test SOCKS4 proxy
        socks4_proxy = {
            'http': 'socks4://user:pass@host:port',
            'https': 'socks4://user:pass@host:port'
        }
        print(f"SOCKS4 Proxy: {validate_proxy_config(socks4_proxy)}")
        
        # Test HTTPS proxy
        https_proxy = {
            'http': 'https://user:pass@host:port',
            'https': 'https://user:pass@host:port'
        }
        print(f"HTTPS Proxy: {validate_proxy_config(https_proxy)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing proxy validation: {e}")
        return False

def test_cookies_loading():
    """Test loading cookies with proxy"""
    try:
        from main import load_multiple_cookies_from_file
        
        print("\n📁 Testing Cookies Loading...")
        
        if os.path.exists('cookies.txt'):
            accounts = load_multiple_cookies_from_file()
            print(f"✅ Berhasil memuat {len(accounts)} accounts dari cookies.txt")
            
            # Check proxy configuration for each account
            for i, account in enumerate(accounts[:3], 1):  # Check first 3 accounts
                proxy = account.get('proxy')
                if proxy:
                    proxy_url = proxy.get('http', 'N/A')
                    print(f"   Account #{i}: {proxy_url[:50]}...")
                else:
                    print(f"   Account #{i}: No proxy")
            
            return True
        else:
            print("⚠️  cookies.txt tidak ditemukan")
            return False
            
    except Exception as e:
        print(f"❌ Error testing cookies loading: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Proxy Validation Test")
    print("=" * 50)
    
    # Test SOCKS import
    socks_ok = test_socks_import()
    
    # Test proxy validation
    validation_ok = test_proxy_validation()
    
    # Test cookies loading
    cookies_ok = test_cookies_loading()
    
    print("\n📊 Test Results:")
    print(f"   SOCKS Import: {'✅' if socks_ok else '❌'}")
    print(f"   Proxy Validation: {'✅' if validation_ok else '❌'}")
    print(f"   Cookies Loading: {'✅' if cookies_ok else '❌'}")
    
    if all([socks_ok, validation_ok, cookies_ok]):
        print("\n🎉 Semua test berhasil! Bot siap digunakan dengan SOCKS proxy.")
    else:
        print("\n⚠️  Beberapa test gagal. Cek error di atas.") 
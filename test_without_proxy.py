#!/usr/bin/env python3
"""
Script untuk test bot tanpa proxy
"""

import requests
import time
import random
import sys
import os

def test_without_proxy():
    """Test koneksi tanpa proxy"""
    print("🧪 Testing Connection Without Proxy")
    print("=" * 50)
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    
    try:
        print("📡 Testing connection to yupp.ai...")
        response = session.get('https://yupp.ai', timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📊 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Connection successful without proxy!")
            return True
        elif response.status_code == 429:
            print("❌ Still rate limited (429) even without proxy")
            print("💡 This means the rate limiting is IP-based, not proxy-specific")
            return False
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
            return True
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints tanpa proxy"""
    print("\n🧪 Testing API Endpoints")
    print("=" * 50)
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
        'Origin': 'https://yupp.ai',
        'Referer': 'https://yupp.ai/',
    })
    
    # Test session endpoint
    try:
        print("📡 Testing session endpoint...")
        response = session.post('https://yupp.ai/api/authentication/session', 
                              json={"userId": "test"}, 
                              timeout=10)
        
        print(f"📊 Session Status: {response.status_code}")
        print(f"📊 Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("✅ Session endpoint working!")
        elif response.status_code == 429:
            print("❌ Session endpoint rate limited")
        else:
            print(f"⚠️  Session endpoint: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Session endpoint error: {e}")

def create_no_proxy_config():
    """Buat konfigurasi tanpa proxy"""
    print("\n🔧 Creating No-Proxy Configuration")
    print("=" * 50)
    
    # Backup current proxy.txt
    if os.path.exists('proxy.txt'):
        with open('proxy_backup.txt', 'w') as f:
            with open('proxy.txt', 'r') as src:
                f.write(src.read())
        print("✅ Backup created: proxy_backup.txt")
    
    # Create empty proxy.txt (no proxy)
    with open('proxy.txt', 'w') as f:
        f.write("# No proxy configuration\n")
        f.write("# Testing without proxy\n")
    
    print("✅ Created no-proxy configuration")

def restore_proxy_config():
    """Restore proxy configuration"""
    if os.path.exists('proxy_backup.txt'):
        with open('proxy.txt', 'w') as f:
            with open('proxy_backup.txt', 'r') as src:
                f.write(src.read())
        print("✅ Restored proxy configuration")

def main():
    """Main function"""
    print("🚀 No-Proxy Test Tool")
    print("=" * 50)
    
    # Test without proxy
    if test_without_proxy():
        print("\n🎉 Connection works without proxy!")
        
        # Test API endpoints
        test_api_endpoints()
        
        # Ask if user wants to test bot without proxy
        choice = input("\n💡 Test bot without proxy? (y/n): ").strip().lower()
        
        if choice == 'y':
            create_no_proxy_config()
            print("\n💡 Now run: python3 main.py")
            print("💡 Choose option 1 (no proxy) when prompted")
        else:
            print("\n💡 Keeping current proxy configuration")
            
    else:
        print("\n❌ Connection failed even without proxy")
        print("💡 This indicates:")
        print("   1. VPS IP is rate limited")
        print("   2. Network connectivity issues")
        print("   3. Server maintenance")
        
        # Ask if user wants to restore proxy config
        choice = input("\n💡 Restore proxy configuration? (y/n): ").strip().lower()
        if choice == 'y':
            restore_proxy_config()
            print("✅ Proxy configuration restored")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Script untuk test bot dengan delay yang lebih baik
"""

import subprocess
import sys
import time
import random

def test_single_account():
    """Test single account dengan delay yang lebih baik"""
    print("🧪 Testing Single Account dengan Delay")
    print("=" * 50)
    
    # Test dengan 1 account saja
    print("📝 Menjalankan bot dengan 1 account...")
    
    try:
        # Run the bot with specific parameters
        result = subprocess.run([
            sys.executable, "main.py"
        ], capture_output=True, text=True, timeout=300)  # 5 minutes timeout
        
        print("📤 Output:")
        print(result.stdout)
        
        if result.stderr:
            print("❌ Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ Test berhasil!")
            return True
        else:
            print(f"❌ Test gagal dengan return code: {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Test timeout setelah 5 menit")
        return False
    except Exception as e:
        print(f"❌ Error menjalankan test: {e}")
        return False

def check_rate_limiting():
    """Check apakah masih ada rate limiting"""
    print("\n🔍 Checking Rate Limiting Status")
    print("=" * 50)
    
    try:
        import requests
        
        # Test basic connection
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Load proxy if available
        try:
            with open('proxy.txt', 'r') as f:
                proxy_line = f.readline().strip()
                if proxy_line and not proxy_line.startswith('#'):
                    if not proxy_line.startswith(('http://', 'https://', 'socks5://', 'socks4://')):
                        proxy_line = f"socks5://{proxy_line}"
                    session.proxies.update({
                        'http': proxy_line,
                        'https': proxy_line
                    })
                    print(f"🌐 Using proxy: {proxy_line[:50]}...")
        except:
            print("🌐 No proxy configuration")
        
        # Test connection to yupp.ai
        print("📡 Testing connection to yupp.ai...")
        response = session.get('https://yupp.ai', timeout=10)
        
        if response.status_code == 200:
            print("✅ Connection successful")
            return True
        elif response.status_code == 429:
            print("❌ Still rate limited (429)")
            return False
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
            return True
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Bot Test dengan Delay")
    print("=" * 50)
    
    # Check rate limiting first
    if not check_rate_limiting():
        print("\n💡 Masih ada rate limiting. Tunggu beberapa menit sebelum test.")
        print("💡 Atau coba dengan proxy yang berbeda.")
        return
    
    # Wait a bit before testing
    wait_time = random.uniform(10, 20)
    print(f"\n⏳ Menunggu {wait_time:.1f} detik sebelum test...")
    time.sleep(wait_time)
    
    # Test single account
    success = test_single_account()
    
    if success:
        print("\n🎉 Test berhasil! Bot berfungsi dengan baik.")
        print("💡 Sekarang bisa menjalankan bot dengan multiple accounts.")
    else:
        print("\n❌ Test gagal. Check error di atas.")
        print("💡 Coba:")
        print("   1. Tunggu beberapa menit")
        print("   2. Gunakan proxy yang berbeda")
        print("   3. Check cookies.txt")

if __name__ == "__main__":
    main() 
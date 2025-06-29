#!/usr/bin/env python3
"""
Script untuk memperbaiki format proxy
"""

import os
import sys

def check_proxy_format():
    """Check dan perbaiki format proxy"""
    print("🔧 Checking Proxy Format")
    print("=" * 50)
    
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
    print(f"📝 Current proxy line: {proxy_line}")
    
    if len(proxy_lines) > 1:
        print(f"⚠️  Found {len(proxy_lines)} proxy lines, analyzing only the first one")
        print(f"   Other lines: {proxy_lines[1:3]}..." if len(proxy_lines) > 3 else f"   Other lines: {proxy_lines[1:]}")
        print("💡 Use manage_proxies.py to test all proxies")
    
    # Analyze the format
    if '@' in proxy_line:
        print("🔍 Format terdeteksi: Proxy dengan authentication")
        
        # Check if protocol is specified
        if proxy_line.startswith(('http://', 'https://', 'socks5://', 'socks4://')):
            print("✅ Protocol sudah ditentukan")
            protocol = proxy_line.split('://')[0] + '://'
            auth_part = proxy_line.split('://')[1]
        else:
            print("⚠️  Protocol tidak ditentukan, assuming socks5://")
            protocol = "socks5://"
            auth_part = proxy_line
        
        # Parse username:password@host:port
        if '@' in auth_part:
            credentials, host_port = auth_part.split('@', 1)
            if ':' in credentials:
                username, password = credentials.split(':', 1)
                print(f"✅ Username: {username}")
                print(f"✅ Password: {password[:3]}***")
            else:
                print("❌ Format credentials salah")
                print("💡 Format harus: username:password@host:port")
                return False
            
            print(f"✅ Host:Port: {host_port}")
            
            # Check if host:port format is correct
            if ':' in host_port:
                host, port = host_port.split(':', 1)
                try:
                    port_num = int(port)
                    print(f"✅ Port valid: {port_num}")
                except ValueError:
                    print("❌ Port tidak valid (bukan angka)")
                    return False
            else:
                print("❌ Format host:port salah")
                return False
                
        else:
            print("❌ Format authentication salah")
            print("💡 Format harus: username:password@host:port")
            return False
            
    else:
        print("🔍 Format terdeteksi: Proxy tanpa authentication")
        if proxy_line.startswith(('http://', 'https://', 'socks5://', 'socks4://')):
            print("✅ Protocol sudah ditentukan")
        else:
            print("⚠️  Protocol tidak ditentukan, assuming http://")
            proxy_line = f"http://{proxy_line}"
    
    print("\n✅ Proxy format looks correct!")
    return True

def suggest_fixes():
    """Suggest fixes untuk common proxy issues"""
    print("\n💡 Common Proxy Issues & Solutions:")
    print("=" * 50)
    
    print("\n1. Error 407 NO_USER:")
    print("   - Pastikan format: username:password@host:port")
    print("   - Jangan gunakan spasi")
    print("   - Contoh: socks5://user123:pass456@proxy.example.com:1080")
    
    print("\n2. Error 407 Authentication Required:")
    print("   - Check username dan password")
    print("   - Pastikan tidak ada karakter khusus yang perlu di-encode")
    print("   - Test dengan curl: curl --proxy socks5://user:pass@host:port https://httpbin.org/ip")
    
    print("\n3. Connection Timeout:")
    print("   - Check host dan port")
    print("   - Pastikan proxy server aktif")
    print("   - Test connectivity: ping host")
    
    print("\n4. SOCKS vs HTTP:")
    print("   - SOCKS5: socks5://user:pass@host:port")
    print("   - HTTP: http://user:pass@host:port")
    print("   - HTTPS: https://user:pass@host:port")

def create_test_proxy():
    """Create test proxy configuration"""
    print("\n🧪 Create Test Proxy Configuration")
    print("=" * 50)
    
    print("Masukkan detail proxy untuk testing:")
    
    protocol = input("Protocol (socks5/http/https): ").strip() or "socks5"
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    host = input("Host: ").strip()
    port = input("Port: ").strip()
    
    if not all([username, password, host, port]):
        print("❌ Semua field harus diisi")
        return
    
    # Create proxy string
    if protocol in ['socks5', 'socks4']:
        proxy_string = f"{protocol}://{username}:{password}@{host}:{port}"
    else:
        proxy_string = f"{protocol}://{username}:{password}@{host}:{port}"
    
    print(f"\n📝 Generated proxy string: {proxy_string}")
    
    # Save to file
    save = input("\nSimpan ke proxy.txt? (y/n): ").strip().lower()
    if save == 'y':
        with open('proxy.txt', 'w') as f:
            f.write(proxy_string)
        print("✅ Proxy disimpan ke proxy.txt")
        print("💡 Test dengan: python3 test_proxy.py")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--fix':
            suggest_fixes()
            return
        elif sys.argv[1] == '--create':
            create_test_proxy()
            return
    
    print("🔧 Proxy Format Checker")
    print("=" * 50)
    
    success = check_proxy_format()
    
    if not success:
        print("\n❌ Proxy format issues detected!")
        print("\n💡 Run these commands for help:")
        print("   python3 fix_proxy.py --fix     (show common fixes)")
        print("   python3 fix_proxy.py --create  (create new proxy config)")
        print("   python3 test_proxy.py          (test proxy connection)")
        sys.exit(1)
    else:
        print("\n✅ Proxy format is correct!")
        print("💡 Test connection with: python3 test_proxy.py")

if __name__ == "__main__":
    main() 
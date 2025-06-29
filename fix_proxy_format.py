#!/usr/bin/env python3
"""
Script untuk memperbaiki format proxy secara otomatis
"""

import os
import sys

def fix_proxy_format():
    """Perbaiki format proxy secara otomatis"""
    print("🔧 Auto Fix Proxy Format")
    print("=" * 50)
    
    try:
        with open('proxy.txt', 'r') as f:
            proxy_lines = f.readlines()
    except FileNotFoundError:
        print("❌ proxy.txt tidak ditemukan")
        return False
    
    # Filter out empty lines and comments
    original_lines = [line.strip() for line in proxy_lines if line.strip() and not line.strip().startswith('#')]
    
    if not original_lines:
        print("❌ Tidak ada proxy yang valid di proxy.txt")
        return False
    
    print(f"📝 Found {len(original_lines)} proxy lines")
    
    # Fix each proxy line
    fixed_lines = []
    for i, line in enumerate(original_lines):
        print(f"\n🔧 Fixing line {i+1}: {line}")
        
        if '@' in line:
            # Proxy dengan authentication
            if line.startswith(('http://', 'https://', 'socks5://', 'socks4://')):
                print(f"   ✅ Already has protocol: {line}")
                fixed_lines.append(line)
            else:
                # Add socks5:// prefix
                fixed_line = f"socks5://{line}"
                print(f"   🔧 Added socks5:// prefix: {fixed_line}")
                fixed_lines.append(fixed_line)
        else:
            # Proxy tanpa authentication
            if line.startswith(('http://', 'https://', 'socks5://', 'socks4://')):
                print(f"   ✅ Already has protocol: {line}")
                fixed_lines.append(line)
            else:
                # Add http:// prefix
                fixed_line = f"http://{line}"
                print(f"   🔧 Added http:// prefix: {fixed_line}")
                fixed_lines.append(fixed_line)
    
    # Create backup
    backup_file = 'proxy_backup.txt'
    with open(backup_file, 'w') as f:
        f.writelines(proxy_lines)
    print(f"\n💾 Backup created: {backup_file}")
    
    # Save fixed proxies
    with open('proxy.txt', 'w') as f:
        for line in fixed_lines:
            f.write(line + '\n')
    
    print(f"\n✅ Fixed {len(fixed_lines)} proxy lines")
    print("📝 Updated proxy.txt with correct format")
    
    return True

def show_fixed_proxies():
    """Tampilkan proxy yang sudah diperbaiki"""
    try:
        with open('proxy.txt', 'r') as f:
            lines = f.readlines()
        
        print("\n📋 Fixed proxy lines:")
        for i, line in enumerate(lines, 1):
            if line.strip() and not line.strip().startswith('#'):
                print(f"   {i}. {line.strip()}")
    except FileNotFoundError:
        print("❌ proxy.txt tidak ditemukan")

def main():
    """Main function"""
    print("🔧 Auto Fix Proxy Format")
    print("=" * 50)
    
    success = fix_proxy_format()
    
    if success:
        show_fixed_proxies()
        print("\n💡 Next steps:")
        print("1. Test proxies: python3 manage_proxies.py")
        print("2. Test single proxy: python3 test_proxy.py")
        print("3. Run bot: python3 main.py")
    else:
        print("\n❌ Failed to fix proxy format")
        sys.exit(1)

if __name__ == "__main__":
    main() 
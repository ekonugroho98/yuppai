#!/usr/bin/env python3
"""
Script untuk mengubah proxy dari HTTP ke SOCKS5 di file cookies.txt
"""

import re

def convert_proxy_to_socks5(input_file="cookies.txt", output_file="cookies_socks5.txt"):
    """
    Mengubah semua proxy dari HTTP ke SOCKS5
    """
    print("🔄 Mengubah proxy dari HTTP ke SOCKS5...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern untuk mencari baris PROXY:http://...
        proxy_pattern = r'PROXY:http://([^:]+):([^:]+)@([^:]+):(\d+)'
        
        def replace_proxy(match):
            username = match.group(1)
            password = match.group(2)
            host = match.group(3)
            port = match.group(4)
            
            # Ubah ke format SOCKS5
            socks5_proxy = f"PROXY:socks5://{username}:{password}@{host}:{port}"
            print(f"   🔄 {match.group(0)} -> {socks5_proxy}")
            return socks5_proxy
        
        # Lakukan replacement
        new_content = re.sub(proxy_pattern, replace_proxy, content)
        
        # Tulis ke file baru
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Berhasil mengubah proxy dan menyimpan ke {output_file}")
        print(f"📊 Total perubahan: {len(re.findall(proxy_pattern, content))} proxy")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: File {input_file} tidak ditemukan")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def backup_original_file(filename="cookies.txt"):
    """
    Membuat backup dari file asli
    """
    import shutil
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"cookies_backup_{timestamp}.txt"
    
    try:
        shutil.copy2(filename, backup_filename)
        print(f"💾 Backup file asli disimpan sebagai: {backup_filename}")
        return True
    except Exception as e:
        print(f"⚠️  Warning: Gagal membuat backup: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Konverter Proxy HTTP ke SOCKS5")
    print("=" * 50)
    
    # Buat backup terlebih dahulu
    backup_original_file()
    
    # Konversi proxy
    success = convert_proxy_to_socks5()
    
    if success:
        print("\n🎉 Konversi selesai!")
        print("📝 File baru: cookies_socks5.txt")
        print("💡 Anda bisa mengganti cookies.txt dengan cookies_socks5.txt")
    else:
        print("\n❌ Konversi gagal!") 
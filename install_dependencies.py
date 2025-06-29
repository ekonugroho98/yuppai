#!/usr/bin/env python3
"""
Script untuk menginstall dependency yang diperlukan untuk SOCKS proxy support
"""

import subprocess
import sys

def install_dependencies():
    """Install dependency yang diperlukan"""
    print("🔧 Menginstall dependency untuk SOCKS proxy support...")
    
    dependencies = [
        "requests[socks]",
        "PySocks"
    ]
    
    for dep in dependencies:
        print(f"📦 Installing {dep}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} berhasil diinstall")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing {dep}: {e}")
            return False
    
    print("\n🎉 Semua dependency berhasil diinstall!")
    print("💡 Sekarang Anda bisa menggunakan SOCKS proxy (socks4://, socks5://)")
    return True

def test_socks_support():
    """Test apakah SOCKS support sudah tersedia"""
    print("\n🧪 Testing SOCKS support...")
    
    try:
        import socks
        import socket
        print("✅ SOCKS support tersedia")
        return True
    except ImportError as e:
        print(f"❌ SOCKS support tidak tersedia: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Installer Dependency SOCKS Proxy")
    print("=" * 50)
    
    success = install_dependencies()
    
    if success:
        test_socks_support()
    else:
        print("\n❌ Gagal menginstall dependency")
        print("💡 Coba jalankan manual: pip install requests[socks] PySocks") 
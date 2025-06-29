#!/usr/bin/env python3
"""
Setup script untuk VPS - install dependencies dan test environment
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run command dengan error handling"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} berhasil")
        if result.stdout:
            print(f"   Output: {result.stdout[:200]}...")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} gagal: {e}")
        if e.stdout:
            print(f"   Stdout: {e.stdout[:200]}...")
        if e.stderr:
            print(f"   Stderr: {e.stderr[:200]}...")
        return False

def check_python_version():
    """Check Python version"""
    print(f"🐍 Python version: {sys.version}")
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required")
        return False
    return True

def install_dependencies():
    """Install semua dependencies yang diperlukan"""
    print("\n📦 Installing dependencies...")
    
    dependencies = [
        "requests[socks]",
        "PySocks",
        "rich",
        "google-generativeai"
    ]
    
    for dep in dependencies:
        if not run_command(f"{sys.executable} -m pip install {dep}", f"Installing {dep}"):
            return False
    
    return True

def test_imports():
    """Test semua imports yang diperlukan"""
    print("\n🧪 Testing imports...")
    
    imports_to_test = [
        ("requests", "requests"),
        ("socks", "PySocks"),
        ("rich.console", "rich"),
        ("google.generativeai", "google-generativeai")
    ]
    
    for module, package in imports_to_test:
        try:
            __import__(module)
            print(f"✅ {package} imported successfully")
        except ImportError as e:
            print(f"❌ {package} import failed: {e}")
            return False
    
    return True

def test_socks_support():
    """Test SOCKS proxy support"""
    print("\n🧪 Testing SOCKS support...")
    
    try:
        import socks
        import socket
        print("✅ SOCKS support tersedia")
        return True
    except ImportError as e:
        print(f"❌ SOCKS support tidak tersedia: {e}")
        return False

def test_network_connectivity():
    """Test network connectivity"""
    print("\n🌐 Testing network connectivity...")
    
    try:
        import requests
        response = requests.get('https://httpbin.org/ip', timeout=10)
        print(f"✅ Network connectivity OK: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Network connectivity failed: {e}")
        return False

def create_test_files():
    """Create test files jika tidak ada"""
    print("\n📝 Creating test files...")
    
    # Create empty proxy.txt if not exists
    if not os.path.exists('proxy.txt'):
        with open('proxy.txt', 'w') as f:
            f.write("# Add your proxy here\n")
        print("✅ Created proxy.txt")
    
    # Create empty cookies.txt if not exists
    if not os.path.exists('cookies.txt'):
        with open('cookies.txt', 'w') as f:
            f.write("# Add your cookies here\n")
        print("✅ Created cookies.txt")
    
    # Create empty cookie.txt if not exists
    if not os.path.exists('cookie.txt'):
        with open('cookie.txt', 'w') as f:
            f.write("# Add your cookie here\n")
        print("✅ Created cookie.txt")

def main():
    """Main setup function"""
    print("🚀 VPS Setup Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Test imports
    if not test_imports():
        return False
    
    # Test SOCKS support
    if not test_socks_support():
        print("⚠️  SOCKS support not available - proxy may not work")
    
    # Test network connectivity
    if not test_network_connectivity():
        print("⚠️  Network connectivity issues detected")
    
    # Create test files
    create_test_files()
    
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Edit proxy.txt with your proxy configuration")
    print("2. Edit cookies.txt or cookie.txt with your cookies")
    print("3. Run: python main.py")
    print("4. If issues persist, run: python test_streaming_debug.py")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 
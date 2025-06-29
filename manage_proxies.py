#!/usr/bin/env python3
"""
Script untuk mengelola multiple proxies
"""

import requests
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def load_proxies():
    """Load semua proxy dari proxy.txt"""
    try:
        with open('proxy.txt', 'r') as f:
            proxy_lines = f.readlines()
    except FileNotFoundError:
        print("❌ proxy.txt tidak ditemukan")
        return []
    
    # Filter out empty lines and comments
    proxy_lines = [line.strip() for line in proxy_lines if line.strip() and not line.strip().startswith('#')]
    
    if not proxy_lines:
        print("❌ Tidak ada proxy yang valid di proxy.txt")
        return []
    
    return proxy_lines

def format_proxy(proxy_line):
    """Format proxy line dengan protocol yang benar"""
    if '@' in proxy_line:
        # Proxy dengan authentication
        if proxy_line.startswith(('http://', 'https://', 'socks5://', 'socks4://')):
            return proxy_line
        else:
            # Assume socks5 jika tidak ada protocol
            return f"socks5://{proxy_line}"
    else:
        # Proxy tanpa authentication
        if proxy_line.startswith(('http://', 'https://', 'socks5://', 'socks4://')):
            return proxy_line
        else:
            # Assume http jika tidak ada protocol
            return f"http://{proxy_line}"

def test_single_proxy(proxy_line, timeout=10):
    """Test single proxy"""
    formatted_proxy = format_proxy(proxy_line)
    
    proxy_config = {
        'http': formatted_proxy,
        'https': formatted_proxy
    }
    
    session = requests.Session()
    session.proxies.update(proxy_config)
    
    try:
        # Test basic connectivity
        response = session.get('https://httpbin.org/ip', timeout=timeout)
        if response.status_code == 200:
            ip_info = response.json()
            return {
                'proxy': proxy_line,
                'formatted': formatted_proxy,
                'status': 'success',
                'ip': ip_info.get('origin', 'unknown'),
                'response_time': response.elapsed.total_seconds()
            }
        else:
            return {
                'proxy': proxy_line,
                'formatted': formatted_proxy,
                'status': 'failed',
                'error': f'HTTP {response.status_code}'
            }
    except requests.exceptions.ProxyError as e:
        return {
            'proxy': proxy_line,
            'formatted': formatted_proxy,
            'status': 'failed',
            'error': f'Proxy Error: {str(e)}'
        }
    except requests.exceptions.Timeout:
        return {
            'proxy': proxy_line,
            'formatted': formatted_proxy,
            'status': 'failed',
            'error': 'Timeout'
        }
    except Exception as e:
        return {
            'proxy': proxy_line,
            'formatted': formatted_proxy,
            'status': 'failed',
            'error': f'Error: {str(e)}'
        }

def test_all_proxies():
    """Test semua proxy secara parallel"""
    proxies = load_proxies()
    
    if not proxies:
        return []
    
    print(f"🔧 Testing {len(proxies)} proxies...")
    print("=" * 60)
    
    results = []
    
    # Test proxies in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_proxy = {executor.submit(test_single_proxy, proxy): proxy for proxy in proxies}
        
        for future in as_completed(future_to_proxy):
            result = future.result()
            results.append(result)
            
            if result['status'] == 'success':
                print(f"✅ {result['proxy'][:50]}... - {result['ip']} ({result['response_time']:.2f}s)")
            else:
                print(f"❌ {result['proxy'][:50]}... - {result['error']}")
    
    return results

def select_best_proxy(results):
    """Pilih proxy terbaik berdasarkan response time"""
    working_proxies = [r for r in results if r['status'] == 'success']
    
    if not working_proxies:
        print("\n❌ Tidak ada proxy yang berfungsi!")
        return None
    
    # Sort by response time
    working_proxies.sort(key=lambda x: x['response_time'])
    
    best_proxy = working_proxies[0]
    print(f"\n🏆 Best proxy: {best_proxy['proxy']}")
    print(f"   IP: {best_proxy['ip']}")
    print(f"   Response time: {best_proxy['response_time']:.2f}s")
    
    return best_proxy

def save_working_proxy(proxy_line):
    """Simpan proxy yang berfungsi ke file terpisah"""
    with open('working_proxy.txt', 'w') as f:
        f.write(proxy_line)
    print("✅ Working proxy disimpan ke working_proxy.txt")

def create_single_proxy_file(proxy_line):
    """Buat file proxy.txt dengan hanya satu proxy"""
    with open('proxy.txt', 'w') as f:
        f.write(proxy_line)
    print("✅ proxy.txt diupdate dengan proxy yang berfungsi")

def show_proxy_stats(results):
    """Tampilkan statistik proxy"""
    total = len(results)
    working = len([r for r in results if r['status'] == 'success'])
    failed = total - working
    
    print(f"\n📊 Proxy Statistics:")
    print(f"   Total: {total}")
    print(f"   Working: {working}")
    print(f"   Failed: {failed}")
    print(f"   Success rate: {(working/total)*100:.1f}%")
    
    if working > 0:
        response_times = [r['response_time'] for r in results if r['status'] == 'success']
        avg_time = sum(response_times) / len(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        
        print(f"   Avg response time: {avg_time:.2f}s")
        print(f"   Min response time: {min_time:.2f}s")
        print(f"   Max response time: {max_time:.2f}s")

def main():
    """Main function"""
    print("🔧 Multiple Proxy Manager")
    print("=" * 60)
    
    # Test all proxies
    results = test_all_proxies()
    
    if not results:
        print("❌ Tidak ada proxy untuk ditest")
        return
    
    # Show statistics
    show_proxy_stats(results)
    
    # Select best proxy
    best_proxy = select_best_proxy(results)
    
    if best_proxy:
        print(f"\n💡 Actions:")
        print("1. Save working proxy to working_proxy.txt")
        print("2. Update proxy.txt with best proxy")
        print("3. Test best proxy with yupp.ai")
        
        choice = input("\nPilih action (1/2/3): ").strip()
        
        if choice == '1':
            save_working_proxy(best_proxy['proxy'])
        elif choice == '2':
            create_single_proxy_file(best_proxy['proxy'])
        elif choice == '3':
            print(f"\n🧪 Testing best proxy with yupp.ai...")
            test_result = test_single_proxy(best_proxy['proxy'])
            if test_result['status'] == 'success':
                print("✅ Proxy works with yupp.ai!")
            else:
                print(f"❌ Proxy failed with yupp.ai: {test_result['error']}")
        else:
            print("❌ Invalid choice")
    else:
        print("\n💡 No working proxies found. Check your proxy.txt file.")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Test untuk mengecek apakah proxy saat ini adalah datacenter IP
dan memberikan solusi residential proxy
"""

import requests
import json
import time

def check_proxy_ip_type(proxy):
    """Check apakah proxy adalah datacenter IP"""
    try:
        # Setup proxy
        if not proxy.startswith(('http://', 'https://', 'socks5://', 'socks4://')):
            proxy = f"socks5://{proxy}"
        
        proxies = {
            'http': proxy,
            'https': proxy
        }
        
        # Check IP info melalui proxy
        response = requests.get('https://ipapi.co/json/', proxies=proxies, timeout=15)
        
        if response.status_code == 200:
            ip_info = response.json()
            
            print(f"📍 Proxy IP: {ip_info.get('ip', 'Unknown')}")
            print(f"🏢 ISP: {ip_info.get('org', 'Unknown')}")
            print(f"🌍 Country: {ip_info.get('country_name', 'Unknown')}")
            print(f"📡 Type: {ip_info.get('type', 'Unknown')}")
            
            # Check if datacenter
            org = ip_info.get('org', '').lower()
            ip_type = ip_info.get('type', '').lower()
            
            datacenter_keywords = [
                'amazon', 'aws', 'google', 'gcp', 'microsoft', 'azure',
                'digitalocean', 'linode', 'vultr', 'ovh', 'hetzner',
                'hostinger', 'godaddy', 'bluehost', 'hostgator',
                'datacenter', 'server', 'vps', 'cloud', 'hosting'
            ]
            
            is_datacenter = False
            for keyword in datacenter_keywords:
                if keyword in org or keyword in ip_type:
                    is_datacenter = True
                    break
            
            if is_datacenter:
                print("❌ DATACENTER IP DETECTED!")
                return True
            else:
                print("✅ RESIDENTIAL IP DETECTED!")
                return False
                
        else:
            print(f"❌ Error checking proxy: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_all_proxies():
    """Test semua proxy untuk mengecek tipe IP"""
    print("🔍 CHECKING PROXY IP TYPES")
    print("=" * 50)
    
    try:
        with open('proxy.txt', 'r') as f:
            proxies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not proxies:
            print("❌ No proxies found in proxy.txt")
            return
        
        datacenter_count = 0
        residential_count = 0
        
        for i, proxy in enumerate(proxies[:3]):  # Test first 3
            print(f"\n🔧 Testing Proxy {i+1}: {proxy[:50]}...")
            
            is_datacenter = check_proxy_ip_type(proxy)
            
            if is_datacenter:
                datacenter_count += 1
            else:
                residential_count += 1
            
            time.sleep(2)  # Delay between tests
        
        print(f"\n📊 SUMMARY:")
        print(f"   Datacenter IPs: {datacenter_count}")
        print(f"   Residential IPs: {residential_count}")
        
        if datacenter_count > 0:
            print("\n❌ PROBLEM IDENTIFIED: You have datacenter proxies!")
            print("   yupp.ai blocks datacenter IPs aggressively")
            suggest_residential_proxies()
        else:
            print("\n✅ All proxies are residential")
            print("   The problem might be temporary rate limiting")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def suggest_residential_proxies():
    """Suggest residential proxy services"""
    print("\n💡 RESIDENTIAL PROXY SOLUTIONS:")
    print("=" * 50)
    
    print("1. 🌟 BRIGHT DATA (RECOMMENDED)")
    print("   - Best residential proxy service")
    print("   - 72M+ residential IPs")
    print("   - Cost: $15-500/month")
    print("   - Website: https://brightdata.com")
    
    print("\n2. 🌟 OXYLABS")
    print("   - High-quality residential proxies")
    print("   - 100M+ residential IPs")
    print("   - Cost: $15-300/month")
    print("   - Website: https://oxylabs.io")
    
    print("\n3. 🌟 SMARTPROXY")
    print("   - Good residential proxy service")
    print("   - 40M+ residential IPs")
    print("   - Cost: $10-200/month")
    print("   - Website: https://smartproxy.com")
    
    print("\n4. 🌟 PROXYSELLER")
    print("   - Affordable residential proxies")
    print("   - 2M+ residential IPs")
    print("   - Cost: $5-100/month")
    print("   - Website: https://proxyseller.com")
    
    print("\n5. 🌟 IPROYAL")
    print("   - Pay-per-use residential proxies")
    print("   - 2M+ residential IPs")
    print("   - Cost: $0.80/GB")
    print("   - Website: https://iproyal.com")

def create_proxy_migration_guide():
    """Create guide untuk migrasi ke residential proxy"""
    print("\n📋 MIGRATION GUIDE:")
    print("=" * 50)
    
    print("🎯 STEP 1: Choose Provider")
    print("   - Start with Bright Data or Oxylabs")
    print("   - They have the best success rate")
    print("   - Test with free trial first")
    
    print("\n🎯 STEP 2: Get Residential IPs")
    print("   - Request residential IPs only")
    print("   - Avoid datacenter IPs")
    print("   - Get IPs from your target country")
    
    print("\n🎯 STEP 3: Update Configuration")
    print("   - Replace proxy.txt with new residential IPs")
    print("   - Test each proxy individually")
    print("   - Use proper authentication")
    
    print("\n🎯 STEP 4: Test Thoroughly")
    print("   - Test with small requests first")
    print("   - Monitor for rate limiting")
    print("   - Adjust delays if needed")

def main():
    """Main function"""
    print("🚀 RESIDENTIAL PROXY ANALYZER")
    print("=" * 50)
    
    # Test all proxies
    test_all_proxies()
    
    # Create migration guide
    create_proxy_migration_guide()
    
    print("\n💡 IMMEDIATE ACTION:")
    print("1. Contact your current proxy provider")
    print("   - Ask if they have residential IPs")
    print("   - Request IP rotation to residential")
    print("   - Check pricing for residential")
    
    print("\n2. If no residential available:")
    print("   - Sign up for Bright Data trial")
    print("   - Test with residential IPs")
    print("   - Compare success rate")
    
    print("\n3. Alternative approach:")
    print("   - Wait 24-48 hours for rate limit reset")
    print("   - Try from different VPS location")
    print("   - Use mobile hotspot temporarily")

if __name__ == "__main__":
    main() 
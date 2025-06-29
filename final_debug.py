#!/usr/bin/env python3
"""
Final Debug - Analisis Mendalam Masalah Rate Limiting
"""

import requests
import time
import json
import subprocess
import sys
from datetime import datetime

def check_ip_info():
    """Check IP information"""
    print("🌐 CHECKING IP INFORMATION")
    print("=" * 50)
    
    try:
        # Check current IP
        response = requests.get('https://httpbin.org/ip', timeout=10)
        if response.status_code == 200:
            ip_data = response.json()
            current_ip = ip_data.get('origin', 'Unknown')
            print(f"📍 Current IP: {current_ip}")
        
        # Check IP details
        response = requests.get('https://ipapi.co/json/', timeout=10)
        if response.status_code == 200:
            ip_info = response.json()
            print(f"🏢 ISP: {ip_info.get('org', 'Unknown')}")
            print(f"🌍 Country: {ip_info.get('country_name', 'Unknown')}")
            print(f"🏙️  City: {ip_info.get('city', 'Unknown')}")
            print(f"📡 Type: {ip_info.get('type', 'Unknown')}")
            
            # Check if it's datacenter
            if 'datacenter' in ip_info.get('type', '').lower():
                print("⚠️  WARNING: This is a datacenter IP!")
                return True
            else:
                print("✅ This appears to be a residential IP")
                return False
                
    except Exception as e:
        print(f"❌ Error checking IP: {e}")
        return False

def test_yupp_specific():
    """Test yupp.ai specific endpoints"""
    print("\n🎯 TESTING YUPP.AI SPECIFIC")
    print("=" * 50)
    
    endpoints = [
        'https://yupp.ai',
        'https://yupp.ai/api',
        'https://yupp.ai/login',
        'https://yupp.ai/register'
    ]
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive'
    })
    
    for endpoint in endpoints:
        try:
            print(f"📡 Testing: {endpoint}")
            response = session.get(endpoint, timeout=15)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 429:
                print("   ❌ Rate limited")
            elif response.status_code == 200:
                print("   ✅ Working!")
                return True
            else:
                print(f"   ⚠️  Status: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return False

def test_with_different_user_agents():
    """Test dengan berbagai User-Agent"""
    print("\n🤖 TESTING DIFFERENT USER-AGENTS")
    print("=" * 50)
    
    user_agents = [
        # Desktop browsers
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        
        # Mobile browsers
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 14; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        
        # Old browsers (less likely to be blocked)
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]
    
    for i, ua in enumerate(user_agents):
        try:
            print(f"🤖 Testing UA {i+1}: {ua[:50]}...")
            
            session = requests.Session()
            session.headers.update({
                'User-Agent': ua,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive'
            })
            
            response = session.get('https://yupp.ai', timeout=15)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ This UA works!")
                return ua
            elif response.status_code == 429:
                print("   ❌ Still rate limited")
            else:
                print(f"   ⚠️  Status: {response.status_code}")
                
            time.sleep(2)  # Small delay between tests
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return None

def check_rate_limit_headers():
    """Check rate limit headers"""
    print("\n⏰ CHECKING RATE LIMIT HEADERS")
    print("=" * 50)
    
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        response = session.get('https://yupp.ai', timeout=15)
        
        print(f"📊 Status: {response.status_code}")
        print("📋 Headers:")
        
        rate_limit_headers = [
            'Retry-After',
            'X-RateLimit-Limit',
            'X-RateLimit-Remaining',
            'X-RateLimit-Reset',
            'RateLimit-Limit',
            'RateLimit-Remaining',
            'RateLimit-Reset'
        ]
        
        for header in rate_limit_headers:
            value = response.headers.get(header)
            if value:
                print(f"   {header}: {value}")
        
        # Check for any custom headers
        print("\n🔍 All Headers:")
        for key, value in response.headers.items():
            if 'rate' in key.lower() or 'limit' in key.lower() or 'retry' in key.lower():
                print(f"   {key}: {value}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

def suggest_realistic_solutions():
    """Suggest realistic solutions based on findings"""
    print("\n💡 REALISTIC SOLUTIONS:")
    print("=" * 50)
    
    print("1. 🏠 RESIDENTIAL PROXY (MOST LIKELY TO WORK)")
    print("   - Your current proxies are likely datacenter IPs")
    print("   - yupp.ai blocks datacenter IPs aggressively")
    print("   - Need residential IP addresses")
    print("   - Services: Bright Data, Oxylabs, SmartProxy")
    print("   - Cost: $10-50/month")
    
    print("\n2. ⏰ WAIT AND RETRY")
    print("   - Rate limits might reset after 24-48 hours")
    print("   - Try again tomorrow or next week")
    print("   - Some services have temporary blocks")
    
    print("\n3. 🌍 DIFFERENT LOCATION")
    print("   - Try from different VPS provider")
    print("   - Different country/region")
    print("   - Some regions have less aggressive blocking")
    
    print("\n4. 📱 MOBILE NETWORK")
    print("   - Use mobile hotspot")
    print("   - Mobile IPs are less likely to be blocked")
    print("   - Test from your phone first")
    
    print("\n5. 🔄 BROWSER AUTOMATION")
    print("   - Use Selenium/Playwright")
    print("   - Real browser is harder to detect")
    print("   - More complex but more reliable")

def create_action_plan():
    """Create specific action plan"""
    print("\n📋 ACTION PLAN:")
    print("=" * 50)
    
    print("🎯 IMMEDIATE ACTIONS:")
    print("1. Contact your proxy provider")
    print("   - Ask for residential IPs")
    print("   - Request IP rotation")
    print("   - Check if they have mobile proxies")
    
    print("\n2. Test from different location")
    print("   - Try from your local machine")
    print("   - Use mobile hotspot")
    print("   - Test from different VPS provider")
    
    print("\n3. Wait and monitor")
    print("   - Wait 24-48 hours")
    print("   - Check if rate limit resets")
    print("   - Monitor for any changes")
    
    print("\n4. Alternative approach")
    print("   - Consider browser automation")
    print("   - Use different service if possible")
    print("   - Manual operation temporarily")

def main():
    """Main function"""
    print("🚀 FINAL DEBUG - ANALISIS MENDALAM")
    print("=" * 60)
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check IP information
    is_datacenter = check_ip_info()
    
    # Test yupp.ai specific
    yupp_working = test_yupp_specific()
    
    # Test different user agents
    working_ua = test_with_different_user_agents()
    
    # Check rate limit headers
    check_rate_limit_headers()
    
    # Analysis
    print("\n🔍 ANALYSIS:")
    print("=" * 50)
    
    if is_datacenter:
        print("❌ PROBLEM IDENTIFIED: Datacenter IP")
        print("   - yupp.ai blocks datacenter IPs")
        print("   - Need residential IP addresses")
    else:
        print("✅ IP type looks good")
    
    if yupp_working:
        print("✅ Some yupp.ai endpoints working")
    else:
        print("❌ All yupp.ai endpoints blocked")
    
    if working_ua:
        print(f"✅ Found working User-Agent: {working_ua[:50]}...")
    else:
        print("❌ No User-Agent works")
    
    # Suggest solutions
    suggest_realistic_solutions()
    
    # Create action plan
    create_action_plan()
    
    print("\n💡 FINAL RECOMMENDATION:")
    if is_datacenter:
        print("🎯 PRIORITY: Get residential proxies")
        print("   This is most likely to solve the problem")
    else:
        print("🎯 PRIORITY: Wait 24-48 hours and retry")
        print("   Rate limit might reset automatically")

if __name__ == "__main__":
    main() 
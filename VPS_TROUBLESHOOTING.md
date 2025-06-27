# 🔧 VPS Troubleshooting Guide

## Masalah: Streaming Connection Gagal di VPS

### Gejala
- ✅ Local: Koneksi streaming berhasil
- ❌ VPS: "Streaming selesai tetapi tidak ada Reward ID yang ditemukan"

## 🔍 Penyebab Umum

### 1. **Network/Firewall Issues**
```bash
# Test koneksi ke Yupp.ai
curl -I https://yupp.ai
curl -I https://yupp.ai/chat/test

# Test dengan timeout
curl --connect-timeout 10 --max-time 30 https://yupp.ai
```

### 2. **DNS Resolution**
```bash
# Test DNS
nslookup yupp.ai
dig yupp.ai

# Gunakan DNS Google
echo "nameserver 8.8.8.8" | sudo tee -a /etc/resolv.conf
echo "nameserver 8.8.4.4" | sudo tee -a /etc/resolv.conf
```

### 3. **Proxy Configuration**
```bash
# Test proxy manual
curl -x your_proxy:port https://httpbin.org/ip

# Test tanpa proxy
curl https://httpbin.org/ip
```

### 4. **Python/Requests Issues**
```bash
# Update pip dan requests
pip install --upgrade pip
pip install --upgrade requests

# Test requests
python3 -c "
import requests
try:
    r = requests.get('https://yupp.ai', timeout=10)
    print(f'Status: {r.status_code}')
except Exception as e:
    print(f'Error: {e}')
"
```

## 🛠️ Solusi

### Solusi 1: Tambahkan Timeout dan Retry
```python
# Tambahkan di main.py sebelum response_stream
import time

max_retries = 3
retry_count = 0

while retry_count < max_retries:
    try:
        response_stream = session.post(
            f'https://yupp.ai/chat/{chat_id}?stream=true', 
            headers=chat_stream_headers, 
            data=chat_stream_data.encode('utf-8'), 
            stream=True,
            timeout=(30, 60)  # (connect_timeout, read_timeout)
        )
        
        if response_stream.status_code == 200:
            # Process stream
            break
        else:
            print(f"HTTP Status: {response_stream.status_code}")
            
    except requests.exceptions.Timeout:
        print(f"Timeout attempt {retry_count + 1}")
    except Exception as e:
        print(f"Error attempt {retry_count + 1}: {e}")
    
    retry_count += 1
    if retry_count < max_retries:
        time.sleep(5)
```

### Solusi 2: Gunakan Session dengan Konfigurasi Khusus
```python
# Buat session dengan konfigurasi VPS-friendly
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
})

# Tambahkan adapter dengan retry
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)

adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)
```

### Solusi 3: Debug Network
```bash
# Install tools debugging
sudo apt update
sudo apt install -y curl wget netcat-openbsd telnet

# Test koneksi
nc -zv yupp.ai 443
telnet yupp.ai 443

# Test dengan wget
wget --timeout=10 --tries=3 https://yupp.ai
```

### Solusi 4: Konfigurasi System
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python dependencies
sudo apt install -y python3-pip python3-venv

# Set ulimit untuk lebih banyak connections
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

# Restart session atau reboot
ulimit -n 65536
```

### Solusi 5: Gunakan Different Network Stack
```python
# Tambahkan di awal script
import socket
import ssl

# Force IPv4
socket.setdefaulttimeout(30)

# Custom SSL context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
```

## 🔧 Script Debug

### Debug Script
```python
#!/usr/bin/env python3
import requests
import json
import time

def test_yupp_connection():
    print("🔍 Testing Yupp.ai connection...")
    
    # Test 1: Basic connection
    try:
        r = requests.get('https://yupp.ai', timeout=10)
        print(f"✅ Basic connection: {r.status_code}")
    except Exception as e:
        print(f"❌ Basic connection failed: {e}")
        return False
    
    # Test 2: API endpoint
    try:
        r = requests.get('https://yupp.ai/api/authentication/session', timeout=10)
        print(f"✅ API endpoint: {r.status_code}")
    except Exception as e:
        print(f"❌ API endpoint failed: {e}")
    
    # Test 3: Streaming endpoint
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        r = requests.post(
            'https://yupp.ai/chat/test?stream=true',
            headers=headers,
            data='test',
            timeout=30,
            stream=True
        )
        print(f"✅ Streaming endpoint: {r.status_code}")
        
        # Try to read first line
        for line in r.iter_lines():
            if line:
                print(f"📡 Stream data: {line.decode()[:100]}...")
                break
                
    except Exception as e:
        print(f"❌ Streaming endpoint failed: {e}")
    
    return True

if __name__ == "__main__":
    test_yupp_connection()
```

## 🌐 VPS Provider Specific

### DigitalOcean
```bash
# Check firewall
sudo ufw status
sudo ufw allow out 443
sudo ufw allow out 80

# Check network
ip route show
```

### AWS EC2
```bash
# Check security groups
# Allow outbound HTTPS (443) and HTTP (80)

# Check VPC settings
aws ec2 describe-security-groups
```

### Google Cloud
```bash
# Check firewall rules
gcloud compute firewall-rules list

# Allow outbound
gcloud compute firewall-rules create allow-outbound \
    --direction=EGRESS \
    --priority=1000 \
    --network=default \
    --action=ALLOW \
    --rules=tcp:443,tcp:80
```

### Vultr
```bash
# Check firewall
ufw status
ufw allow out 443
ufw allow out 80
```

## 📊 Monitoring

### Log Analysis
```bash
# Monitor network
watch -n 1 'netstat -an | grep :443'

# Monitor connections
watch -n 1 'ss -tuln | grep :443'

# Monitor bandwidth
iftop -i eth0
```

### Performance Test
```bash
# Test download speed
wget -O /dev/null https://yupp.ai

# Test latency
ping -c 10 yupp.ai

# Test DNS
nslookup yupp.ai
```

## 🚨 Emergency Fixes

### Quick Fix 1: Restart Network
```bash
sudo systemctl restart networking
sudo systemctl restart systemd-resolved
```

### Quick Fix 2: Change DNS
```bash
echo "nameserver 1.1.1.1" | sudo tee /etc/resolv.conf
echo "nameserver 1.0.0.1" | sudo tee -a /etc/resolv.conf
```

### Quick Fix 3: Disable IPv6
```bash
echo 'net.ipv6.conf.all.disable_ipv6 = 1' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv6.conf.default.disable_ipv6 = 1' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## 📝 Checklist

- [ ] Test basic connectivity
- [ ] Check DNS resolution
- [ ] Verify firewall settings
- [ ] Test with/without proxy
- [ ] Update Python packages
- [ ] Check system resources
- [ ] Monitor network logs
- [ ] Test different VPS regions

## 🆘 Still Not Working?

1. **Try different VPS provider**
2. **Use different VPS location**
3. **Contact VPS support**
4. **Use VPN on VPS**
5. **Try different Python version**

---

**Note**: Most VPS streaming issues are related to network configuration, firewall rules, or DNS resolution. Start with basic connectivity tests and work your way up to more complex solutions. 
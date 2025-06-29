# VPS Troubleshooting Guide

## Masalah: "Tidak ada Reward ID yang ditemukan dalam streaming response"

### Penyebab Umum
1. **Perbedaan environment** antara local dan VPS
2. **Network connectivity issues** pada VPS
3. **Proxy configuration problems**
4. **Missing dependencies**
5. **Response format differences**

## 🔥 **MASALAH KHUSUS: Error 429 (Rate Limiting)**

### Gejala:
```
❌ Still rate limited (429)
❌ Streaming request failed with status: 429
```

### Penyebab:
- **Server yupp.ai** mendeteksi terlalu banyak request
- **Vercel protection** aktif dan memblokir IP/proxy
- **Proxy IP** sudah di-blacklist oleh server
- **VPS IP** sudah di-rate limit

### Solusi Cepat:

#### 1. Test Semua Proxy untuk Rate Limiting
```bash
python3 bypass_rate_limit.py
```

#### 2. Test Tanpa Proxy
```bash
python3 test_without_proxy.py
```

#### 3. Gunakan Proxy Rotation
```bash
python3 manage_proxies.py
```

#### 4. Test dengan Delay yang Lebih Baik
```bash
python3 test_with_delay.py
```

### Strategi Bypass Rate Limiting:

#### A. Proxy Rotation
1. **Test semua proxy** untuk menemukan yang tidak rate limited
2. **Gunakan proxy yang berbeda** untuk setiap account
3. **Rotate proxy** setiap beberapa request

#### B. Delay Strategy
1. **Random delays** antara request (2-8 detik)
2. **Longer delays** antara account (15-30 detik)
3. **Exponential backoff** untuk retry

#### C. IP Rotation
1. **Gunakan residential proxy** (lebih sulit di-detect)
2. **Contact proxy provider** untuk IP rotation
3. **Gunakan VPN** sebagai alternatif

### Troubleshooting 429 Error:

#### Step 1: Identify the Source
```bash
# Test tanpa proxy
python3 test_without_proxy.py

# Test dengan proxy
python3 bypass_rate_limit.py
```

#### Step 2: Find Working Proxy
```bash
# Test semua proxy
python3 manage_proxies.py

# Pilih proxy terbaik
# Update proxy.txt dengan proxy yang berfungsi
```

#### Step 3: Use Better Delays
```bash
# Test dengan delay yang lebih baik
python3 test_with_delay.py

# Atau jalankan bot dengan sequential mode
python3 main.py
# Pilih: Sequential mode, 1 account, delay yang lebih lama
```

#### Step 4: Alternative Solutions
1. **Tunggu 30-60 menit** sebelum test lagi
2. **Gunakan proxy service yang berbeda**
3. **Test dengan account yang berbeda**
4. **Kurangi jumlah concurrent requests**

### Advanced Bypass Techniques:

#### 1. User-Agent Rotation
```python
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36...',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36...'
]
```

#### 2. Request Pattern Variation
- **Random delays** antara request
- **Different request sequences**
- **Vary request headers**

#### 3. Session Management
- **Fresh session** untuk setiap account
- **Clear cookies** antara request
- **Different device profiles**

### Monitoring Rate Limiting:

#### Check Rate Limit Status:
```bash
# Test basic connection
curl -I https://yupp.ai

# Test dengan proxy
curl --proxy socks5://user:pass@host:port -I https://yupp.ai
```

#### Monitor Response Headers:
- **X-RateLimit-Remaining**: Requests remaining
- **X-RateLimit-Reset**: Time until reset
- **Retry-After**: Wait time for retry

### Emergency Solutions:

#### Jika Semua Proxy Rate Limited:
1. **Tunggu 1-2 jam** sebelum test lagi
2. **Contact proxy provider** untuk IP rotation
3. **Gunakan residential proxy** service
4. **Test dari lokasi yang berbeda**

#### Jika VPS IP Rate Limited:
1. **Restart VPS** untuk mendapatkan IP baru
2. **Contact VPS provider** untuk IP change
3. **Use VPN** pada VPS
4. **Migrate ke VPS provider lain**

---

## 🔥 **MASALAH KHUSUS: Error 407 NO_USER**

### Gejala:
```
❌ Basic connection failed: HTTPSConnectionPool(host='yupp.ai', port=443): 
Max retries exceeded with url: / (Caused by ProxyError('Unable to connect to proxy', 
OSError('Tunnel connection failed: 407 NO_USER')))
```

### Penyebab:
- **Proxy authentication error**: Username atau password salah/format tidak benar
- **Format proxy tidak sesuai**: Protocol tidak ditentukan atau format salah

### Solusi Cepat:

#### 1. Check Proxy Format
```bash
python3 fix_proxy.py
```

#### 2. Test Proxy Connection
```bash
python3 test_proxy.py
```

#### 3. Create New Proxy Config
```bash
python3 fix_proxy.py --create
```

#### 4. Show Common Fixes
```bash
python3 fix_proxy.py --fix
```

### Format Proxy yang Benar:
```
# SOCKS5 dengan authentication
socks5://username:password@host:port

# HTTP dengan authentication  
http://username:password@host:port

# HTTPS dengan authentication
https://username:password@host:port

# Tanpa authentication
socks5://host:port
http://host:port
```

### Troubleshooting 407 Error:
1. **Check username:password** - pastikan tidak ada spasi atau karakter khusus
2. **Verify protocol** - pastikan socks5://, http://, atau https:// ditentukan
3. **Test dengan curl**:
   ```bash
   curl --proxy socks5://username:password@host:port https://httpbin.org/ip
   ```
4. **Check proxy service** - pastikan proxy server aktif dan credentials valid

---

### Solusi Step-by-Step

#### 1. Setup Environment VPS
```bash
# Install dependencies
python3 setup_vps.py

# Atau manual
pip3 install requests[socks] PySocks rich google-generativeai
```

#### 2. Test Network Connectivity
```bash
# Test basic connectivity
python3 test_streaming_debug.py
```

#### 3. Check Proxy Configuration
- Pastikan format proxy benar di `proxy.txt`
- Test proxy dengan script debug
- Coba tanpa proxy terlebih dahulu

#### 4. Debug Streaming Response
Bot sekarang memiliki fitur debug yang lebih baik:
- Menampilkan raw response lines
- Mencoba multiple parsing patterns
- Fallback regex extraction
- Retry mechanism

#### 5. Common VPS Issues

##### Issue: SOCKS Proxy Not Working
```bash
# Install SOCKS support
pip3 install requests[socks] PySocks

# Test SOCKS support
python3 install_dependencies.py
```

##### Issue: Network Timeout
- Bot sekarang memiliki timeout 60 detik
- Retry mechanism (3 attempts)
- Better error handling

##### Issue: Different Response Format
- Bot sekarang mendukung multiple response formats:
  - `a:` prefix format
  - Direct JSON format
  - Array format
  - Regex fallback

#### 6. Environment Differences

##### Local vs VPS Differences:
1. **Python Version**: Pastikan versi Python sama
2. **Dependencies**: Install semua dependencies yang diperlukan
3. **Network**: VPS mungkin memiliki firewall/restrictions
4. **Proxy**: Proxy behavior mungkin berbeda di VPS

#### 7. Advanced Debugging

##### Enable Verbose Logging
Bot sekarang menampilkan:
- Raw response lines (first 5)
- Total lines received
- Found keywords
- Response format detection

##### Manual Testing
```bash
# Test dengan curl
curl -X POST "https://yupp.ai/chat/test?stream=true" \
  -H "Content-Type: text/plain;charset=UTF-8" \
  -H "User-Agent: Mozilla/5.0..." \
  --data '["test", "test", "hello", "$undefined", "$undefined", [], "$undefined", [], "none", false]'
```

#### 8. Temporary Workarounds

##### Jika streaming tetap gagal:
1. **Coba tanpa proxy** terlebih dahulu
2. **Gunakan HTTP proxy** instead of SOCKS
3. **Test dengan account berbeda**
4. **Check VPS provider restrictions**

#### 9. Monitoring dan Logs

##### Check VPS Logs:
```bash
# Check system logs
tail -f /var/log/syslog

# Check network connectivity
ping yupp.ai
nslookup yupp.ai

# Check proxy connectivity
curl --proxy your-proxy:port https://httpbin.org/ip
```

#### 10. Performance Optimization

##### Untuk VPS dengan resources terbatas:
1. **Kurangi concurrent threads** (default: 5)
2. **Increase timeout** jika diperlukan
3. **Monitor memory usage**
4. **Use lighter device profiles**

### File Files Penting

1. **`setup_vps.py`** - Setup script untuk VPS
2. **`test_streaming_debug.py`** - Debug streaming connection
3. **`install_dependencies.py`** - Install SOCKS dependencies
4. **`main.py`** - Bot utama dengan improvements

### Contact Support

Jika masalah masih berlanjut:
1. Jalankan `python3 test_streaming_debug.py`
2. Capture output lengkap
3. Check VPS provider documentation
4. Verify proxy service status 
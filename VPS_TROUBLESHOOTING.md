# VPS Troubleshooting Guide

## Masalah: "Tidak ada Reward ID yang ditemukan dalam streaming response"

### Penyebab Umum
1. **Perbedaan environment** antara local dan VPS
2. **Network connectivity issues** pada VPS
3. **Proxy configuration problems**
4. **Missing dependencies**
5. **Response format differences**

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
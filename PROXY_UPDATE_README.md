# 🔄 Update Proxy Support - Multiple Protocol

## 📋 Perubahan yang Dibuat

### ✅ Dukungan Multiple Protocol Proxy
Sekarang bot mendukung berbagai protokol proxy:
- **HTTP**: `http://username:password@host:port`
- **HTTPS**: `https://username:password@host:port`
- **SOCKS4**: `socks4://username:password@host:port`
- **SOCKS5**: `socks5://username:password@host:port`

### 🔧 Dependency Baru
Untuk mendukung SOCKS proxy, diperlukan dependency tambahan:
```bash
pip install requests[socks] PySocks
```

Atau jalankan script installer:
```bash
python3 install_dependencies.py
```

### 🛠️ Perbaikan Error Handling
- Validasi proxy sebelum digunakan
- Error handling yang lebih baik untuk SOCKS proxy
- Fallback ke mode tanpa proxy jika dependency tidak tersedia

## 📁 File yang Diupdate

### 1. `requirements.txt`
```txt
google-generativeai
requests
requests[socks]  # ← Baru
PySocks          # ← Baru
rich
deepseek
```

### 2. `main.py`
- ✅ Fungsi `validate_proxy_config()` - Validasi proxy dan dependency
- ✅ Update `load_proxy_config()` - Support multiple protocol
- ✅ Update `get_manual_proxy()` - Support multiple protocol
- ✅ Update `load_multiple_cookies_from_file()` - Validasi proxy per account
- ✅ Error handling yang lebih baik di `run_single_bot_process()`

### 3. `cookies.txt`
Proxy sudah diubah dari HTTP ke SOCKS5:
```txt
# Sebelum
PROXY:http://username:password@host:port

# Sesudah
PROXY:socks5://username:password@host:port
```

## 🚀 Cara Penggunaan

### 1. Install Dependency
```bash
python3 install_dependencies.py
```

### 2. Test SOCKS Support
```bash
python3 -c "import socks; import socket; print('✅ SOCKS support OK')"
```

### 3. Jalankan Bot
```bash
python3 main.py
```

## 🔍 Format Proxy yang Didukung

### HTTP/HTTPS
```txt
PROXY:http://username:password@host:port
PROXY:https://username:password@host:port
PROXY:http://host:port
PROXY:https://host:port
```

### SOCKS
```txt
PROXY:socks5://username:password@host:port
PROXY:socks5://host:port
PROXY:socks4://username:password@host:port
PROXY:socks4://host:port
```

## ⚠️ Troubleshooting

### Error: "Missing dependencies for SOCKS support"
**Solusi:**
```bash
pip install requests[socks] PySocks
```

### Error: "SOCKS proxy memerlukan dependency tambahan"
**Solusi:**
```bash
python3 install_dependencies.py
```

### Proxy tidak berfungsi
**Solusi:**
1. Cek format proxy di `cookies.txt`
2. Pastikan proxy server aktif
3. Cek username/password proxy
4. Coba tanpa proxy dulu untuk test

## 📊 Keuntungan Update

1. **Multiple Protocol**: Support HTTP, HTTPS, SOCKS4, SOCKS5
2. **Better Security**: SOCKS5 lebih aman dari HTTP proxy
3. **Better Performance**: SOCKS5 lebih cepat untuk beberapa kasus
4. **Error Handling**: Validasi dan error handling yang lebih baik
5. **Fallback**: Otomatis fallback ke mode tanpa proxy jika ada masalah

## 🔄 Rollback (Jika Perlu)

Jika ingin kembali ke HTTP proxy:
1. Edit `cookies.txt` - ganti `socks5://` menjadi `http://`
2. Atau jalankan script converter:
```bash
python3 convert_proxy_to_http.py
```

---

**🎉 Update selesai! Bot sekarang mendukung multiple protocol proxy dengan error handling yang lebih baik.** 
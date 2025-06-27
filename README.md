# 🤖 Yupp.ai Auto-Bot v4.3

**Advanced automation bot for Yupp.ai with multi-account support, proxy rotation, device spoofing, and AI-powered message generation.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [Security Notes](#security-notes)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

Yupp.ai Auto-Bot is a sophisticated automation tool designed to interact with the Yupp.ai platform. It supports multiple accounts, proxy rotation, device fingerprinting, and can generate messages using either predefined text or AI-powered content generation via Google's Gemini API.

### What it does:
- ✅ Automatically sends messages to Yupp.ai chat
- ✅ Claims rewards automatically when available
- ✅ Supports multiple accounts simultaneously
- ✅ Rotates between different device profiles
- ✅ Supports various proxy configurations
- ✅ Generates messages using AI or predefined text
- ✅ Provides detailed logging and progress tracking

## ✨ Features

### 🔐 Multi-Account Support
- **Single Account Mode**: Use one account with `cookie.txt`
- **Multiple Accounts Mode**: Manage multiple accounts with `cookies.txt`
- Individual proxy and user ID configuration per account
- Automatic account rotation during execution

### 🌐 Proxy Support
- **No Proxy**: Direct connection
- **Global Proxy**: Single proxy for all accounts
- **Individual Proxy**: Different proxy per account
- **Manual Proxy**: Enter proxy manually
- Supports HTTP, HTTPS, and SOCKS5 protocols
- Authentication support (username:password@host:port)

### 📱 Device Spoofing
- **8 Device Profiles**: Windows Chrome, macOS Chrome, Android Chrome, Windows Firefox, macOS Safari, iOS Safari, Linux Firefox, Windows Edge
- **Per-Account Assignment**: Assign specific device profiles to each account
- **Random Fallback**: Uses random device profile if none specified
- **Realistic Fingerprinting**: Mimics different browsers and operating systems
- **Reduces Detection Risk**: Each account maintains consistent device identity

### 🤖 AI Integration
- **Gemini AI**: Generate dynamic messages using Google's Gemini API
- **Predefined Messages**: Use static messages from `pesan.txt`
- Automatic message rotation and randomization

### 📊 Advanced Monitoring
- Rich console interface with progress bars
- Detailed error reporting and logging
- JSON response formatting
- Real-time status updates

## 📋 Prerequisites

Before using this bot, ensure you have:

- **Python 3.8 or higher**
- **Active Yupp.ai account(s)**
- **Valid session cookies** from your Yupp.ai account
- **Google Gemini API key** (optional, for AI message generation)
- **Proxy servers** (optional, for IP rotation)

## 🚀 Installation

### 1. Clone or Download
```bash
# If using git
git clone <repository-url>
cd yuppai-bot

# Or download and extract the ZIP file
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Installation
```bash
python main.py --help
```

## ⚙️ Configuration

### Required Files Setup

#### 1. Session Cookies (`cookie.txt` or `cookies.txt`)

**For Single Account (`cookie.txt`):**
```txt
__Secure-yupp.session-token=your_session_token_here
AMP_MKTG_78c6b96db9=your_amp_mktg_value_here
AMP_78c6b96db9=your_amp_value_here
```

**For Multiple Accounts (`cookies.txt`):**
```txt
# ACCOUNT 1 - Windows Chrome
PROXY:http://proxy1.example.com:8080
USER_ID:37cf0952-9403-4d29-bf7a-1d1c08368a4a
DEVICE_PROFILE:Windows Chrome
__Secure-yupp.session-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
AMP_MKTG_78c6b96db9=JTdCJTdE
AMP_78c6b96db9=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI5NWM3YmMyNy0wYjA3LTQ4NzAtYWFmZi1lZDhiM2U1NGYxOTclMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIzN2NmMDk1Mi05NDAzLTRkMjktYmY3YS0xZDFjMDgzNjhhNGElMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzUwOTg5MzQ5MzU3JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTc1MDk4OTM5MzQ1MSUyQyUyMmxhc3RFdmVudElkJTIyJTNBMjA1JTJDJTIycGFnZUNvdW50ZXIlMjIlM0EyJTdE

---
# ACCOUNT 2 - macOS Safari
PROXY:socks5://proxy2.example.com:1080
USER_ID:039a1999-b8a6-42b7-8d86-85322912fb28
DEVICE_PROFILE:macOS Safari
__Secure-yupp.session-token=your_second_account_token_here
AMP_MKTG_78c6b96db9=your_second_amp_mktg_here
AMP_78c6b96db9=your_second_amp_here
```

**Available Device Profiles:**
1. **Windows Chrome** - Windows 10/11 with Chrome browser
2. **macOS Chrome** - macOS with Chrome browser  
3. **Android Chrome** - Android mobile with Chrome browser
4. **Windows Firefox** - Windows with Firefox browser
5. **macOS Safari** - macOS with Safari browser
6. **iOS Safari** - iPhone/iPad with Safari browser
7. **Linux Firefox** - Linux with Firefox browser
8. **Windows Edge** - Windows with Microsoft Edge browser

#### 2. Proxy Configuration (`proxy.txt`)
```txt
# Single proxy for all accounts
http://username:password@host:port
# or
socks5://host:port
# or
host:port
```

#### 3. AI API Key (`apikey.txt`)
```txt
your_google_gemini_api_key_here
```

#### 4. Predefined Messages (`pesan.txt`)
```txt
What is cryptocurrency, and how does it differ from traditional fiat currencies?
How does blockchain technology work, and why is it considered secure?
What are the main differences between proof-of-work and proof-of-stake?
```

### How to Get Session Cookies

1. **Login to Yupp.ai** in your browser
2. **Open Developer Tools** (F12)
3. **Go to Application/Storage tab**
4. **Find Cookies** for `yupp.ai`
5. **Copy the required cookies**:
   - `__Secure-yupp.session-token`
   - `AMP_MKTG_78c6b96db9`
   - `AMP_78c6b96db9`

### How to Get Gemini API Key

1. **Visit** [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Create a new API key**
3. **Copy the key** to `apikey.txt`

## 🎮 Usage

### Basic Usage
```bash
python main.py
```

### Interactive Setup Process

When you run the bot, it will guide you through an interactive setup:

1. **Proxy Configuration**
   - Choose proxy mode (None, Global, Individual, Manual)
   - Configure proxy settings if needed

2. **Cookie Configuration**
   - Choose between single or multiple accounts
   - Verify cookie files are properly configured

3. **Message Source**
   - Use predefined messages from `pesan.txt`
   - Use AI-generated messages with Gemini

4. **Loop Configuration**
   - Set number of execution loops
   - Configure delays between operations

### Example Session
```
🚀 Yupp.ai Auto-Bot v4.3 (Device Spoofing + Multi-Proxy + Multi-Account) 🚀
by Gemini

┌─ PILIH MODE PROXY ─┐
│                     │
│ 1. Tidak menggunakan proxy
│ 2. Gunakan 1 proxy untuk semua account
│ 3. Gunakan proxy individual per account (dari cookies.txt)
│ 4. Masukkan proxy manual untuk semua account
│                     │
└─────────────────────┘

Masukkan pilihan Anda [1]: 1

┌─ PILIH KONFIGURASI COOKIE ─┐
│                             │
│ 1. Gunakan single cookie (cookie.txt)
│ 2. Gunakan multiple cookies (cookies.txt)
│                             │
└─────────────────────────────┘

Masukkan pilihan Anda [1]: 2

✅ Berhasil memuat 3 account dari cookies.txt

┌─ PILIH SUMBER PESAN ─┐
│                       │
│ 1. Gunakan pesan dari pesan.txt
│ 2. Gunakan Gemini AI untuk generate pesan
│                       │
└───────────────────────┘

Masukkan pilihan Anda [1]: 1

✅ Pilihan: Menggunakan `pesan.txt`. Ditemukan 25 pesan untuk diacak.

Masukkan jumlah looping yang diinginkan [1]: 3

--- Pengaturan Selesai. Memulai Looping. ---

┌─ LOOP KE-1 DARI 3 ─┐
🖥️  Menggunakan profil device: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...

┌─ ACCOUNT #1 DARI 3 ─┐
1.   🔐 Menginisialisasi session...
2.   💬 Membuat chat baru...
3.   📤 Mengirim pesan...
4.   ✍️  Mengirim Log Event Umpan Balik...
5.   🎁 Mengklaim Hadiah dengan ID: reward_123...
   ✅ PROSES KLAIM BERHASIL!
```

## 📁 File Structure

```
yuppai-bot/
├── main.py                 # Main bot script
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── cookie.txt             # Single account cookies
├── cookies.txt            # Multiple accounts cookies
├── cookies_example.txt    # Example cookies format
├── proxy.txt              # Global proxy configuration
├── proxy_example.txt      # Example proxy format
├── apikey.txt             # Google Gemini API key
├── pesan.txt              # Predefined messages
├── venv/                  # Virtual environment
└── .gitignore            # Git ignore file
```

## 🔧 Advanced Features

### Device Profile Rotation
The bot automatically rotates between different device profiles to mimic real user behavior:

- **Windows 10/11** with Chrome/Firefox/Edge
- **macOS** with Safari/Chrome
- **Linux** with Firefox/Chrome
- **Mobile** devices (iOS/Android)

### Proxy Rotation Strategies
- **Round-robin**: Rotate through proxy list
- **Individual**: Different proxy per account
- **Failover**: Switch proxy on connection failure
- **Geographic**: Route through different countries

### Error Handling
- **Connection retry**: Automatic retry on network errors
- **Proxy failover**: Switch proxy if current one fails
- **Session refresh**: Handle expired sessions
- **Rate limiting**: Respect API rate limits

### Logging and Monitoring
- **Real-time progress**: Live progress bars and status updates
- **Error tracking**: Detailed error messages and stack traces
- **Response analysis**: JSON formatting for API responses
- **Performance metrics**: Execution time and success rates

## 🛠️ Troubleshooting

### Common Issues

#### 1. "File not found" Errors
```bash
# Ensure all required files exist
ls -la *.txt
```

#### 2. "Invalid cookie format" Errors
```bash
# Check cookie format in cookie.txt or cookies.txt
# Ensure no extra spaces or invalid characters
```

#### 3. "Proxy connection failed" Errors
```bash
# Test proxy manually
curl -x your_proxy:port https://httpbin.org/ip
```

#### 4. "API key invalid" Errors
```bash
# Verify Gemini API key is correct and active
# Check API quota and billing status
```

#### 5. "Session expired" Errors
```bash
# Refresh cookies from browser
# Ensure cookies are recent and valid
```

### Debug Mode
To enable detailed logging, modify the script to include debug output:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Optimization
- **Reduce loop count** for testing
- **Use fewer accounts** initially
- **Increase delays** between operations
- **Monitor system resources**

## 🔒 Security Notes

### Important Security Considerations

1. **Cookie Security**
   - Never share your session cookies
   - Store cookies securely
   - Rotate cookies regularly
   - Use different cookies for different accounts

2. **Proxy Security**
   - Use trusted proxy providers
   - Verify proxy anonymity
   - Monitor proxy logs
   - Rotate proxies regularly

3. **API Key Security**
   - Keep API keys private
   - Monitor API usage
   - Set usage limits
   - Rotate keys periodically

4. **Account Security**
   - Use strong passwords
   - Enable 2FA if available
   - Monitor account activity
   - Report suspicious activity

### Best Practices

- ✅ **Test with single account first**
- ✅ **Use small loop counts initially**
- ✅ **Monitor for rate limiting**
- ✅ **Keep software updated**
- ✅ **Backup configuration files**
- ✅ **Use virtual environments**

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests if applicable**
5. **Submit a pull request**

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd yuppai-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and personal use only. Users are responsible for:

- **Compliance with Yupp.ai Terms of Service**
- **Respect for rate limits and fair use policies**
- **Proper handling of personal data**
- **Legal compliance in their jurisdiction**

The developers are not responsible for any misuse or violations of terms of service.

## 📞 Support

For support and questions:

- **Create an issue** on GitHub
- **Check the troubleshooting section**
- **Review the configuration examples**
- **Test with minimal setup first**

---

**Made with ❤️ for the Yupp.ai community**

*Last updated: December 2024* 
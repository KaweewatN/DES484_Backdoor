"""
Utility functions for the backdoor project
"""

import os
import sys
import platform


def check_environment():
    """Check if the environment is suitable for running the backdoor"""
    info = {
        'python_version': sys.version,
        'platform': platform.platform(),
        'system': platform.system(),
        'machine': platform.machine(),
        'processor': platform.processor(),
    }
    return info


def check_dependencies():
    """Check which optional dependencies are available"""
    dependencies = {
        'pynput': False,
        'PIL': False,
        'pyautogui': False,
        'pyaudio': False,
        'cv2': False,
    }
    
    # Try importing each dependency
    try:
        import pynput
        dependencies['pynput'] = True
    except ImportError:
        pass
    
    try:
        from PIL import Image
        dependencies['PIL'] = True
    except ImportError:
        pass
    
    try:
        import pyautogui
        dependencies['pyautogui'] = True
    except ImportError:
        pass
    
    try:
        import pyaudio
        dependencies['pyaudio'] = True
    except ImportError:
        pass
    
    try:
        import cv2
        dependencies['cv2'] = True
    except ImportError:
        pass
    
    return dependencies


def print_status():
    """Print environment and dependency status"""
    print("=== Environment Status ===")
    env = check_environment()
    for key, value in env.items():
        print(f"{key}: {value}")
    
    print("\n=== Dependency Status ===")
    deps = check_dependencies()
    for dep, available in deps.items():
        status = "✓ Available" if available else "✗ Not installed"
        print(f"{dep}: {status}")
    
    print("\n=== Feature Availability ===")
    print(f"Keylogger: {'Full' if deps['pynput'] else 'Fallback mode'}")
    print(f"Screenshots: {'Full' if deps['PIL'] or deps['pyautogui'] else 'System commands'}")
    print(f"Audio Recording: {'Full' if deps['pyaudio'] else 'System commands'}")
    print(f"Webcam Capture: {'Full' if deps['cv2'] else 'Not available'}")
    print(f"Network Discovery: Always available")
    print(f"Privilege Escalation: Always available")
    print(f"Persistence: Always available")


if __name__ == "__main__":
    print_status()

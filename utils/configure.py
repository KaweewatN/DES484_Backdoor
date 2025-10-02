#!/usr/bin/env python3
"""
Configuration helper for the backdoor
Updates server.py with attacker IP and port
"""

import sys
import os


def get_attacker_config():
    """Get attacker configuration from user"""
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║           Backdoor Configuration Helper                      ║")
    print("╚═══════════════════════════════════════════════════════════════╝\n")
    
    # Get IP address
    while True:
        ip = input("Enter attacker IP address [192.168.1.12]: ").strip()
        if not ip:
            ip = "192.168.1.12"
        
        # Basic IP validation
        parts = ip.split('.')
        if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
            break
        else:
            print("Invalid IP address format. Please try again.")
    
    # Get port
    while True:
        port = input("Enter attacker port [5555]: ").strip()
        if not port:
            port = "5555"
        
        if port.isdigit() and 1 <= int(port) <= 65535:
            break
        else:
            print("Invalid port number. Must be between 1 and 65535.")
    
    return ip, port


def update_server_config(ip, port):
    """Update server.py with new configuration"""
    server_file = 'server.py'
    
    if not os.path.exists(server_file):
        print(f"Error: {server_file} not found!")
        return False
    
    # Read the file
    with open(server_file, 'r') as f:
        content = f.read()
    
    # Replace the configuration
    # Look for the configuration section
    old_config = "ATTACKER_HOST = '192.168.1.12'"
    new_config = f"ATTACKER_HOST = '{ip}'"
    content = content.replace(old_config, new_config)
    
    old_port = "ATTACKER_PORT = 5555"
    new_port = f"ATTACKER_PORT = {port}"
    content = content.replace(old_port, new_port)
    
    # Write back
    with open(server_file, 'w') as f:
        f.write(content)
    
    return True


def main():
    """Main function"""
    print("\nThis script will configure server.py with your attacker machine details.\n")
    
    ip, port = get_attacker_config()
    
    print(f"\nConfiguration:")
    print(f"  Attacker IP: {ip}")
    print(f"  Attacker Port: {port}")
    
    confirm = input("\nUpdate server.py with these settings? [Y/n]: ").strip().lower()
    
    if confirm in ['', 'y', 'yes']:
        if update_server_config(ip, port):
            print("\n✓ server.py updated successfully!")
            print(f"\nNext steps:")
            print(f"1. On attacker machine: python3 backend.py")
            print(f"2. On target machine: python3 server.py")
        else:
            print("\n✗ Failed to update server.py")
            sys.exit(1)
    else:
        print("\nConfiguration cancelled.")


if __name__ == "__main__":
    main()

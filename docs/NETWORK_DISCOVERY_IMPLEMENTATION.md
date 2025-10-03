# Network Discovery Implementation Guide

## Overview

Network reconnaissance capabilities to map network topology, discover hosts, scan ports, and gather network intelligence.

## Implementation Details

### Architecture

- **Module**: `features/network_discovery.py`
- **Class**: `NetworkDiscovery`
- **Methods**: Platform-specific commands (ifconfig, ip, netstat, nmap, arp)
- **Fallbacks**: Multiple methods for cross-platform compatibility

## Commands Reference

### Network Information

```bash
net_info
```

**What happens:**

- Enumerates network interfaces
- Displays IP addresses
- Shows subnet masks
- Lists MAC addresses
- Identifies active interfaces

**Response:**

```
=== Network Information ===
Interface: eth0
  IP Address: 192.168.1.50
  Netmask: 255.255.255.0
  MAC: 00:11:22:33:44:55
  Status: UP

Interface: wlan0
  IP Address: 192.168.1.51
  Netmask: 255.255.255.0
  MAC: AA:BB:CC:DD:EE:FF
  Status: UP

Default Gateway: 192.168.1.1
DNS Servers: 192.168.1.1, 8.8.8.8
```

**Use case:**

- Understand network configuration
- Identify target's IP address
- Find network ranges for scanning
- Detect VPN connections

**Implementation:**

- Linux/macOS: `ifconfig` or `ip addr`
- Windows: `ipconfig /all`
- Parses output for IP, MAC, interface info

---

### Network Scan (Ping Sweep)

```bash
net_scan
```

**What happens:**

- Determines local subnet (e.g., 192.168.1.0/24)
- Sends ping to all IPs in range
- Identifies live hosts
- May use ARP scan on Linux
- Returns list of responsive hosts

**Response:**

```
[+] Scanning network 192.168.1.0/24...
[+] Live hosts discovered:
  192.168.1.1   (Gateway)
  192.168.1.10
  192.168.1.12  (Attacker)
  192.168.1.50  (This machine)
  192.168.1.100
  192.168.1.105

Total: 6 hosts found
```

**Use case:**

- Map network topology
- Discover other machines
- Find potential pivot points
- Identify network size

**Implementation:**

- Ping sweep: `ping -c 1` each IP
- ARP scan: `arp-scan` (Linux with tool)
- Or `arp -a` to read ARP cache
- Timeout: 1-2 seconds per host

**Performance:**

- /24 network: ~30-60 seconds
- Parallel scanning for speed
- May be noisy (generates traffic)

---

### Active Connections

```bash
net_connections
```

**What happens:**

- Lists all active TCP/UDP connections
- Shows local and remote addresses
- Displays connection states
- Identifies listening ports
- Shows process IDs (if permissions allow)

**Response:**

```
=== Active Network Connections ===

TCP Connections:
Proto  Local Address          Foreign Address         State       PID/Program
tcp    192.168.1.50:5555     192.168.1.12:45678      ESTABLISHED  1234/python3
tcp    192.168.1.50:22       0.0.0.0:*               LISTEN       567/sshd
tcp    127.0.0.1:3306        0.0.0.0:*               LISTEN       890/mysqld

UDP Connections:
Proto  Local Address          Foreign Address         State
udp    0.0.0.0:68            0.0.0.0:*
udp    192.168.1.50:123      0.0.0.0:*

Listening Ports: 22, 80, 443, 3306, 5555
```

**Use case:**

- Identify running services
- Detect backdoor connections
- Find database connections
- Discover listening services

**Implementation:**

- Linux/macOS: `netstat -an` or `ss -tulpn`
- Windows: `netstat -ano`
- Parses output for connections

---

### Port Scan

```bash
net_portscan <host>
```

**Parameter:**

- `host`: Target IP address or hostname

**Example:**

```bash
net_portscan 192.168.1.1
```

**What happens:**

- Scans common ports on target
- Tests: 21, 22, 23, 25, 80, 443, 3306, 3389, 5900, 8080, etc.
- Attempts TCP connection to each port
- Reports open ports

**Response:**

```
[+] Scanning ports on 192.168.1.1...
[+] Open ports:
  22   (SSH)
  80   (HTTP)
  443  (HTTPS)
  8080 (HTTP-ALT)

Closed ports: 21, 23, 25, 3306, 3389, 5900
```

**Use case:**

- Identify services on router/gateway
- Find vulnerable services
- Discover network infrastructure
- Plan lateral movement

**Implementation:**

- TCP connect scan
- Socket connection attempt
- Timeout: 2-3 seconds per port
- Common ports list (20-30 ports)

**Performance:**

- ~30 seconds for full common port scan
- Sequential scanning (not parallel)
- May trigger IDS/firewall alerts

---

### Public IP Address

```bash
net_public_ip
```

**What happens:**

- Queries external service (ifconfig.me, ipify.org, etc.)
- Returns public-facing IP address
- Indicates if behind NAT

**Response:**

```
[+] Public IP Address: 203.0.113.45
[+] Organization: Example ISP
[+] Location: City, Country
```

**Use case:**

- Determine if target is behind NAT
- Identify ISP/location
- Verify VPN usage
- Geolocation information

**Implementation:**

- HTTP request to: `http://ifconfig.me/ip`
- Alternative: `https://api.ipify.org`
- Fallback: `http://checkip.amazonaws.com`
- Parses response for IP

**Note:** Requires internet connection

---

### Internet Connectivity Check

```bash
net_check_internet
```

**What happens:**

- Attempts to reach common internet hosts
- Tests: 8.8.8.8 (Google DNS), 1.1.1.1 (Cloudflare)
- Reports connectivity status

**Response:**

```
[+] Internet connectivity: ONLINE
[+] DNS resolution: Working
[+] Ping to 8.8.8.8: 15ms
[+] Ping to 1.1.1.1: 12ms
```

Or:

```
[!] Internet connectivity: OFFLINE
[!] No route to internet
```

**Use case:**

- Verify network access
- Test for air-gapped systems
- Check firewall restrictions
- Validate exfiltration path

**Implementation:**

- Ping 8.8.8.8 and 1.1.1.1
- DNS lookup test
- HTTP connection test
- Multiple methods for reliability

## Troubleshooting

### Issue 1: net_scan finds no hosts

**Causes:**

- Firewall blocking ping
- ARP scan not available
- Subnet calculation wrong

**Solutions:**

```bash
# Check current IP first
net_info

# Manually verify network
ping 192.168.1.1  # Test gateway

# Check firewall
# Linux:
sudo iptables -L

# macOS:
sudo pfctl -s all

# Windows:
netsh advfirewall show allprofiles
```

---

### Issue 2: net_portscan shows all ports closed

**Causes:**

- Host firewall blocking
- Host is down
- Network firewall filtering

**Solutions:**

```bash
# Verify host is up first
ping <target_ip>

# Try manual connection
telnet <target_ip> 80

# Check your firewall isn't blocking outbound
```

---

### Issue 3: "Permission denied" errors

**Cause:** Some network commands require elevated privileges

**Solution:**

```bash
# Run backdoor with appropriate permissions
sudo python3 backdoor.py

# Or use privilege escalation features
priv_check
priv_enum
```

---

### Issue 4: net_public_ip fails

**Causes:**

- No internet connection
- Firewall blocking HTTP
- External service down

**Solutions:**

```bash
# Check internet first
net_check_internet

# Manually test
curl http://ifconfig.me/ip

# Check for proxy/firewall
echo $http_proxy
```

---

### Issue 5: Slow network scans

**Causes:**

- Large subnet (/16 network)
- Slow network response times
- Sequential scanning

**Solutions:**

- Use smaller subnet ranges
- Increase timeout values
- Be patient (large networks take time)
- /24 network: ~30-60 seconds
- /16 network: Could take hours

## Limitations

### Technical Limitations

1. **Platform Differences**

   - Commands vary by OS
   - Not all tools available everywhere
   - Output format differences
   - Feature availability varies

2. **Permissions Required**

   - Some scans need root/admin
   - RAW sockets for ICMP
   - Reading system network state

3. **Network Restrictions**

   - Firewalls may block scans
   - ICMP may be filtered
   - IDS/IPS may detect activity
   - Rate limiting by network devices

4. **Accuracy**
   - Hosts can ignore pings
   - Firewalls hide services
   - False negatives common
   - Port states may be filtered

### Detection Risks

1. **Network Traffic**

   - Ping sweeps generate noise
   - Port scans trigger IDS alerts
   - Unusual traffic patterns
   - High packet rate

2. **Logging**

   - Firewall logs connections
   - IDS/IPS alert on scans
   - SIEM systems detect patterns
   - Network monitoring tools

3. **Performance**
   - Network slowdown during scans
   - Bandwidth usage
   - Timeout increases

### Functional Limitations

1. **No Stealth**

   - All methods are noisy
   - Easily detected
   - Logged by network devices
   - Not suitable for covert ops

2. **Basic Scanning Only**

   - No OS fingerprinting
   - No service version detection
   - No vulnerability scanning
   - Limited port coverage

3. **No Advanced Features**
   - No SYN scan (stealth scan)
   - No UDP scan
   - No fragmentation
   - No timing controls

## Best Practices

### 1. Reconnaissance Order

```bash
# 1. Understand local network
net_info

# 2. Verify internet access
net_check_internet

# 3. Discover local hosts
net_scan

# 4. Examine connections
net_connections

# 5. Scan specific targets
net_portscan 192.168.1.1

# 6. Get public IP
net_public_ip
```

### 2. Stealth Considerations

```bash
# Minimize noise:
# - Scan during business hours
# - Use slower timing
# - Scan fewer ports
# - Avoid repeated scans

# Quick recon:
net_info
net_connections
# Avoid: net_scan, net_portscan
```

### 3. Target Selection

```bash
# Focus on important targets:
# 1. Gateway/router
net_portscan 192.168.1.1

# 2. DNS server
net_portscan <dns_ip>

# 3. Discovered hosts
net_scan
# Then scan interesting IPs
```

### 4. Data Collection

```bash
# Collect all network info at once
net_info > network_info.txt
net_scan > network_scan.txt
net_connections > connections.txt
net_public_ip > public_ip.txt

# Download for offline analysis
download network_info.txt
download network_scan.txt
```

## Attack Scenarios

### Scenario 1: Network Mapping

```bash
# 1. Understand local network
net_info
# Identifies: 192.168.1.50 on /24 network

# 2. Scan for live hosts
net_scan
# Finds: 6 hosts

# 3. Scan gateway
net_portscan 192.168.1.1
# Discovers: SSH, HTTP, HTTPS open

# Result: Network map created
```

---

### Scenario 2: Lateral Movement Prep

```bash
# 1. Find other systems
net_scan
# Discovers: 192.168.1.100, 192.168.1.105

# 2. Scan for services
net_portscan 192.168.1.100
# Finds: SSH (22), RDP (3389)

# 3. Target SMB shares, databases, etc.
# Plan next attack vector
```

---

### Scenario 3: Exfiltration Path Verification

```bash
# 1. Check internet access
net_check_internet
# Status: ONLINE

# 2. Get public IP
net_public_ip
# IP: 203.0.113.45

# 3. Check current connections
net_connections
# Verify backdoor connection
# Plan exfiltration methods
```

---

### Scenario 4: Service Discovery

```bash
# 1. Check what's running locally
net_connections
# Finds: MySQL (3306), Apache (80)

# 2. Scan localhost
net_portscan 127.0.0.1
# Confirm services

# 3. Exploit local services
# Target database, web server, etc.
```

## Performance Impact

### CPU Usage

- net_info: Minimal
- net_scan: Moderate (parallel processes)
- net_connections: Minimal
- net_portscan: Low (sequential connections)

### Network Impact

- net_scan: **High** traffic (ping all IPs)
- net_portscan: Moderate (connection attempts)
- Other commands: Minimal

### Time Requirements

- net_info: < 1 second
- net_scan: 30-60 seconds (/24)
- net_connections: < 1 second
- net_portscan: 20-40 seconds
- net_public_ip: 1-2 seconds
- net_check_internet: 2-5 seconds

## Security Considerations

### For Attackers

✅ Run network commands early in session
✅ Save output for offline analysis
✅ Minimize repeated scans
✅ Scan during normal business hours
✅ Focus on specific targets
❌ Don't scan entire internet ranges
❌ Avoid continuous scanning
❌ Don't ignore IDS alerts

### For Defenders

✅ Monitor for ping sweeps
✅ Alert on port scans
✅ Log all connection attempts
✅ Use IDS/IPS systems
✅ Implement rate limiting
✅ Segment networks
✅ Deploy honeypots

## Real-World Value

### What You Discover

- 🌐 Network topology
- 💻 Live hosts
- 🔓 Open services
- 🔌 Active connections
- 🌍 Public IP/location
- 🚪 Entry points for lateral movement
- 💾 Database servers
- 🖥️ Remote desktop services

### Detection Probability

- **High**: Port scans, ping sweeps
- **Medium**: Connection enumeration
- **Low**: Single host checks, public IP queries

## Summary

Network discovery features:
✅ Network interface enumeration
✅ Live host discovery
✅ Port scanning capabilities
✅ Connection monitoring
✅ Public IP identification
✅ Internet connectivity testing
✅ Cross-platform support
✅ Multiple fallback methods

**Warning:** Network scanning is noisy and easily detected. Use carefully in authorized testing only.

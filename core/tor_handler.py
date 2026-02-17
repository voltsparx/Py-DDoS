import socket
import time
import requests
from stem import Signal
from stem.control import Controller, EventType
from stem.util import term
import logging

class TORHandler:
    """Advanced TOR handler with circuit rotation, metrics, and error handling"""
    
    def __init__(self):
        self.controller = None
        self.enabled = False
        self.proxies = None
        self.circuit_count = 0
        self.rotation_count = 0
        self.connection_errors = 0
        self.last_rotation_time = None
        self.tor_port = 9050
        self.control_port = 9051
        self.bootstrap_status = None
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Setup logging for TOR operations with proper handlers"""
        logger = logging.getLogger('TORHandler')
        logger.setLevel(logging.DEBUG)
        
        # Add stream handler if not already present
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def check_tor_available(self):
        """Check if TOR daemon is running"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('127.0.0.1', self.control_port))
            sock.close()
            return result == 0
        except:
            return False
    
    def get_current_ip(self):
        """Get current exit IP for verification with fallback endpoints"""
        endpoints = [
            'http://icanhazip.com/',
            'http://api.ipify.org',
            'http://ifconfig.me/',
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(
                    endpoint,
                    proxies=self.proxies,
                    timeout=5
                )
                return response.text.strip()
            except Exception as e:
                self.logger.debug(f"Endpoint {endpoint} failed: {e}")
                self.connection_errors += 1
        
        self.logger.error("All IP check endpoints failed")
        return None
    
    def setup(self, console):
        """Initialize TOR control connection with error handling"""
        try:
            # Check if TOR is running
            if not self.check_tor_available():
                console.print("[red]✗ TOR daemon not running on port 9051[/red]")
                console.print("[yellow]  Install TOR and start it: tor --controlport 9051[/yellow]")
                return False
            
            # Connect to TOR control port
            self.controller = Controller.from_port(port=self.control_port)
            self.controller.authenticate()
            
            console.print("[green]✓ Connected to TOR control port[/green]")
            
            # Setup event listeners
            self._setup_events(console)
            
            # Test connection
            version = self.controller.get_version()
            console.print(f"[cyan]  TOR version: {version}[/cyan]")
            
            return True
        
        except Exception as e:
            console.print(f"[red]✗ TOR setup failed: {e}[/red]")
            self.logger.error(f"TOR setup error: {e}")
            return False
    
    def _setup_events(self, console):
        """Setup TOR event listeners"""
        try:
            def _log_bootstrap(line):
                if "Bootstrapped" in line:
                    console.print(f"[yellow]{line}[/yellow]")
            
            self.controller.add_event_listener(_log_bootstrap, EventType.INFO)
        except:
            pass
    
    def enable_stealth(self, console):
        """Enable TOR stealth mode with circuit rotation"""
        if not self.setup(console):
            return False
        
        try:
            # Request new circuit
            self.controller.signal(Signal.NEWNYM)
            time.sleep(2)  # Wait for new circuit
            
            self.proxies = {
                'http': f'socks5h://127.0.0.1:{self.tor_port}',
                'https': f'socks5h://127.0.0.1:{self.tor_port}'
            }
            
            # Verify connection
            current_ip = self.get_current_ip()
            if current_ip:
                console.print(f"[green]✓ TOR stealth enabled - Exit IP: {current_ip}[/green]")
                self.enabled = True
                self.circuit_count += 1
                self.rotation_count += 1
                return True
            else:
                console.print("[red]✗ Failed to verify TOR connection[/red]")
                return False
        
        except Exception as e:
            console.print(f"[red]✗ TOR stealth activation failed: {e}[/red]")
            self.logger.error(f"Stealth mode error: {e}")
            self.connection_errors += 1
            return False
    
    def rotate_circuit(self, console=None):
        """Rotate to new TOR circuit for anonymity"""
        if not self.enabled or not self.controller:
            return False
        
        try:
            self.controller.signal(Signal.NEWNYM)
            time.sleep(3)  # Wait for new circuit
            
            new_ip = self.get_current_ip()
            self.rotation_count += 1
            self.last_rotation_time = time.time()
            
            if console:
                console.print(f"[cyan]↻ Circuit rotated to IP: {new_ip}[/cyan]")
            
            self.logger.info(f"Circuit rotated. New IP: {new_ip}")
            return True
        
        except Exception as e:
            self.logger.error(f"Circuit rotation failed: {e}")
            self.connection_errors += 1
            return False
    
    def get_metrics(self):
        """Get TOR operation metrics"""
        return {
            'enabled': self.enabled,
            'circuits_created': self.circuit_count,
            'rotations': self.rotation_count,
            'connection_errors': self.connection_errors,
            'last_rotation': self.last_rotation_time
        }
    
    def cleanup(self):
        """Cleanup TOR resources"""
        try:
            if self.controller:
                self.controller.close()
                self.enabled = False
        except:
            pass
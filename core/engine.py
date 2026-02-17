"""
Py-DDoS Engine - Operational network stress test orchestration
Handles test execution, monitoring, and reporting

Features:
- Traditional threaded attacks
- Async HTTP high-performance engine
- Rate limiting and adaptive load control
- Target warm-up phase
- Dry-run mode for testing
- Structured JSON logging

Author: voltsparx
Contact: voltsparx@gmail.com
"""

import time
import threading
import socket
import os
import ipaddress
import requests
import statistics
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed

from .colors import Styles, Colors
from .attack import AttackWorkers
from .reporter import ReportGenerator
from .logger import AttackLogger
from .metrics import MetricsCollector
from .safety_locks import SafetyLocks
from .tor_handler import TORHandler
from .config import Config
from .counters import ThreadSafeCounter
from .rate_limiter import RateLimiter
from .structured_logger import StructuredJSONLogger
from .metadata import VERSION, PROJECT_NAME, AUTHOR, CONTACT


class AttackType(Enum):
    """Attack type enumeration to prevent typos"""
    HTTP = "HTTP"
    SLOWLORIS = "SLOWLORIS"
    SLOWREAD = "SLOWREAD"
    UDP = "UDP"
    SYN = "SYN"
    ICMP = "ICMP"
    DNS = "DNS"
    NTP = "NTP"


def is_private_ip(host):
    """Check if IP is private using ipaddress module. Resolves hostnames first."""
    try:
        # Try to resolve hostname to IP if needed
        try:
            ip_str = socket.gethostbyname(host)
        except (socket.gaierror, socket.herror):
            # If hostname resolution fails, assume it's already an IP
            ip_str = host
        
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback
    except ValueError:
        return False


class PyDDoS:
    """Main PyDDoS attack engine with advanced features"""
    
    MAX_RPS_HISTORY = 300  # Prevent unbounded memory growth
    WARMUP_DURATION = 5  # Warm-up phase duration (seconds)
    WARMUP_RPS = 100  # Warm-up target RPS
    
    def __init__(self, use_cli_output=True):
        self.logger = AttackLogger()
        self.json_logger = StructuredJSONLogger()
        self.safety_locks = SafetyLocks()
        self.metrics = MetricsCollector()
        self.attack_active = threading.Event()
        
        # Thread-safe counter with built-in lock
        self.packet_counter = ThreadSafeCounter()
        
        # Thread-safe RPS samples using deque
        from collections import deque
        self.rps_samples = deque(maxlen=self.MAX_RPS_HISTORY)
        self.rps_lock = threading.Lock()
        
        self.start_time = 0
        self.is_root = self._check_root()
        self.tor_handler = TORHandler()
        self.attack_workers = None
        self.rate_limiter = None
        self.use_cli_output = use_cli_output
        self.duration_timer = None
        
        # Adaptive load control state
        self.adaptive_enabled = False
        self.current_threads = 0
        self.current_rps_limit = None
        self.response_times = deque(maxlen=100)
        self.response_lock = threading.Lock()
        
        self.logger.log("Py-DDoS v7.1 Engine initialized with advanced features")
        self.use_cli_output = use_cli_output
        self.duration_timer = None
        
        self.logger.log("Py-DDoS v7.1 Engine initialized")
    
    def _check_root(self):
        """Check if running with root/admin privileges"""
        if os.name == 'nt':
            try:
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            except Exception:
                return False
        try:
            return os.geteuid() == 0
        except AttributeError:
            return False
    
    def check_target_status(self, host, port, scheme=None, verify_ssl=False):
        """Check target server status with fallback endpoints
        
        Args:
            host: Target hostname or IP
            port: Target port
            scheme: HTTP scheme ('http' or 'https')
            verify_ssl: Whether to verify SSL certificates
        """
        if scheme is None:
            scheme = "https" if port == 443 else "http"
        
        try:
            url = f"{scheme}://{host}:{port}/"
            resp = requests.get(url, timeout=2, verify=verify_ssl)
            return f"{resp.status_code}"
        except requests.Timeout:
            return "TIMEOUT"
        except requests.ConnectionError:
            return "DOWN"
        except requests.RequestException:
            return "ERROR"
        except Exception:
            return "ERROR"
    
    def _validate_config(self, config):
        """Validate configuration before execution"""
        if not config:
            raise ValueError("Configuration cannot be empty")
        
        # Check required fields
        required_fields = ['target_host', 'target_port', 'attack_type', 'threads', 'duration']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate target host
        if not isinstance(config['target_host'], str) or not config['target_host']:
            raise ValueError("target_host must be a non-empty string")
        
        # Validate port
        port = config['target_port']
        if not isinstance(port, int) or port < 1 or port > 65535:
            raise ValueError("target_port must be between 1 and 65535")
        
        # Validate thread count
        threads = config['threads']
        if not isinstance(threads, int) or threads < 1:
            raise ValueError("threads must be a positive integer")
        
        cpu_cores = self._get_cpu_cores()
        max_recommended = cpu_cores * 50  # Safer cap than 200
        if threads > max_recommended:
            self.logger.warning(f"Thread count {threads} exceeds recommended max {max_recommended}")
        
        # Validate duration
        duration = config['duration']
        if not isinstance(duration, (int, float)) or duration <= 0:
            raise ValueError("duration must be a positive number")
        
        # Validate attack type
        attack_type = config.get('attack_type', '').upper()
        valid_attacks = [a.value for a in AttackType]
        if attack_type not in valid_attacks:
            raise ValueError(f"attack_type must be one of: {', '.join(valid_attacks)}")
        
        # Check authorization flag
        if not config.get('authorized', False):
            raise PermissionError("Authorization required - set authorized=True in config")
        
        # Check external target authorization
        if not is_private_ip(config['target_host']):
            if not config.get('authorized_external', False):
                raise PermissionError(
                    "External target requires explicit authorization - "
                    "set authorized_external=True after obtaining written permission"
                )
        
        # Validate optional parameters
        # Dry-run mode
        if 'dry_run' in config:
            if not isinstance(config['dry_run'], bool):
                raise ValueError("dry_run must be a boolean")
        
        # Rate limiting parameters
        if 'global_rps_limit' in config:
            val = config['global_rps_limit']
            if val is not None and (not isinstance(val, (int, float)) or val <= 0):
                raise ValueError("global_rps_limit must be a positive number or None")
        
        if 'per_thread_rps_limit' in config:
            val = config['per_thread_rps_limit']
            if val is not None and (not isinstance(val, (int, float)) or val <= 0):
                raise ValueError("per_thread_rps_limit must be a positive number or None")
        
        # Warm-up parameters
        if 'warmup_enabled' in config:
            if not isinstance(config['warmup_enabled'], bool):
                raise ValueError("warmup_enabled must be a boolean")
        
        # Adaptive load control
        if 'adaptive_load_control' in config:
            if not isinstance(config['adaptive_load_control'], bool):
                raise ValueError("adaptive_load_control must be a boolean")
        
        return True
    
    def run_attack(self, config):
        """Execute the attack with given configuration"""
        
        # Validate configuration
        try:
            self._validate_config(config)
        except (ValueError, PermissionError) as e:
            self._print(Styles.error(f"Configuration error: {e}"))
            self.logger.error(f"Config validation failed: {e}")
            return False
        
        self.target_host = config['target_host']
        self.target_input = config.get('target_input', config['target_host'])
        self.target_port = config['target_port']
        self.attack_type = config['attack_type'].upper()
        self.threads = config['threads']
        self.duration = config['duration']
        self.use_tor = config.get('use_tor', False)
        self.proxies = config.get('proxies', None)
        self.dry_run = config.get('dry_run', False)
        
        # Structured logging
        self.json_logger.log_attack_start(
            self.attack_type,
            self.target_host,
            self.target_port,
            self.threads,
            self.duration,
            config
        )
        
        # Setup rate limiting
        global_rps = config.get('global_rps_limit', None)
        per_thread_rps = config.get('per_thread_rps_limit', None)
        if global_rps or per_thread_rps:
            self.rate_limiter = RateLimiter(global_rps, per_thread_rps)
            self._print(Styles.info(f"Rate limiting enabled: {global_rps} global RPS, {per_thread_rps} per-thread"))
        
        # Adaptive load control
        self.adaptive_enabled = config.get('adaptive_load_control', False)
        if self.adaptive_enabled:
            self._print(Styles.info("Adaptive load control enabled"))
        
        # Check dry-run mode
        if self.dry_run:
            self._print(Styles.warning("DRY-RUN MODE: No packets will be sent, only metrics simulated"))
            self.json_logger.log_event(
                'dry_run_start',
                'WARNING',
                'Starting attack in DRY-RUN mode - no packets will be sent',
                {'target': f"{self.target_host}:{self.target_port}", 'attack_type': self.attack_type}
            )
        
        self._print(Styles.section(f"STARTING {self.attack_type.upper()} NETWORK STRESS TEST"))
        self.use_tor = config.get('use_tor', False)
        self.proxies = config.get('proxies', None)
        
        self._print(Styles.section(f"STARTING {self.attack_type.upper()} NETWORK STRESS TEST"))
        self._print()
        
        # Setup TOR if requested
        if self.use_tor:
            self._print(Styles.info("Setting up TOR anonymity layer..."))
            try:
                if self.tor_handler.enable_stealth():
                    self.proxies = self.tor_handler.proxies
                    self._print(Styles.success("TOR stealth mode enabled"))
                    self.logger.log("TOR stealth mode enabled")
                else:
                    self._print(Styles.warning("TOR setup failed, continuing without anonymity"))
                    self.logger.log("TOR setup failed")
                    self.use_tor = False
            except Exception as e:
                self._print(Styles.warning(f"TOR setup error: {e}. Continuing without anonymity"))
                self.logger.warning(f"TOR setup error: {e}")
                self.use_tor = False
        
        self.logger.log(f"Network stress test session started: {self.attack_type} on {self.target_input}:{self.target_port}")
        
        # Warm-up phase (unless dry-run)
        if not self.dry_run and config.get('warmup_enabled', True):
            self._warmup_phase()
        
        # Execute attack
        if not self.dry_run:
            self.execute_attack()
        else:
            self._print(Styles.warning("Dry-run mode: skipping actual attack execution"))
            self.json_logger.log_event(
                'dry_run_skip_execution',
                'INFO',
                'Skipped actual attack execution in dry-run mode',
                {'attack_type': self.attack_type}
            )
        
        # Calculate statistics
        elapsed = time.time() - self.start_time
        stats = {
            'total_packets': self.packet_counter.get(),
            'avg_rps': sum(self.rps_samples) / len(self.rps_samples) if self.rps_samples else 0,
            'peak_rps': max(self.rps_samples) if self.rps_samples else 0,
            'duration': elapsed,
            'attack_type': self.attack_type,
            'target': f"{self.target_input}:{self.target_port}"
        }
        
        if self.attack_workers:
            stats['success_count'] = self.attack_workers.metrics.success_count
            stats['error_count'] = self.attack_workers.metrics.error_count
            stats['bytes_sent'] = self.attack_workers.metrics.bytes_sent
            stats['packets_sent'] = self.attack_workers.metrics.packets_sent
            success_rate = (self.attack_workers.metrics.success_count / max(
                self.attack_workers.metrics.success_count + self.attack_workers.metrics.error_count, 1
            )) * 100
            stats['success_rate'] = success_rate
        
        if self.use_tor:
            stats['tor_metrics'] = self.tor_handler.get_metrics()
        
        # Log attack completion with structured logging
        self.json_logger.log_attack_complete(
            self.attack_type,
            stats.get('total_packets', 0),
            stats.get('success_count', 0),
            stats.get('error_count', 0),
            stats['avg_rps'],
            stats['peak_rps'],
            elapsed,
            stats.get('success_rate', 0),
            self.dry_run
        )
        self.json_logger.log_attack_complete(
            self.attack_type,
            stats.get('success_count', 0),
            stats.get('error_count', 0),
            stats.get('total_packets', 0),
            stats['duration'],
            stats['avg_rps'],
            stats['peak_rps'],
            stats.get('success_rate', 0)
        )
        
        # Print final statistics
        self._print()
        self._print(Styles.section("NETWORK STRESS TEST STATISTICS"))
        self._print()
        self._print(Styles.metric("Total Packets Sent", f"{stats['total_packets']:,}"))
        self._print(Styles.metric("Total Bytes Sent", f"{stats.get('bytes_sent', 0):,}"))
        self._print(Styles.metric("Average RPS", f"{stats['avg_rps']:.2f}"))
        self._print(Styles.metric("Peak RPS", f"{stats['peak_rps']:.2f}"))
        self._print(Styles.metric("Duration", f"{stats['duration']:.2f} seconds"))
        self._print(Styles.metric("Success Rate", f"{stats.get('success_rate', 0):.2f}%"))
        self._print()
        
        # Generate reports (both HTML and TXT)
        reporter = ReportGenerator("reports")
        html_report_path, txt_report_path = reporter.generate(stats, config, self.rps_samples)
        self._print(Styles.success(f"HTML Report: {html_report_path}"))
        self._print(Styles.success(f"TXT Report:  {txt_report_path}"))
        self._print(Styles.success(f"Log file:    {self.logger.get_log_path()}"))
        
        # Cleanup
        if self.use_tor:
            self.tor_handler.cleanup()
        
        self.logger.log(f"Network stress test completed successfully")
        self._print()
        
        return True
    
    def execute_attack(self):
        """Execute the actual attack with worker threads"""
        self.attack_active.set()
        self.start_time = time.time()
        
        def rps_monitor():
            """Monitor requests per second with bounded history"""
            while self.attack_active.is_set():
                time.sleep(1)
                elapsed = time.time() - self.start_time
                rps = self.packet_counter.get() / max(elapsed, 1)
                with self.rps_lock:
                    self.rps_samples.append(rps)
        
        def live_dashboard():
            """Display live attack statistics - updated every 0.5s to reduce CPU"""
            last_print = time.time()
            while self.attack_active.is_set():
                current_time = time.time()
                # Update every 0.5 seconds instead of checking every 0.1s
                if current_time - last_print >= 0.5:
                    elapsed = current_time - self.start_time
                    total = self.packet_counter.get()
                    rps = total / max(elapsed, 1)
                    status = self.check_target_status(self.target_host, self.target_port)
                    
                    # Clear line and print stats
                    self._print(f"\r{Colors.BRIGHT_CYAN}[*] {total:>10} packets | "
                               f"{rps:>8.2f} RPS | "
                               f"{elapsed:>6.1f}s | "
                               f"Status: {status}{Colors.RESET}", end='', flush=True)
                    
                    last_print = current_time
                time.sleep(0.1)
            print()  # New line after attack ends
        
        def duration_timer():
            """Stop attack after specified duration"""
            time.sleep(self.duration)
            if self.attack_active.is_set():
                self._print()
                self._print(Styles.info(f"Attack duration ({self.duration}s) reached. Stopping..."))
                self.attack_active.clear()
        
        # Start monitoring threads
        monitor_thread = threading.Thread(target=rps_monitor, daemon=True)
        dashboard_thread = threading.Thread(target=live_dashboard, daemon=True)
        timer_thread = threading.Thread(target=duration_timer, daemon=True)
        monitor_thread.start()
        dashboard_thread.start()
        timer_thread.start()
        
        # Start adaptive load monitor if enabled
        adaptive_thread = None
        if self.adaptive_enabled:
            self.current_threads = self.threads  # Initialize adaptive tracking
            adaptive_thread = threading.Thread(target=self._adaptive_load_monitor, daemon=True)
            adaptive_thread.start()
            self._print(Styles.info("Adaptive load control monitor started"))
        
        # Initialize attack workers
        self.attack_workers = AttackWorkers(
            self.target_host,
            self.target_port,
            self.attack_active,
            self.packet_counter,
            self.use_tor,
            self.proxies
        )
        
        # Map attack types to worker methods
        attack_map = {
            'HTTP': self.attack_workers.http_flood,
            'SLOWLORIS': self.attack_workers.slowloris,
            'UDP': self.attack_workers.udp_flood,
            'SYN': self.attack_workers.syn_flood,
            'SLOWREAD': self.attack_workers.slowread,
            'DNS': self.attack_workers.dns_amplification,
            'ICMP': self.attack_workers.icmp_flood,
            'NTP': self.attack_workers.ntp_amplification,
        }
        
        worker_func = attack_map.get(self.attack_type, self.attack_workers.http_flood)
        
        self._print(Styles.info(f"Starting {self.threads} worker threads..."))
        self.logger.log(f"Starting {self.threads} worker threads for {self.attack_type} stress test")
        
        # Execute attack with thread pool
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(worker_func) for _ in range(self.threads)]
            try:
                # Wait without timeout - let duration_timer handle stopping
                self._print(Styles.info("Press Ctrl+C to stop the attack immediately"))
                # Just wait for futures to complete
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        self.logger.warning(f"Worker thread error: {e}")
            except KeyboardInterrupt:
                self._print()
                self._print(Styles.warning("Network stress test interrupted by user (Ctrl+C)"))
                self.logger.warning("Network stress test interrupted by user (Ctrl+C)")
                self.attack_active.clear()
            except Exception as e:
                self.logger.error(f"Attack execution error: {e}")
            finally:
                self.attack_active.clear()
                self._print(Styles.info(f"Test workers terminated after {time.time() - self.start_time:.2f}s"))
                self.logger.log(f"Test workers terminated")
    
    def _warmup_phase(self, target_rps=100, duration=5):
        """
        Warm-up phase: gradually ramp load to stabilize target
        
        Args:
            target_rps: Target RPS to reach (default: 100)
            duration: Duration in seconds (default: 5)
        """
        self._print(Styles.info(f"Starting warm-up phase ({duration}s, ramping to {target_rps} RPS)..."))
        self.json_logger.log_event(
            'warmup_start',
            'INFO',
            f'Warm-up phase starting: {duration}s duration, target {target_rps} RPS',
            {'target_rps': target_rps, 'duration': duration}
        )
        
        warmup_start = time.time()
        initial_packets = self.packet_counter.get()
        
        # Simple worker for warm-up (single thread, gradually increasing load)
        def warmup_worker():
            while time.time() - warmup_start < duration and self.attack_active.is_set():
                # Calculate elapsed time (0.0 to 1.0)
                elapsed = time.time() - warmup_start
                progress = min(elapsed / duration, 1.0)
                
                # Linear ramp from ~10 RPS to target_rps
                current_target = 10 + (target_rps - 10) * progress
                requests_per_cycle = int(current_target / 10)  # 10 cycles per second
                
                for _ in range(requests_per_cycle):
                    if not self.attack_active.is_set():
                        break
                    
                    try:
                        if self.attack_type == "HTTP":
                            self.attack_workers.send_http_request(self.target_host, self.target_port)
                        elif self.attack_type == "UDP":
                            self.attack_workers.send_udp_packet(self.target_host, self.target_port)
                        elif self.attack_type == "TCP":
                            self.attack_workers.send_tcp_packet(self.target_host, self.target_port)
                        
                        self.packet_counter.increment()
                        
                        # Track response time for adaptive control
                        with self.response_lock:
                            self.response_times.append(time.time())
                    except Exception as e:
                        self.logger.debug(f"Warm-up request error: {e}")
                
                # Sleep to maintain rate
                time.sleep(0.1)
        
        # Run warm-up with minimal threads
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                warmup_future = executor.submit(warmup_worker)
                warmup_future.result(timeout=duration + 1)
        except Exception as e:
            self.logger.warning(f"Warm-up phase error: {e}")
        
        warmup_packets = self.packet_counter.get() - initial_packets
        avg_response = statistics.mean(
            [t for t in self.response_times if t > warmup_start]
        ) - warmup_start if self.response_times else 0
        
        self._print(Styles.success(f"Warm-up complete: {warmup_packets} requests sent"))
        self.json_logger.log_warmup_phase(
            'complete',
            warmup_packets,
            int(target_rps * duration),
            avg_response
        )
    
    def _adaptive_load_monitor(self):
        """
        Monitor attack metrics and dynamically adjust load
        Runs in background thread during attack
        """
        monitor_interval = 2  # Check every 2 seconds
        last_check = time.time()
        baseline_threads = self.threads
        baseline_rps = self.attack_workers.metrics.get() if hasattr(self.attack_workers.metrics, 'get') else 0
        
        while self.attack_active.is_set():
            try:
                time.sleep(0.5)
                now = time.time()
                
                if now - last_check < monitor_interval:
                    continue
                
                last_check = now
                
                # Get current metrics
                total_packets = self.packet_counter.get()
                success_count = self.attack_workers.metrics.success_count
                error_count = self.attack_workers.metrics.error_count
                total_requests = success_count + error_count
                
                if total_requests == 0:
                    continue
                
                # Calculate metrics
                error_rate = error_count / total_requests if total_requests > 0 else 0
                success_rate = success_count / total_requests if total_requests > 0 else 0
                
                # Calculate average response time
                with self.response_lock:
                    if self.response_times:
                        recent_times = list(self.response_times)[-20:]
                        if recent_times:
                            avg_response_time = statistics.mean(recent_times)
                        else:
                            avg_response_time = 0
                    else:
                        avg_response_time = 0
                
                # Determine adjustments
                should_decrease = (
                    error_rate > 0.10 or  # Error rate > 10%
                    (avg_response_time > 0.5 and self.attack_type == "HTTP") or  # Response time > 500ms
                    success_rate < 0.85  # Success rate dropped
                )
                
                should_increase = (
                    error_rate < 0.05 and  # Error rate < 5%
                    (avg_response_time < 0.2 or self.attack_type != "HTTP") and  # Good response time
                    success_rate > 0.95  # Success rate > 95%
                )
                
                # Apply adjustments
                if should_decrease and self.current_threads > max(1, baseline_threads // 2):
                    self.current_threads = max(1, int(self.current_threads * 0.9))
                    action = "DECREASED"
                    reason = f"Error rate {error_rate:.1%}, Response time {avg_response_time:.3f}s, Success {success_rate:.1%}"
                    
                    self.json_logger.log_adaptive_control(
                        action, reason,
                        int(self.threads), int(self.current_threads),
                        0, 0,
                        'error_rate' if error_rate > 0.10 else 'response_time',
                        error_rate if error_rate > 0.10 else avg_response_time
                    )
                    self._print(Styles.warning(f"[Adaptive] Load decreased: {reason}"))
                
                elif should_increase and self.current_threads < baseline_threads * 1.5:
                    self.current_threads = min(int(baseline_threads * 1.5), int(self.current_threads * 1.1))
                    action = "INCREASED"
                    reason = f"Error rate {error_rate:.1%}, Response time {avg_response_time:.3f}s, Success {success_rate:.1%}"
                    
                    self.json_logger.log_adaptive_control(
                        action, reason,
                        int(self.threads), int(self.current_threads),
                        0, 0,
                        'all_metrics_good',
                        success_rate
                    )
                    self._print(Styles.success(f"[Adaptive] Load increased: {reason}"))
            
            except Exception as e:
                self.logger.debug(f"Adaptive monitor error: {e}")
    
    def _print(self, message='', **kwargs):
        """
        Print message based on CLI output setting
        
        Args:
            message: Text to print (default: empty string for newline)
            **kwargs: Additional arguments to pass to print()
        """
        if self.use_cli_output:
            print(message, **kwargs)
    
    def _get_cpu_cores(self):
        """Get number of CPU cores safely"""
        return os.cpu_count() or 1


__all__ = ['PyDDoS', 'AttackType', 'is_private_ip']
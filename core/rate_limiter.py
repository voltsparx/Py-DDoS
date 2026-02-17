"""
Rate Limiting for Py-DDoS - Token Bucket Algorithm
Prevents self-DoS and controls request rates per thread

Implements:
- Token bucket algorithm for smooth rate limiting
- Per-thread and global rate limits
- Adaptive burst capacity
- Configurable refill rates

Author: voltsparx
Contact: voltsparx@gmail.com
"""

import time
import threading
from typing import Optional


class TokenBucket:
    """
    Token bucket rate limiter using token bucket algorithm
    
    Allows bursts up to capacity, then refills at fixed rate.
    Thread-safe implementation suitable for concurrent workers.
    
    Attributes:
        capacity: Maximum tokens in bucket (burst size)
        refill_rate: Tokens added per second
        tokens: Current token count
        last_refill: Timestamp of last refill
    """
    
    def __init__(self, capacity: float, refill_rate: float):
        """
        Initialize token bucket
        
        Args:
            capacity: Maximum tokens (burst size)
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = threading.Lock()
    
    def _refill(self):
        """Refill bucket based on elapsed time"""
        now = time.time()
        elapsed = now - self.last_refill
        new_tokens = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill = now
    
    def consume(self, tokens: float = 1.0, block: bool = True) -> bool:
        """
        Consume tokens from bucket
        
        Args:
            tokens: Number of tokens to consume (default: 1)
            block: Whether to wait until tokens available (default: True)
        
        Returns:
            True if tokens consumed, False if not available (non-blocking)
        """
        with self.lock:
            self._refill()
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            
            if not block:
                return False
            
            # Calculate wait time for tokens
            needed = tokens - self.tokens
            wait_time = needed / self.refill_rate
            
            # Release lock during wait
            self.lock.release()
            try:
                time.sleep(wait_time)
                return self.consume(tokens, block=False)
            finally:
                self.lock.acquire()
    
    def get_wait_time(self, tokens: float = 1.0) -> float:
        """
        Get time to wait for tokens without blocking
        
        Args:
            tokens: Number of tokens to check
        
        Returns:
            Wait time in seconds
        """
        with self.lock:
            self._refill()
            
            if self.tokens >= tokens:
                return 0.0
            
            needed = tokens - self.tokens
            return needed / self.refill_rate
    
    def reset(self):
        """Reset bucket to full capacity"""
        with self.lock:
            self.tokens = self.capacity
            self.last_refill = time.time()


class RateLimiter:
    """
    Multi-level rate limiter with global and per-thread limits
    
    Coordinates multiple worker threads to prevent self-DoS while
    allowing fine-grained control over request rates.
    
    Attributes:
        global_limit: Requests per second (all threads combined)
        per_thread_limit: Requests per second (individual thread)
        burst_multiplier: Burst capacity = limit × multiplier
    """
    
    def __init__(
        self,
        global_rps: Optional[float] = None,
        per_thread_rps: Optional[float] = None,
        burst_multiplier: float = 2.0
    ):
        """
        Initialize rate limiter
        
        Args:
            global_rps: Global requests per second limit (None = unlimited)
            per_thread_rps: Per-thread requests per second limit (None = unlimited)
            burst_multiplier: Capacity multiplier for token bucket (default: 2x)
        """
        self.global_rps = global_rps
        self.per_thread_rps = per_thread_rps
        self.burst_multiplier = burst_multiplier
        
        # Create buckets
        self.global_bucket = None
        self.per_thread_buckets = {}
        self.buckets_lock = threading.Lock()
        
        if global_rps and global_rps > 0:
            capacity = global_rps * burst_multiplier
            self.global_bucket = TokenBucket(capacity, global_rps)
    
    def acquire(self, thread_id: Optional[int] = None, tokens: float = 1.0, block: bool = True) -> bool:
        """
        Acquire tokens from rate limiter
        
        Checks both global and per-thread limits.
        
        Args:
            thread_id: Thread identifier (auto-detected if None)
            tokens: Number of tokens (default: 1)
            block: Whether to wait for tokens (default: True)
        
        Returns:
            True if tokens acquired, False if not available (non-blocking)
        """
        if thread_id is None:
            thread_id = threading.current_thread().ident
        
        # Check global limit
        if self.global_bucket:
            if not self.global_bucket.consume(tokens, block=block):
                return False
        
        # Check per-thread limit
        if self.per_thread_rps and self.per_thread_rps > 0:
            bucket = self._get_per_thread_bucket(thread_id)
            if not bucket.consume(tokens, block=block):
                if self.global_bucket:
                    # Refund global tokens if per-thread check failed
                    with self.global_bucket.lock:
                        self.global_bucket.tokens += tokens
                return False
        
        return True
    
    def _get_per_thread_bucket(self, thread_id: int) -> TokenBucket:
        """Get or create per-thread bucket"""
        with self.buckets_lock:
            if thread_id not in self.per_thread_buckets:
                capacity = self.per_thread_rps * self.burst_multiplier
                self.per_thread_buckets[thread_id] = TokenBucket(
                    capacity,
                    self.per_thread_rps
                )
            return self.per_thread_buckets[thread_id]
    
    def get_load_factor(self) -> float:
        """
        Get current load as fraction of capacity
        
        Returns:
            Load factor 0.0-1.0 (0 = empty, 1 = full)
        """
        if not self.global_bucket:
            return 0.0
        
        with self.global_bucket.lock:
            return 1.0 - (self.global_bucket.tokens / self.global_bucket.capacity)
    
    def reset(self):
        """Reset all rate limiters"""
        if self.global_bucket:
            self.global_bucket.reset()
        
        with self.buckets_lock:
            for bucket in self.per_thread_buckets.values():
                bucket.reset()


__all__ = ['TokenBucket', 'RateLimiter']

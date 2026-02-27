"""
Thread-safe counter utilities for attack coordination
Provides simple counter interface with thread-safe increments

Author: voltsparx
Contact: voltsparx@gmail.com
"""

import threading


class ThreadSafeCounter:
    """Thread-safe integer counter with lock management"""
    
    def __init__(self, initial=0):
        """
        Initialize counter with optional initial value
        
        Args:
            initial: Starting counter value (default: 0)
        """
        self.value = initial
        self.lock = threading.Lock()
    
    def increment(self, amount=1):
        """
        Thread-safe increment
        
        Args:
            amount: Number to increment by (default: 1)
            
        Returns:
            New counter value
        """
        with self.lock:
            self.value += amount
            return self.value
    
    def decrement(self, amount=1):
        """
        Thread-safe decrement
        
        Args:
            amount: Number to decrement by (default: 1)
            
        Returns:
            New counter value
        """
        with self.lock:
            self.value -= amount
            return self.value
    
    def get(self):
        """Get current counter value"""
        with self.lock:
            return self.value
    
    def get_lock(self):
        """Get lock for optional multiprocessing usage (multiprocessing.Value compatibility)"""
        return self.lock
    
    def reset(self):
        """Reset counter to zero"""
        with self.lock:
            self.value = 0
    
    def __str__(self):
        return str(self.get())
    
    def __repr__(self):
        return f"ThreadSafeCounter({self.get()})"
    
    def __int__(self):
        return self.get()


__all__ = ['ThreadSafeCounter']

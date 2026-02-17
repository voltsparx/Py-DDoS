"""
Real-time metrics tracking and analysis for network stress testing
Captures performance data throughout test execution

Author: voltsparx
Contact: voltsparx@gmail.com

Features:
- Real-time RPS tracking
- Bandwidth measurement
- Response time analysis
- Connection state tracking
- Resource usage monitoring
- Statistical analysis
"""

import time
import threading
from collections import deque, defaultdict
from statistics import mean, median, stdev
from datetime import datetime


class MetricsCollector:
    """Comprehensive metrics collection for network stress tests"""
    
    def __init__(self, max_history=1000):
        self.start_time = time.time()
        self.end_time = None
        self.max_history = max_history
        
        # Core metrics
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_bytes_sent = 0
        self.total_bytes_received = 0
        
        # Time-series data
        self.timestamps = deque(maxlen=max_history)
        self.rps_history = deque(maxlen=max_history)
        self.bandwidth_history = deque(maxlen=max_history)
        self.response_times = deque(maxlen=max_history)
        
        # Connection tracking
        self.connection_states = defaultdict(int)  # established, timeout, refused
        self.http_response_codes = defaultdict(int)  # 200, 404, 503, etc
        
        # Lock for thread-safe operations
        self._lock = threading.Lock()
        
        # Tracking window
        self.last_request_count = 0
        self.last_timestamp = self.start_time
    
    def record_request(self, success=True, response_time=0, bytes_sent=0, bytes_received=0, 
                      status_code=None, connection_state=None):
        """Record a single request"""
        with self._lock:
            self.total_requests += 1
            
            if success:
                self.successful_requests += 1
                if status_code:
                    self.http_response_codes[status_code] += 1
            else:
                self.failed_requests += 1
            
            self.total_bytes_sent += bytes_sent
            self.total_bytes_received += bytes_received
            self.response_times.append(response_time)
            
            if connection_state:
                self.connection_states[connection_state] += 1
    
    def get_elapsed_time(self):
        """Get elapsed seconds since start"""
        return time.time() - self.start_time
    
    def calculate_rps(self):
        """Calculate current requests per second"""
        elapsed = self.get_elapsed_time()
        if elapsed == 0:
            return 0
        return self.total_requests / elapsed
    
    def calculate_bandwidth(self):
        """Calculate current bandwidth (MB/s)"""
        elapsed = self.get_elapsed_time()
        if elapsed == 0:
            return 0
        total_mb = (self.total_bytes_sent + self.total_bytes_received) / (1024 * 1024)
        return total_mb / elapsed
    
    def get_response_time_stats(self):
        """Get response time statistics"""
        if not self.response_times:
            return {
                'min': 0,
                'max': 0,
                'mean': 0,
                'median': 0,
                'stdev': 0
            }
        
        times_list = list(self.response_times)
        return {
            'min': min(times_list),
            'max': max(times_list),
            'mean': mean(times_list),
            'median': median(times_list),
            'stdev': stdev(times_list) if len(times_list) > 1 else 0
        }
    
    def get_success_rate(self):
        """Get success rate percentage"""
        if self.total_requests == 0:
            return 0
        return (self.successful_requests / self.total_requests) * 100
    
    def get_summary(self):
        """Get comprehensive metrics summary"""
        rt_stats = self.get_response_time_stats()
        
        return {
            'duration': self.get_elapsed_time(),
            'total_requests': self.total_requests,
            'successful': self.successful_requests,
            'failed': self.failed_requests,
            'success_rate': self.get_success_rate(),
            'rps': self.calculate_rps(),
            'bandwidth_mbps': self.calculate_bandwidth(),
            'total_bytes_sent': self.total_bytes_sent,
            'total_bytes_received': self.total_bytes_received,
            'response_times': rt_stats,
            'http_codes': dict(self.http_response_codes),
            'connection_states': dict(self.connection_states)
        }
    
    def get_time_series_data(self):
        """Get time-series data for graphing"""
        return {
            'timestamps': list(self.timestamps),
            'rps': list(self.rps_history),
            'bandwidth': list(self.bandwidth_history),
        }
    
    def record_window_metrics(self):
        """Record metrics for current time window (call periodically)"""
        with self._lock:
            current_time = time.time()
            current_count = self.total_requests
            
            time_delta = current_time - self.last_timestamp
            request_delta = current_count - self.last_request_count
            
            if time_delta > 0:
                rps = request_delta / time_delta
                bw = ((self.total_bytes_sent + self.total_bytes_received) / (1024 * 1024)) / time_delta
                
                self.timestamps.append(current_time - self.start_time)
                self.rps_history.append(rps)
                self.bandwidth_history.append(bw)
            
            self.last_timestamp = current_time
            self.last_request_count = current_count
    
    def finalize(self):
        """Finalize metrics at test completion"""
        self.end_time = time.time()
    
    def get_test_classification(self):
        """Classify test effectiveness"""
        success_rate = self.get_success_rate()
        rps = self.calculate_rps()
        bandwidth = self.calculate_bandwidth()
        
        if success_rate < 10:
            return "MINIMAL - Server handling attack effectively"
        elif success_rate < 30:
            return "LOW - Server experiencing stress but functional"
        elif success_rate < 50:
            return "MODERATE - Server degraded but operational"
        elif success_rate < 80:
            return "HIGH - Server severely impacted"
        else:
            return "CRITICAL - Server unable to handle load"
    
    def get_educational_insights(self):
        """Generate educational insights from metrics"""
        insights = []
        
        rt_stats = self.get_response_time_stats()
        
        # Response time analysis
        if rt_stats['mean'] > 5:
            insights.append("Server response times are elevated (>5s avg) - indicating resource constraint")
        
        # Success rate analysis
        success = self.get_success_rate()
        if success < 50:
            insights.append("Low success rate indicates effective server rejection of requests")
        
        # Bandwidth analysis
        bw = self.calculate_bandwidth()
        if bw > 100:
            insights.append(f"High bandwidth consumption ({bw:.2f}MB/s) - monitor network capacity")
        
        # HTTP codes analysis
        codes = dict(self.http_response_codes)
        if codes.get(503, 0) > self.successful_requests * 0.1:
            insights.append("Service unavailable (503) responses indicate successful load impact")
        
        if codes.get(502, 0) > self.successful_requests * 0.1:
            insights.append("Bad gateway (502) responses suggest load balancer/upstream issues")
        
        if codes.get(408, 0) > 0:
            insights.append("Request timeout (408) responses indicate connection exhaustion")
        
        # Connection state analysis
        conn_states = dict(self.connection_states)
        if conn_states.get('timeout', 0) > conn_states.get('established', 0):
            insights.append("High timeout rate suggests connection limits reached")
        
        if conn_states.get('refused', 0) > 0:
            insights.append("Connection refusal indicates active server-side mitigation")
        
        return insights if insights else ["Test completed - server responding normally"]

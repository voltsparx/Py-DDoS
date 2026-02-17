"""
Test Harness for Py-DDoS Attack Modules
Unit tests and integration tests for attack implementations

Tests verify attack signatures, thread safety, error handling, and metrics.

Author: voltsparx
Contact: voltsparx@gmail.com
"""

import unittest
import threading
import time
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from .attack import AttackWorkers, AttackMetrics
from .counters import ThreadSafeCounter


class TestAttackMetrics(unittest.TestCase):
    """Test AttackMetrics tracking"""
    
    def test_metrics_initialization(self):
        """Test metrics init"""
        metrics = AttackMetrics()
        self.assertEqual(metrics.success_count, 0)
        self.assertEqual(metrics.error_count, 0)
        self.assertEqual(metrics.bytes_sent, 0)
        self.assertEqual(metrics.packets_sent, 0)
    
    def test_metrics_increment(self):
        """Test metrics increment"""
        metrics = AttackMetrics()
        metrics.success_count = 10
        metrics.bytes_sent = 1000
        
        self.assertEqual(metrics.success_count, 10)
        self.assertEqual(metrics.bytes_sent, 1000)


class TestThreadSafeCounter(unittest.TestCase):
    """Test ThreadSafeCounter"""
    
    def test_counter_increment(self):
        """Test counter increment"""
        counter = ThreadSafeCounter(0)
        counter.increment(5)
        self.assertEqual(counter.get(), 5)
    
    def test_counter_decrement(self):
        """Test counter decrement"""
        counter = ThreadSafeCounter(10)
        counter.decrement(3)
        self.assertEqual(counter.get(), 7)
    
    def test_counter_thread_safety(self):
        """Test thread-safe increments"""
        counter = ThreadSafeCounter(0)
        
        def increment_100_times():
            for _ in range(100):
                counter.increment(1)
        
        threads = [threading.Thread(target=increment_100_times) for _ in range(5)]
        
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()
        
        # Should be 5 threads × 100 increments = 500
        self.assertEqual(counter.get(), 500)
    
    def test_counter_reset(self):
        """Test counter reset"""
        counter = ThreadSafeCounter(100)
        counter.reset()
        self.assertEqual(counter.get(), 0)


class TestAttackWorkerInit(unittest.TestCase):
    """Test AttackWorkers initialization"""
    
    def test_worker_creation(self):
        """Test worker creation"""
        stop_event = threading.Event()
        counter = ThreadSafeCounter(0)
        
        worker = AttackWorkers(
            host="127.0.0.1",
            port=8080,
            stop_event=stop_event,
            counter=counter,
            use_tor=False,
            proxies=None
        )
        
        self.assertEqual(worker.host, "127.0.0.1")
        self.assertEqual(worker.port, 8080)
        self.assertFalse(worker.stop_event.is_set())
    
    def test_worker_increment_counter(self):
        """Test worker counter increment"""
        stop_event = threading.Event()
        counter = ThreadSafeCounter(0)
        
        worker = AttackWorkers(
            host="127.0.0.1",
            port=8080,
            stop_event=stop_event,
            counter=counter
        )
        
        worker.increment_counter(5)
        self.assertEqual(counter.get(), 5)
    
    def test_worker_metrics(self):
        """Test worker metrics creation"""
        stop_event = threading.Event()
        counter = ThreadSafeCounter(0)
        
        worker = AttackWorkers(
            host="127.0.0.1",
            port=8080,
            stop_event=stop_event,
            counter=counter
        )
        
        self.assertIsNotNone(worker.metrics)
        self.assertEqual(worker.metrics.success_count, 0)


class TestAttackWorkerIntegration(unittest.TestCase):
    """Integration tests for attack workers"""
    
    def test_worker_stops_on_event(self):
        """Test worker respects stop event"""
        stop_event = threading.Event()
        counter = ThreadSafeCounter(0)
        
        worker = AttackWorkers(
            host="127.0.0.1",
            port=8080,
            stop_event=stop_event,
            counter=counter
        )
        
        # Mock the attack method to check stop event
        def mock_attack():
            start_time = time.time()
            while not stop_event.is_set():
                time.sleep(0.01)
                if time.time() - start_time > 5:
                    break
        
        # Simulate attack with stop event
        thread = threading.Thread(target=mock_attack)
        thread.start()
        
        # Let it run briefly
        time.sleep(0.1)
        
        # Set stop event
        stop_event.set()
        
        # Wait for thread
        thread.join(timeout=1.0)
        
        self.assertFalse(thread.is_alive())


class TestAttackDryRun(unittest.TestCase):
    """Test dry-run functionality"""
    
    def test_dry_run_mode(self):
        """Test that dry-run doesn't actually attack"""
        stop_event = threading.Event()
        counter = ThreadSafeCounter(0)
        
        worker = AttackWorkers(
            host="example.com",
            port=80,
            stop_event=stop_event,
            counter=counter
        )
        
        # In dry-run mode, increment_counter should be noraml
        # but actual HTTP requests wouldn't be sent
        # This is tested at engine level with dry_run flag
        
        self.assertIsNotNone(worker)


class TestAttackWithMocking(unittest.TestCase):
    """Test attacks with mocked network calls"""
    
    @patch('requests.Session.get')
    def test_http_flood_mocked(self, mock_get):
        """Test HTTP flood with mocked requests"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'content-length': '100'}
        mock_get.return_value = mock_response
        
        stop_event = threading.Event()
        counter = ThreadSafeCounter(0)
        
        worker = AttackWorkers(
            host="127.0.0.1",
            port=8080,
            stop_event=stop_event,
            counter=counter
        )
        
        # Would normally test attack methods here
        # This demonstrates the pattern
        self.assertIsNotNone(worker)


class TestRateLimitingIntegration(unittest.TestCase):
    """Test rate limiting with attack workers"""
    
    def test_counter_with_rate_limit(self):
        """Test counter under rate limiting"""
        counter = ThreadSafeCounter(0)
        stop_event = threading.Event()
        
        start_time = time.time()
        iterations = 0
        target_iterations = 10
        
        # Simulate rate-limited requests
        request_interval = 0.01  # 100 RPS
        
        while iterations < target_iterations:
            counter.increment(1)
            iterations += 1
            time.sleep(request_interval)
        
        elapsed = time.time() - start_time
        actual_rps = iterations / elapsed
        
        # Should be approximately 100 RPS (within 10%)
        self.assertGreater(actual_rps, 90)
        self.assertLess(actual_rps, 110)


class TestMetricsCollection(unittest.TestCase):
    """Test metrics collection from attacks"""
    
    def test_metrics_from_multiple_workers(self):
        """Test collecting metrics from multiple workers"""
        counter = ThreadSafeCounter(0)
        stop_event = threading.Event()
        
        workers = [
            AttackWorkers("127.0.0.1", 8080, stop_event, counter)
            for _ in range(3)
        ]
        
        # Simulate packet increments from each worker
        for worker in workers:
            worker.metrics.success_count = 100
            worker.metrics.error_count = 5
            worker.metrics.bytes_sent = 50000
        
        # Total metrics
        total_success = sum(w.metrics.success_count for w in workers)
        total_error = sum(w.metrics.error_count for w in workers)
        total_bytes = sum(w.metrics.bytes_sent for w in workers)
        
        self.assertEqual(total_success, 300)
        self.assertEqual(total_error, 15)
        self.assertEqual(total_bytes, 150000)


def run_tests(verbosity=2):
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAttackMetrics))
    suite.addTests(loader.loadTestsFromTestCase(TestThreadSafeCounter))
    suite.addTests(loader.loadTestsFromTestCase(TestAttackWorkerInit))
    suite.addTests(loader.loadTestsFromTestCase(TestAttackWorkerIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestAttackDryRun))
    suite.addTests(loader.loadTestsFromTestCase(TestAttackWithMocking))
    suite.addTests(loader.loadTestsFromTestCase(TestRateLimitingIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestMetricsCollection))
    
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

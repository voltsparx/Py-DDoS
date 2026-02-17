"""
Structured JSON Logging for Py-DDoS
Provides machine-readable event logging for integration with log aggregation systems

Outputs structured JSON events with timestamp, level, context, and metrics.

Author: voltsparx
Contact: voltsparx@gmail.com
"""

import json
import time
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime


class StructuredJSONLogger:
    """
    Structured JSON event logger for logs, metrics, and diagnostics
    
    Outputs JSON objects suitable for Elasticsearch, Splunk, DataDog, etc.
    
    Attributes:
        log_dir: Directory for JSON log files
        event_log_file: Path to event log file
        metrics_log_file: Path to metrics log file
    """
    
    def __init__(self, log_dir: str = "logs"):
        """
        Initialize structured JSON logger
        
        Args:
            log_dir: Directory for log files (default: "logs")
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.event_log_file = self.log_dir / f"events_{timestamp}.jsonl"
        self.metrics_log_file = self.log_dir / f"metrics_{timestamp}.jsonl"
        
        # Standard Python logger for backup
        self.logger = logging.getLogger("py-ddos")
        self.logger.setLevel(logging.DEBUG)
    
    def log_event(
        self,
        event_type: str,
        level: str = "INFO",
        message: str = "",
        context: Optional[Dict[str, Any]] = None,
        tags: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Log structured event
        
        Args:
            event_type: Event type (attack_start, request_sent, error, etc.)
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            message: Human-readable message
            context: Event context data
            tags: Key-value tags for filtering
        """
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'level': level,
            'message': message,
            'context': context or {},
            'tags': tags or {},
            'version': '1.0'
        }
        
        self._write_json(self.event_log_file, event)
    
    def log_metric(
        self,
        metric_name: str,
        value: float,
        unit: str = "",
        context: Optional[Dict[str, Any]] = None,
        tags: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Log structured metric
        
        Args:
            metric_name: Metric name (requests_per_second, response_time_ms, etc.)
            value: Metric value
            unit: Unit (rps, ms, bytes, %, etc.)
            context: Metric context
            tags: Classification tags
        """
        metric = {
            'timestamp': datetime.utcnow().isoformat(),
            'metric_name': metric_name,
            'value': value,
            'unit': unit,
            'context': context or {},
            'tags': tags or {}
        }
        
        self._write_json(self.metrics_log_file, metric)
    
    def log_attack_start(
        self,
        attack_type: str,
        target_host: str,
        target_port: int,
        threads: int,
        duration: float,
        config: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log attack start event"""
        self.log_event(
            event_type='attack_start',
            level='INFO',
            message=f'Starting {attack_type} attack on {target_host}:{target_port}',
            context={
                'attack_type': attack_type,
                'target_host': target_host,
                'target_port': target_port,
                'threads': threads,
                'duration': duration,
                'config': config or {}
            },
            tags={'operation': 'attack', 'phase': 'init'}
        )
    
    def log_attack_complete(
        self,
        attack_type: str,
        total_requests: int,
        successful: int,
        failed: int,
        duration: float,
        avg_rps: float,
        peak_rps: float
    ) -> None:
        """Log attack completion event"""
        success_rate = (successful / max(total_requests, 1)) * 100
        
        self.log_event(
            event_type='attack_complete',
            level='INFO',
            message=f'{attack_type} attack completed: {successful}/{total_requests} successful',
            context={
                'attack_type': attack_type,
                'total_requests': total_requests,
                'successful': successful,
                'failed': failed,
                'success_rate': success_rate,
                'duration': duration,
                'avg_rps': avg_rps,
                'peak_rps': peak_rps
            },
            tags={'operation': 'attack', 'phase': 'complete'}
        )
    
    def log_error(
        self,
        error_type: str,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        fatal: bool = False
    ) -> None:
        """Log error event"""
        level = 'CRITICAL' if fatal else 'ERROR'
        
        self.log_event(
            event_type='error',
            level=level,
            message=message,
            context={
                'error_type': error_type,
                'fatal': fatal,
                'details': context or {}
            },
            tags={'severity': 'error', 'fatal': 'yes' if fatal else 'no'}
        )
    
    def log_performance_snapshot(
        self,
        packets_sent: int,
        success_count: int,
        error_count: int,
        current_rps: float,
        avg_response_time_ms: float,
        memory_usage_mb: Optional[float] = None,
        cpu_usage_percent: Optional[float] = None
    ) -> None:
        """Log performance metrics snapshot"""
        self.log_event(
            event_type='performance_snapshot',
            level='INFO',
            message='Performance snapshot',
            context={
                'packets_sent': packets_sent,
                'success_count': success_count,
                'error_count': error_count,
                'current_rps': current_rps,
                'avg_response_time_ms': avg_response_time_ms,
                'memory_usage_mb': memory_usage_mb,
                'cpu_usage_percent': cpu_usage_percent
            },
            tags={'type': 'performance', 'phase': 'running'}
        )
    
    def log_rate_limit_event(
        self,
        reason: str,
        global_rps_limit: Optional[float] = None,
        per_thread_rps_limit: Optional[float] = None,
        current_rps: Optional[float] = None
    ) -> None:
        """Log rate limiting event"""
        self.log_event(
            event_type='rate_limit_triggered',
            level='INFO',
            message=f'Rate limiting active: {reason}',
            context={
                'reason': reason,
                'global_rps_limit': global_rps_limit,
                'per_thread_rps_limit': per_thread_rps_limit,
                'current_rps': current_rps
            },
            tags={'type': 'rate_limiting'}
        )
    
    def log_warmup_phase(
        self,
        phase: str,  # 'start', 'progress', 'complete'
        requests_sent: int,
        target_requests: int,
        avg_response_time_ms: float
    ) -> None:
        """Log target warm-up phase"""
        self.log_event(
            event_type='warmup_phase',
            level='INFO',
            message=f'Warm-up phase {phase}: {requests_sent}/{target_requests} requests',
            context={
                'phase': phase,
                'requests_sent': requests_sent,
                'target_requests': target_requests,
                'avg_response_time_ms': avg_response_time_ms
            },
            tags={'type': 'warmup', 'phase': phase}
        )
    
    def log_adaptive_control(
        self,
        action: str,  # 'increase', 'decrease', 'maintain'
        reason: str,
        old_threads: int,
        new_threads: int,
        old_rps: float,
        new_rps: float,
        trigger_metric: str,
        trigger_value: float
    ) -> None:
        """Log adaptive load control adjustment"""
        self.log_event(
            event_type='adaptive_control',
            level='INFO',
            message=f'Adaptive control: {action} load due to {reason}',
            context={
                'action': action,
                'reason': reason,
                'old_threads': old_threads,
                'new_threads': new_threads,
                'old_rps': old_rps,
                'new_rps': new_rps,
                'trigger_metric': trigger_metric,
                'trigger_value': trigger_value
            },
            tags={'type': 'adaptive', 'action': action}
        )
    
    def _write_json(self, filepath: Path, event: Dict[str, Any]) -> None:
        """Write JSON event to file (JSONL format)"""
        try:
            with open(filepath, 'a') as f:
                f.write(json.dumps(event) + '\n')
        except Exception as e:
            self.logger.error(f"Failed to write JSON log: {e}")
    
    def export_events(self, output_file: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Export all events as JSON array
        
        Args:
            output_file: Optional file to save export
        
        Returns:
            List of event dictionaries
        """
        events = []
        
        if self.event_log_file.exists():
            with open(self.event_log_file, 'r') as f:
                for line in f:
                    if line.strip():
                        try:
                            events.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(events, f, indent=2)
        
        return events
    
    def get_log_files(self) -> Dict[str, str]:
        """Get paths to log files"""
        return {
            'events': str(self.event_log_file),
            'metrics': str(self.metrics_log_file)
        }


__all__ = ['StructuredJSONLogger']

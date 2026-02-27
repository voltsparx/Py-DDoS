"""
Safety Locks System - Multi-layer protections for authorized testing
Prevents accidental misuse with thorough validation, audit trails, and granular controls

Author: voltsparx
Contact: voltsparx@gmail.com

Features:
- Multi-layer authorization checks
- Granular lock controls (disable individual checks)
- Resource usage predictions
- Audit trail logging
- Rate limiting suggestions
- Risk assessment warnings
"""

import sys
import datetime
import json
import os
from pathlib import Path
from ..ui.colors import Styles, Colors


class SafetyLocks:
    """Multi-layer safety protections with audit trails and risk assessment"""
    
    def __init__(self, audit_log_dir='logs'):
        self.locks_enabled = True
        self.warn_only = False  # when True, locks warn but never block
        self.audit_log_dir = Path(audit_log_dir)
        self.audit_log_dir.mkdir(exist_ok=True)
        
        # Granular lock controls
        self.lock_status = {
            'high_thread_warning': True,
            'long_duration_warning': True,
            'external_network_warning': True,
            'tor_anonymity_warning': True,
            'no_local_target_warning': True,
            'bandwidth_estimation': True,
            'resource_impact_warning': True,
            'authorization_verification': True,
        }
        
        # Risk thresholds
        self.thresholds = {
            'thread_warning': 500,
            'thread_critical': 2000,
            'duration_warning': 600,  # 10 minutes
            'duration_critical': 3600,  # 1 hour
            'bandwidth_warning': 1000,  # MB/s estimate
            'rps_warning': 100000,  # requests per second
        }
        
        # Audit trail
        self.audit_trail = []
    
    def _estimate_bandwidth(self, threads, rps, payload_size=1024):
        """Estimate bandwidth consumption"""
        return (rps * payload_size) / (1024 * 1024)  # MB/s
    
    def _estimate_cpu_impact(self, threads):
        """Estimate CPU usage percentage"""
        import multiprocessing
        cpu_count = multiprocessing.cpu_count()
        return min(100, (threads / cpu_count) * 25)  # Rough estimate
    
    def _estimate_memory_impact(self, threads):
        """Estimate memory usage (MB)"""
        return (threads * 2)  # ~2MB per thread estimate
    
    def _log_audit(self, action, details, status):
        """Log action to audit trail"""
        timestamp = datetime.datetime.now().isoformat()
        entry = {
            'timestamp': timestamp,
            'action': action,
            'details': details,
            'status': status
        }
        self.audit_trail.append(entry)
    
    def _save_audit_trail(self, filename='safety_audit.json'):
        """Save audit trail to file"""
        filepath = self.audit_log_dir / filename
        with open(filepath, 'w') as f:
            json.dump(self.audit_trail, f, indent=2)
    
    def check_high_thread_count(self, threads, payload_size=1024, auto_confirm=False):
        """Thread count validation with resource estimation"""
        if self.warn_only:
            # always log and permit
            self._log_audit('thread_check', {'threads': threads, 'risk': 'WARN_ONLY'}, True)
            return True
        if not self.locks_enabled or not self.lock_status['high_thread_warning']:
            return True
        
        cpu_impact = self._estimate_cpu_impact(threads)
        mem_impact = self._estimate_memory_impact(threads)
        
        risk_level = "LOW"
        if threads > self.thresholds['thread_critical']:
            risk_level = "CRITICAL"
        elif threads > self.thresholds['thread_warning']:
            risk_level = "HIGH"
        
        if threads > self.thresholds['thread_warning']:
            print()
            print(Styles.warning(f"[{risk_level}] SAFETY LOCK: High thread count"))
            print(Styles.info(f"  Threads: {threads:,}"))
            print(Styles.info(f"  Est. Memory Impact: ~{mem_impact:.1f}MB"))
            print(Styles.info(f"  Est. CPU Usage: ~{cpu_impact:.1f}%"))
            
            if risk_level == "CRITICAL":
                print(Styles.danger("  WARNING: This may severely impact your system!"))
            
            if auto_confirm:
                print(Styles.warning("  [AUTO MODE] Proceeding without confirmation"))
                self._log_audit('thread_check', {'threads': threads, 'risk': risk_level}, True)
                return True
            
            print()
            response = input(Styles.prompt(f"Continue? (yes/no): ")).strip().lower()
            print()
            
            self._log_audit('thread_check', {'threads': threads, 'risk': risk_level}, response in ['yes', 'y'])
            return response in ['yes', 'y']
        
        self._log_audit('thread_check', {'threads': threads, 'risk': 'SAFE'}, True)
        return True
    
    def check_long_duration(self, duration):
        """Duration validation with time estimation"""
        if self.warn_only:
            self._log_audit('duration_check', {'duration': duration, 'risk': 'WARN_ONLY'}, True)
            return True
        if not self.locks_enabled or not self.lock_status['long_duration_warning']:
            return True
        
        risk_level = "LOW"
        if duration > self.thresholds['duration_critical']:
            risk_level = "CRITICAL"
        elif duration > self.thresholds['duration_warning']:
            risk_level = "HIGH"
        
        if duration > self.thresholds['duration_warning']:
            mins, secs = divmod(duration, 60)
            print()
            print(Styles.warning(f"[{risk_level}] SAFETY LOCK: Extended attack duration"))
            print(Styles.info(f"  Duration: {duration}s ({int(mins)}m {secs}s)"))
            print(Styles.info(f"  Long-running tests may trigger network detection systems"))
            
            if risk_level == "CRITICAL":
                print(Styles.danger("  WARNING: This duration likely exceeds authorized testing scope!"))
            
            print()
            response = input(Styles.prompt(f"Continue? (yes/no): ")).strip().lower()
            print()
            
            self._log_audit('duration_check', {'duration': duration, 'risk': risk_level}, response in ['yes', 'y'])
            return response in ['yes', 'y']
        
        self._log_audit('duration_check', {'duration': duration, 'risk': 'SAFE'}, True)
        return True
    
    def check_external_target(self, target_ip):
        """External target validation with jurisdiction checks"""
        if self.warn_only:
            self._log_audit('external_target_check', {'target': target_ip, 'warn_only': True}, True)
            return True
        if not self.locks_enabled or not self.lock_status['external_network_warning']:
            return True
        
        # Check if target is not local
        local_ranges = ['127.', '192.168.', '10.', '172.1', '169.254', 'localhost']
        is_local = any(target_ip.startswith(r) if isinstance(r, str) and r != 'localhost' else target_ip == r 
                      for r in local_ranges)
        
        if not is_local:
            print()
            print(Styles.danger("SAFETY LOCK: External target authorization check"))
            print(Styles.info(f"  Target: {target_ip}"))
            print(Styles.warning("  AUTHORIZATION REQUIREMENTS:"))
            print(Styles.warning("    1. Do you have WRITTEN AUTHORIZATION from system owner?"))
            print(Styles.warning("    2. Is this authorized by your organization?"))
            print(Styles.warning("    3. Are you complying with all applicable laws?"))
            print(Styles.warning("    4. Do you have documentation of this authorization?"))
            print()
            
            response = input(Styles.prompt("Confirm written authorization exists (yes/no): ")).strip().lower()
            print()
            
            if response in ['yes', 'y']:
                # Double-check for high-risk jurisdictions
                print(Styles.info("Unauthorized testing could violate laws in:"))
                print(Styles.info("  • United States: Computer Fraud and Abuse Act (CFAA)"))
                print(Styles.info("  • UK: Computer Misuse Act 1990"))
                print(Styles.info("  • EU: ePrivacy Directive"))
                print(Styles.info("  • Most other countries have similar laws"))
                print()
                response2 = input(Styles.prompt("Confirm compliance with local laws (yes/no): ")).strip().lower()
                print()
                
                self._log_audit('external_target_check', {'target': target_ip, 'authorized': True}, 
                              response2 in ['yes', 'y'])
                return response2 in ['yes', 'y']
            
            self._log_audit('external_target_check', {'target': target_ip, 'authorized': False}, False)
            return False
        
        self._log_audit('external_target_check', {'target': target_ip, 'type': 'local'}, True)
        return True
    
    def check_tor_enabled(self):
        """TOR security implications check"""
        if self.warn_only:
            # in warn-only mode we log and allow
            self._log_audit('tor_check', {'enabled': True, 'risk': 'WARN_ONLY'}, True)
            return True
        if not self.locks_enabled or not self.lock_status['tor_anonymity_warning']:
            return True
        
        print()
        print(Styles.warning("SAFETY LOCK: TOR anonymity layer enabled"))
        print(Styles.info("  TOR SECURITY IMPLICATIONS:"))
        print(Styles.info("    • TOR relays log network metadata"))
        print(Styles.info("    • Exit node operators see TOR connection patterns"))
        print(Styles.info("    • Exit node operators see cleartext traffic"))
        print(Styles.info("    • ISP may throttle or block TOR traffic"))
        print()
        print(Styles.warning("  AUTHORIZATION SCOPE:"))
        print(Styles.info("    • Ensure TOR usage is within authorized testing scope"))
        print(Styles.info("    • TOR may not be allowed in some corporate environments"))
        print(Styles.info("    • Document TOR usage in your testing records"))
        print()
        
        response = input(Styles.prompt("Understand TOR implications and confirm? (yes/no): ")).strip().lower()
        print()
        
        self._log_audit('tor_check', {'enabled': True}, response in ['yes', 'y'])
        return response in ['yes', 'y']
    
    def check_all(self, config, auto_confirm=False):
        """Run all applicable safety checks with optional auto-confirmation for scripts

        When :pyattr:`warn_only` is enabled the individual checks will still log
        warnings but they will always return ``True`` so the attack is not
        blocked.  This is useful for educational demonstrations where you want
        the safety messages without requiring explicit confirmation.
        """
        checks = [
            ('threads', self.check_high_thread_count),
            ('duration', self.check_long_duration),
            ('target_host', self.check_external_target),
        ]
        
        for key, check_func in checks:
            if key in config:
                # Pass auto_confirm flag for checks that support it
                if key == 'threads':
                    if not check_func(config[key], auto_confirm=auto_confirm):
                        return False
                else:
                    if not check_func(config[key]):
                        return False
        
        if config.get('use_tor', False):
            if not self.check_tor_enabled():
                return False
        
        return True
    
    def disable_locks(self):
        """Disable all safety locks - requires acknowledgment"""
        print()
        print(Styles.danger("DISABLING SAFETY LOCKS"))
        print(Styles.warning("Without safety locks, this tool will NOT ask for confirmations"))
        print(Styles.warning("Ensure you understand the risks and have full authorization"))
        print()
        response = input(Styles.prompt("Type 'disable' to confirm: ")).strip().lower()
        
        if response == 'disable':
            self.locks_enabled = False
            print(Styles.success("Safety locks disabled"))
            return True
        else:
            print(Styles.info("Safety locks remain enabled"))
            return False
    
    def disable_specific_lock(self, lock_name):
        """Disable a specific safety lock"""
        if lock_name in self.lock_status:
            self.lock_status[lock_name] = False
            return True
        return False
    
    def enable_specific_lock(self, lock_name):
        """Enable a specific safety lock"""
        if lock_name in self.lock_status:
            self.lock_status[lock_name] = True
            return True
        return False
    
    def get_status(self):
        """Detailed safety locks status report"""
        print()
        print(Styles.section("SAFETY LOCKS STATUS"))
        print()
        
        overall_status = "ENABLED" if self.locks_enabled else "DISABLED"
        color = Styles.success if self.locks_enabled else Styles.danger
        print(color(f"  Overall Status: {overall_status}"))
        print()
        
        for lock_name, enabled in self.lock_status.items():
            status = "✓ ON" if enabled else "✗ OFF"
            color_func = Styles.success if enabled else Styles.warning
            print(color_func(f"    {lock_name:.<50} {status}"))
        
        print()
        print(Styles.section("RESOURCE THRESHOLDS"))
        print()
        for threshold_name, value in self.thresholds.items():
            print(Styles.info(f"  {threshold_name:.<50} {value}"))
        
        print()
    
    def print_risk_assessment(self, config):
        """Print comprehensive risk assessment before execution"""
        print()
        print(Styles.section("RISK ASSESSMENT REPORT"))
        print()
        
        risks = []
        
        # Thread risk
        threads = config.get('threads', 100)
        if threads > self.thresholds['thread_critical']:
            risks.append(('CRITICAL', f"Threads ({threads}) exceed critical threshold"))
        elif threads > self.thresholds['thread_warning']:
            risks.append(('HIGH', f"Threads ({threads}) exceed warning threshold"))
        
        # Duration risk
        duration = config.get('duration', 60)
        if duration > self.thresholds['duration_critical']:
            risks.append(('CRITICAL', f"Duration ({duration}s) exceeds critical threshold"))
        elif duration > self.thresholds['duration_warning']:
            risks.append(('HIGH', f"Duration ({duration}s) exceeds warning threshold"))
        
        # External target risk
        target = config.get('target_host', 'localhost')
        local_ranges = ['127.', '192.168.', '10.', '172.1']
        is_local = any(target.startswith(r) for r in local_ranges) or target == 'localhost'
        if not is_local:
            risks.append(('CRITICAL', f"External target ({target}) - Authorization required"))
        
        # TOR risk
        if config.get('use_tor', False):
            risks.append(('HIGH', "TOR anonymity layer increases forensic footprint"))
        
        if not risks:
            print(Styles.success("  No significant risks detected"))
        else:
            print(Styles.warning(f"  {len(risks)} risk(s) identified:"))
            print()
            for risk_level, description in risks:
                if risk_level == 'CRITICAL':
                    print(Styles.danger(f"    [CRITICAL] {description}"))
                else:
                    print(Styles.warning(f"    [{risk_level}] {description}"))
        
        print()
        
        self._log_audit('risk_assessment', {'config': config, 'risks_found': len(risks)}, True)
        
        overall_status = "ENABLED" if self.locks_enabled else "DISABLED"
        color = Styles.success if self.locks_enabled else Styles.danger
        print(f"Overall: {color(overall_status)}")
        print()
        
        for lock_name, status in self.lock_status.items():
            status_str = "ENABLED" if status else "DISABLED"
            color = Styles.success if status else Styles.warning
            print(f"  {lock_name}: {color(status_str)}")
        print()

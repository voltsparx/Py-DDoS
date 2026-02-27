"""
Configuration module for RedLoad-X
Handles all configuration and settings
"""

from pathlib import Path
import json
from ..ui.colors import Styles

class Config:
    """Configuration manager for RedLoad-X"""
    
    DEFAULT_CONFIG = {
        'target_host': '',
        'target_port': 80,
        'attack_type': 'HTTP',
        'threads': 100,
        'duration': 60,
        'use_tor': False,
        'timeout': 5,
        'verify_ssl': False,
        'request_rate': 0,  # 0 = unlimited
        'payload_size': 1024,
        'authorized': False,
        'authorized_external': False,
    }
    
    ATTACK_TYPES = {
        '1': {
            'name': 'HTTP',
            'description': 'Layer 7 HTTP GET/POST Flood',
            'requires_root': False,
            'bandwidth_intensive': True,
            'stealth': False
        },
        '2': {
            'name': 'SLOWLORIS',
            'description': 'Slow client connections - Resource exhaustion',
            'requires_root': False,
            'bandwidth_intensive': False,
            'stealth': True
        },
        '3': {
            'name': 'UDP',
            'description': 'Layer 4 UDP Flood',
            'requires_root': False,
            'bandwidth_intensive': True,
            'stealth': False
        },
        '4': {
            'name': 'SYN',
            'description': 'TCP SYN Flood (Raw sockets)',
            'requires_root': True,
            'bandwidth_intensive': True,
            'stealth': False
        },
        '5': {
            'name': 'SLOWREAD',
            'description': 'Slow read attacks - Keep connections open',
            'requires_root': False,
            'bandwidth_intensive': False,
            'stealth': True
        },
        '6': {
            'name': 'DNS',
            'description': 'DNS amplification attack',
            'requires_root': False,
            'bandwidth_intensive': True,
            'stealth': False
        },
        '7': {
            'name': 'ICMP',
            'description': 'ICMP Flood (Ping flood)',
            'requires_root': True,
            'bandwidth_intensive': True,
            'stealth': False
        },
        '8': {
            'name': 'NTP',
            'description': 'NTP amplification attack',
            'requires_root': False,
            'bandwidth_intensive': True,
            'stealth': False
        },
    }
    
    @staticmethod
    def print_disclaimer():
        """Print important legal disclaimer"""
        print(Styles.warning("LEGAL DISCLAIMER"))
        print()
        print("This tool is provided for EDUCATIONAL and AUTHORIZED SECURITY TESTING only.")
        print("Unauthorized access to computer systems is ILLEGAL under laws such as:")
        print("  - Computer Fraud and Abuse Act (CFAA) in the United States")
        print("  - Computer Misuse Act in the United Kingdom")
        print("  - Similar laws in virtually all countries")
        print()
        print("You are responsible for ensuring you have explicit authorization to test")
        print("the target systems. Misuse of this tool may result in:")
        print("  - Criminal prosecution")
        print("  - Civil liability")
        print("  - Imprisonment")
        print("  - Substantial fines")
        print()
        print(Styles.warning("Use only on systems you own or have written permission to test."))
        print()
    
    @staticmethod
    def print_educational_note():
        """Print educational context"""
        print(Styles.info("EDUCATIONAL CONTEXT"))
        print()
        print("This tool demonstrates how DDoS attacks work for learning purposes:")
        print("  - Network security concepts")
        print("  - Attack detection and mitigation")
        print("  - Infrastructure resilience")
        print("  - Security testing methodologies")
        print()
        print("Understanding attacks helps develop better defenses.")
        print()
    
    @staticmethod
    def load_config(config_file: str = None):
        """Load configuration from file"""
        if config_file and Path(config_file).exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(Styles.warning(f"Failed to load config: {e}"))
        return Config.DEFAULT_CONFIG.copy()
    
    @staticmethod
    def save_config(config: dict, config_file: str):
        """Save configuration to file"""
        try:
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            print(Styles.success(f"Config saved to {config_file}"))
        except Exception as e:
            print(Styles.error(f"Failed to save config: {e}"))
    
    @staticmethod
    def get_attack_info(attack_type: str) -> dict:
        """Get information about an attack type"""
        for key, value in Config.ATTACK_TYPES.items():
            if value['name'] == attack_type:
                return value
        return None

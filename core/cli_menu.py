"""
Interactive CLI Menu System for Py-DDoS
Provides user-friendly interface with colored output
"""

import socket
from .colors import Styles, Colors
from .config import Config
from .metadata import (
    PROJECT_NAME,
    VERSION,
    PROJECT_DESCRIPTION,
    AUTHOR,
    CONTACT,
    LICENSE,
    get_banner,
)


def validate_ip_or_domain(target: str) -> tuple:
    """Validate and resolve IP or domain"""
    try:
        # Try to resolve as domain
        ip = socket.gethostbyname(target)
        return True, ip, target
    except socket.gaierror:
        # Check if it's already an IP
        try:
            socket.inet_aton(target)
            return True, target, target
        except socket.error:
            return False, None, target


def print_banner():
    """Print colored banner with metadata"""
    banner = f"""{Colors.BRIGHT_CYAN}{get_banner()}{Colors.RESET}"""
    print(banner)


def interactive_menu(is_root: bool) -> dict:
    """Interactive CLI menu for attack configuration"""
    
    print_banner()
    
    # Disclaimer
    Config.print_disclaimer()
    print()
    Config.print_educational_note()
    print()
    
    config = Config.DEFAULT_CONFIG.copy()
    
    # Target selection
    print(Styles.section("TARGET CONFIGURATION"))
    while True:
        target = input(Styles.info("Enter target IP or hostname") + ": ").strip()
        valid, ip, domain = validate_ip_or_domain(target)
        if valid:
            config['target_host'] = ip
            config['target_input'] = domain
            print(Styles.success(f"Target resolved: {domain} -> {ip}"))
            break
        else:
            print(Styles.error("Invalid IP or hostname. Please try again."))
    
    # Port selection
    while True:
        try:
            port = int(input(Styles.info("Enter target port (default: 80)") + ": ").strip() or "80")
            if 1 <= port <= 65535:
                config['target_port'] = port
                print(Styles.success(f"Port set to: {port}"))
                break
            else:
                print(Styles.error("Port must be between 1 and 65535"))
        except ValueError:
            print(Styles.error("Invalid port number"))
    
    # Attack type selection
    print()
    print(Styles.section("ATTACK VECTOR SELECTION"))
    print()
    
    for key, attack in Config.ATTACK_TYPES.items():
        req_root = " (requires root)" if attack['requires_root'] and not is_root else ""
        status = Colors.BRIGHT_RED + " [ROOT REQUIRED]" + Colors.RESET if attack['requires_root'] and not is_root else ""
        print(Styles.option(key, attack['name'], attack['description']) + status)
    
    print()
    while True:
        choice = input(Styles.info("Select attack type") + " [1-8]: ").strip()
        if choice in Config.ATTACK_TYPES:
            attack_info = Config.ATTACK_TYPES[choice]
            if attack_info['requires_root'] and not is_root:
                print(Styles.warning(f"{attack_info['name']} requires root/admin privileges"))
                continue
            config['attack_type'] = attack_info['name']
            print(Styles.success(f"Attack type selected: {attack_info['name']}"))
            print(Styles.info(f"Type: {attack_info['description']}"))
            break
        else:
            print(Styles.error("Invalid selection"))
    
    # Thread count
    print()
    print(Styles.section("PERFORMANCE SETTINGS"))
    while True:
        try:
            threads = int(input(Styles.info("Number of threads (default: 100, recommended: 50-500)") + ": ").strip() or "100")
            if 1 <= threads <= 10000:
                config['threads'] = threads
                print(Styles.success(f"Threads set to: {threads}"))
                break
            else:
                print(Styles.error("Threads must be between 1 and 10000"))
        except ValueError:
            print(Styles.error("Invalid number"))
    
    # Duration
    while True:
        try:
            duration = int(input(Styles.info("Attack duration in seconds (default: 60)") + ": ").strip() or "60")
            if 1 <= duration <= 3600:
                config['duration'] = duration
                print(Styles.success(f"Duration set to: {duration} seconds"))
                break
            else:
                print(Styles.error("Duration must be between 1 and 3600 seconds"))
        except ValueError:
            print(Styles.error("Invalid duration"))
    
    # TOR option
    print()
    tor_choice = input(Styles.info("Enable TOR anonymity layer? (y/n)") + ": ").strip().lower()
    if tor_choice in ['y', 'yes']:
        config['use_tor'] = True
        print(Styles.warning("TOR mode enabled - Requires TOR daemon running on port 9051"))
    else:
        config['use_tor'] = False
        print(Styles.info("TOR mode disabled"))
    
    # Summary
    print()
    print(Styles.section("ATTACK SUMMARY"))
    print()
    print(Styles.table_row("Target", f"{config['target_input']} ({config['target_host']})"))
    print(Styles.table_row("Port", str(config['target_port'])))
    print(Styles.table_row("Attack Type", config['attack_type']))
    print(Styles.table_row("Threads", str(config['threads'])))
    print(Styles.table_row("Duration", f"{config['duration']} seconds"))
    print(Styles.table_row("TOR Enabled", "Yes" if config['use_tor'] else "No"))
    print()
    
    # Confirmation
    confirm = input(Styles.warning("Confirm attack parameters? (yes/no)") + ": ").strip().lower()
    if confirm not in ['yes', 'y']:
        print(Styles.error("Attack cancelled"))
        return None
    
    print()
    print(Styles.success("Configuration complete. Starting attack..."))
    print()
    
    return config

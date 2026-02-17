#!/usr/bin/env python3
"""
Py-DDoS v7.5 - Operational Network Stress Testing Tool
For Educational and Authorized Penetration Testing Only

Author: voltsparx
Contact: voltsparx@gmail.com

IMPORTANT: This tool includes built-in safety locks by default to prevent
accidental misuse. Safety locks require confirmation before executing potentially
high-impact network stress tests. Safety locks can be disabled during configuration.

Usage:
    Interactive mode:
        python3 py-ddos.py
    
    Command-line mode:
        python3 py-ddos.py -t target.com -p 80 -a HTTP -d 60 -c 100
        python3 py-ddos.py --target 192.168.1.1 --port 8080 --attack SLOWLORIS --duration 120

LEGAL DISCLAIMER:
    This tool is for AUTHORIZED OPERATIONAL TESTING and EDUCATIONAL purposes only.
    Unauthorized network stress testing is ILLEGAL in most jurisdictions.
    The author assumes no liability for misuse of this tool.

SAFETY FEATURES:
    - Built-in safety locks enabled by default
    - Confirmation prompts for high-impact configurations
    - Educational notes for learning purposes
    - Full audit logging of all activities
    - Can be disabled only with explicit user confirmation
"""

import sys
import os
import argparse
import signal

# Add core directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.colors import Styles, Colors
from core.config import Config
from core.cli_menu import interactive_menu, print_banner
from core.engine import PyDDoS
from core.safety_locks import SafetyLocks
from core.metadata import VERSION, PROJECT_NAME, AUTHOR, CONTACT


def create_parser():
    """Create command-line argument parser with educational help"""
    
    # Custom help text with educational notes
    help_text = """
Py-DDoS v7.0 - Operational Network Stress Testing Tool

Author: voltsparx | Contact: voltsparx@gmail.com

This tool is designed for:
  - Learning about network resilience and stress testing
  - Authorized penetration testing and validation
  - Security research in controlled environments
  - Testing incident response procedures
  - Infrastructure capacity planning

EDUCATIONAL FOCUS:
  Each network stress test demonstrates a different testing vector:
  - HTTP: Application-layer volumetric stress tests
  - SLOWLORIS: Resource exhaustion via slow clients
  - UDP: Network-layer stress testing
  - SYN: TCP connection exhaustion scenarios
  - SLOWREAD: Slow data transmission testing
  - DNS: Amplification test scenarios
  - ICMP: Network monitoring protocol testing
  - NTP: Reflected amplification scenarios

SAFETY FEATURES:
  - Safety locks enabled by default
  - Confirmation prompts for high-resource tests
  - External target warning system
  - TOR usage acknowledgment prompts
  - Complete audit logging
  - Ctrl+C interrupt support during tests

"""
    
    parser = argparse.ArgumentParser(
        prog='py-ddos',
        description=help_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
    parser.add_argument('--test-aiohttp-errors', action='store_true', help='Run aiohttp error handling test suite (developer only)')
    parser.add_argument('--about', action='store_true', help='Show information about this tool, attacks, credits, and disclaimers')
EXAMPLES:
  # Interactive mode with safety locks
  python3 py-ddos.py
  
  # HTTP flood attack
  python3 py-ddos.py -t example.com -p 80 -a HTTP -d 60 -c 100
  
  # Slowloris attack with TOR (requires confirmation)
  python3 py-ddos.py -t 192.168.1.1 -p 8080 -a SLOWLORIS -d 120 --tor
  
  # UDP flood with many threads
  python3 py-ddos.py --target example.com --attack UDP --duration 300 --threads 500
  
  # List all available attacks
  python3 py-ddos.py -l

EDUCATIONAL NOTES:
  Understanding DDoS attacks is crucial for:
  1. Network defense and mitigation strategies
  2. Incident response and detection
  3. Infrastructure capacity planning
  4. Security testing methodologies
  
  Each attack type reveals different vulnerabilities:
  - Application layer (L7): HTTP, SLOWLORIS, SLOWREAD
  - Transport layer (L4): UDP, SYN, DNS, NTP
  - Network layer (L3): ICMP
  
  Defending against these requires:
  - Rate limiting and throttling
  - Geographic distribution
  - Anycast network routing
  - Advanced filtering and monitoring

LEGAL NOTICE:
  Using this tool against systems without explicit written authorization is ILLEGAL
  and may result in criminal prosecution. Ensure you have:
  1. Written permission from the system owner
  2. Documented scope and authorized test window
  3. Legal compliance in your jurisdiction
  4. Proper incident response procedures

Author: voltsparx | Contact: voltsparx@gmail.com
        """
    )
    
    # Target options
    parser.add_argument('-t', '--target', dest='target', 
                       help='Target IP address or hostname')
    parser.add_argument('-p', '--port', dest='port', type=int, default=80, 
                       help='Target port (default: 80)')
    
    # Attack options
    parser.add_argument('-a', '--attack', dest='attack_type',
                       choices=['HTTP', 'SLOWLORIS', 'UDP', 'SYN', 'SLOWREAD', 'DNS', 'ICMP', 'NTP'],
                       help='Attack type (see --help for educational notes)')
    parser.add_argument('-d', '--duration', dest='duration', type=int, default=60,
                       help='Attack duration in seconds (default: 60)')
    parser.add_argument('-c', '--threads', dest='threads', type=int, default=100,
                       help='Number of worker threads (default: 100)')
    
    # Optional features
    parser.add_argument('--tor', dest='use_tor', action='store_true',
                       help='Enable TOR anonymity layer (triggers confirmation)')
    parser.add_argument('--config', dest='config_file',
                       help='Load configuration from JSON file')
    parser.add_argument('--save-config', dest='save_config',
                       help='Save configuration to JSON file after test')
    parser.add_argument('--no-safety-locks', dest='no_safety', action='store_true',
                       help='Disable safety locks (requires confirmation)')
    
    # Utility options
    parser.add_argument('-l', '--list-attacks', dest='list_attacks', action='store_true',
                       help='List all available test scenarios with descriptions')
    parser.add_argument('--version', action='version', version='Py-DDoS v7.0 - Educational Edition')
    
    return parser


def list_attacks():
    """Display all available test scenarios with educational information"""
    print(Styles.section("AVAILABLE TEST SCENARIOS"))
    print()
    
    for key, attack in Config.ATTACK_TYPES.items():
        print(f"  {Colors.BRIGHT_YELLOW}[{key}]{Colors.RESET} {Colors.BOLD}{attack['name']:<15}{Colors.RESET}")
        print(f"      {Colors.CYAN}{attack['description']}{Colors.RESET}")
        print(f"      Root Required: {Colors.BRIGHT_RED if attack['requires_root'] else Colors.BRIGHT_GREEN}"
              f"{'Yes' if attack['requires_root'] else 'No'}{Colors.RESET}")
        print()
    
    print()
    print(Styles.educational_note("NETWORK STRESS TEST CLASSIFICATION",
"""Network stress test scenarios are classified by OSI layer:

LAYER 7 (Application Layer):
  - HTTP: Direct application-layer stress testing
  - SLOWLORIS: Keep-alive header manipulation
  - SLOWREAD: Slow data transmission

LAYER 4 (Transport Layer):
  - UDP: User Datagram Protocol stress testing
  - SYN: TCP connection exhaustion scenarios
  - DNS: Recursive query amplification testing
  - NTP: Network Time Protocol reflection testing

LAYER 3 (Network Layer):
  - ICMP: Internet Control Message Protocol testing

MITIGATION STRATEGIES:
  1. Rate limiting and throttling
  2. Geo-redundancy and load balancing
  3. DDoS scrubbing centers
  4. BGP flowspec filtering
  5. Anycast distribution networks
  6. Advanced traffic analysis and detection"""))
    
    print()


def main():
        # About flag: show interactive about prompt
        if getattr(args, 'about', False):
            from core.about import about_prompt
            about_prompt()
            sys.exit(0)
    """Main entry point with safety lock integration"""
    
    parser = create_parser()
    args = parser.parse_args()

    # Developer test: run aiohttp error handling test suite
    if getattr(args, 'test_aiohttp_errors', False):
        import subprocess
        import os
        test_path = os.path.join(os.path.dirname(__file__), 'core', 'test_aiohttp_errors.py')
        result = subprocess.run([sys.executable, test_path])
        sys.exit(result.returncode)
    
    # Initialize safety locks
    safety = SafetyLocks()
    
    # Check if safety locks should be disabled
    if args.no_safety:
        print(Styles.warning("You requested to disable safety locks"))
        if not safety.disable_locks():
            sys.exit(1)
    
    # Check if no arguments provided
    if len(sys.argv) == 1:
        # Interactive mode
        print_banner()
        Config.print_disclaimer()
        print()
        print(Styles.info("Safety locks are ENABLED by default"))
        print(Styles.info("You will receive confirmation prompts for high-impact configurations"))
        print()
        
        engine = PyDDoS(use_cli_output=True)
        config = interactive_menu(engine.is_root)
        
        if config:
            # Run safety checks
            if not safety.check_all(config):
                print(Styles.warning("Attack cancelled due to safety checks"))
                sys.exit(1)
            
            engine.run_attack(config)
        else:
            print(Styles.error("Attack cancelled"))
            sys.exit(1)
    
    elif args.list_attacks:
        # List attack types with educational notes
        list_attacks()
        sys.exit(0)
    
    elif args.target and args.attack_type:
        # Command-line attack mode
        print_banner()
        Config.print_disclaimer()
        print()
        
        # Show safety status
        if safety.locks_enabled:
            print(Styles.success("Safety locks: ENABLED"))
            print(Styles.info("High-impact configurations will require confirmation"))
        else:
            print(Styles.danger("Safety locks: DISABLED"))
            print(Styles.warning("Proceeding without safety confirmations"))
        print()
        
        # Validate target
        import socket
        try:
            resolved_ip = socket.gethostbyname(args.target)
            print(Styles.success(f"Target resolved: {args.target} -> {resolved_ip}"))
        except socket.gaierror:
            try:
                socket.inet_aton(args.target)
                resolved_ip = args.target
            except socket.error:
                print(Styles.error(f"Invalid target: {args.target}"))
                sys.exit(1)
        
        # Validate attack type
        attack_info = Config.get_attack_info(args.attack_type.upper())
        if not attack_info:
            print(Styles.error(f"Unknown attack type: {args.attack_type}"))
            sys.exit(1)
        
        # Check root requirement
        engine = PyDDoS(use_cli_output=True)
        if attack_info['requires_root'] and not engine.is_root:
            print(Styles.error(f"{args.attack_type} attack requires root/admin privileges"))
            sys.exit(1)
        
        # Build configuration
        config = {
            'target_host': resolved_ip,
            'target_input': args.target,
            'target_port': args.port,
            'attack_type': args.attack_type.upper(),
            'threads': args.threads,
            'duration': args.duration,
            'use_tor': args.use_tor or False,
            'proxies': None
        }
        
        # Load config file if specified
        if args.config_file:
            print(Styles.info(f"Loading configuration from {args.config_file}"))
            loaded_config = Config.load_config(args.config_file)
            config.update(loaded_config)
        
        # Display configuration
        print()
        print(Styles.section("ATTACK CONFIGURATION"))
        print()
        print(Styles.table_row("Target", f"{config['target_input']} ({config['target_host']})"))
        print(Styles.table_row("Port", str(config['target_port'])))
        print(Styles.table_row("Attack Type", config['attack_type']))
        print(Styles.table_row("Threads", str(config['threads'])))
        print(Styles.table_row("Duration", f"{config['duration']} seconds"))
        print(Styles.table_row("TOR", "Enabled" if config['use_tor'] else "Disabled"))
        print()
        
        # Run safety checks
        if not safety.check_all(config):
            print(Styles.warning("Attack cancelled by safety checks"))
            sys.exit(1)
        
        # Execute attack
        if engine.run_attack(config):
            # Save config if requested
            if args.save_config:
                Config.save_config(config, args.save_config)
                print(Styles.success(f"Configuration saved to {args.save_config}"))
            
            print(Styles.success("Attack completed successfully"))
            sys.exit(0)
        else:
            print(Styles.error("Attack failed"))
            sys.exit(1)
    
    else:
        # Missing required arguments
        from core.help_menu import print_help_menu
        print_help_menu()
        print()
        print(Styles.warning("Missing required arguments for command-line mode"))
        print(Styles.info("Use: python3 py-ddos.py --help for more information"))
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print(Styles.warning("Attack interrupted by user"))
        sys.exit(0)
    except Exception as e:
        print(Styles.error(f"Unexpected error: {e}"))
        import traceback
        traceback.print_exc()
        sys.exit(1)
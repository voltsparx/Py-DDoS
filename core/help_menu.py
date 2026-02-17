"""
help_menu.py - Centralized help menu for Py-DDoS CLI
"""

from core.colors import Colors, Styles

def print_help_menu():
    print(Styles.section("Py-DDoS - Advanced Network Stress Testing Tool"))
    print(f"{Colors.BRIGHT_CYAN}Usage:{Colors.RESET}")
    print(f"  {Colors.BRIGHT_YELLOW}python py-ddos.py [options]{Colors.RESET}\n")
    print(f"{Colors.BRIGHT_CYAN}Options:{Colors.RESET}")
    print(f"  {Colors.BRIGHT_YELLOW}-t{Colors.RESET}, {Colors.BRIGHT_YELLOW}--target TARGET{Colors.RESET}         Target IP address or hostname")
    print(f"  {Colors.BRIGHT_YELLOW}-p{Colors.RESET}, {Colors.BRIGHT_YELLOW}--port PORT{Colors.RESET}             Target port (default: 80)")
    print(f"  {Colors.BRIGHT_YELLOW}-a{Colors.RESET}, {Colors.BRIGHT_YELLOW}--attack TYPE{Colors.RESET}           Attack type (HTTP, SLOWLORIS, UDP, SYN, SLOWREAD, DNS, ICMP, NTP)")
    print(f"  {Colors.BRIGHT_YELLOW}-d{Colors.RESET}, {Colors.BRIGHT_YELLOW}--duration SECONDS{Colors.RESET}      Attack duration in seconds (default: 60)")
    print(f"  {Colors.BRIGHT_YELLOW}-c{Colors.RESET}, {Colors.BRIGHT_YELLOW}--threads COUNT{Colors.RESET}         Number of worker threads (default: 100)")
    print(f"  {Colors.BRIGHT_YELLOW}--tor{Colors.RESET}                       Enable TOR anonymity layer")
    print(f"  {Colors.BRIGHT_YELLOW}--config FILE{Colors.RESET}               Load configuration from JSON file")
    print(f"  {Colors.BRIGHT_YELLOW}--save-config FILE{Colors.RESET}          Save configuration to JSON file after test")
    print(f"  {Colors.BRIGHT_YELLOW}--no-safety-locks{Colors.RESET}           Disable safety locks (requires confirmation)")
    print(f"  {Colors.BRIGHT_YELLOW}-l{Colors.RESET}, {Colors.BRIGHT_YELLOW}--list-attacks{Colors.RESET}          List all available test scenarios with descriptions")
    print(f"  {Colors.BRIGHT_YELLOW}--test-aiohttp-errors{Colors.RESET}       Run aiohttp error handling test suite (developer only)")
    print(f"  {Colors.BRIGHT_YELLOW}--about{Colors.RESET}                     Show information about this tool, attacks, credits, and disclaimers")
    print(f"  {Colors.BRIGHT_YELLOW}--version{Colors.RESET}                   Show version information")
    print(f"  {Colors.BRIGHT_YELLOW}-h{Colors.RESET}, {Colors.BRIGHT_YELLOW}--help{Colors.RESET}                  Show this help message and exit\n")
    print(f"{Colors.BRIGHT_CYAN}Examples:{Colors.RESET}")
    print(f"  python py-ddos.py -t example.com -a HTTP -d 60 -c 100")
    print(f"  python py-ddos.py --about")
    print(f"  python py-ddos.py --test-aiohttp-errors\n")
    print(f"For more information, see the README.md or use --about.\n")

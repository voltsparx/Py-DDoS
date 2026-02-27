"""
about.py - Interactive about menu for RedLoad-X
"""

from core.ui.colors import Colors, Styles
from core.config.metadata import AUTHOR, CONTACT, VERSION

def about_prompt():
    print(Styles.section("ABOUT RedLoad-X"))
    options = [
        "What is RedLoad-X?",
        "What do the attack types do?",
        "Types of DDoS Traffic",
        "Credits",
        "Legal Disclaimers",
        "Exit"
    ]
    while True:
        print(Styles.header("Select an option:"))
        for i, opt in enumerate(options, 1):
            print(Styles.option(str(i), opt))
        try:
            choice = int(input(Styles.prompt("Enter number")))
        except Exception:
            print(Styles.error("Invalid input. Please enter a number."))
            continue
        if choice == 1:
            print(Styles.subheader("\nWhat is RedLoad-X?\n"))
            print(f"{Colors.BRIGHT_CYAN}RedLoad-X{Colors.RESET} is a modular network stress testing tool for {Colors.BRIGHT_YELLOW}educational{Colors.RESET} and {Colors.BRIGHT_YELLOW}authorized penetration testing{Colors.RESET}. It supports multiple attack vectors (L3-L7), real-time metrics, safety locks, and detailed reporting.\nUse only with {Colors.BRIGHT_RED}explicit written authorization{Colors.RESET}.")
        elif choice == 2:
            print(Styles.subheader("\nAttack Types and How They Work\n"))
            print(f"{Colors.BRIGHT_YELLOW}HTTP:{Colors.RESET} Sends rapid HTTP GET/POST requests to overwhelm web servers.")
            print(f"{Colors.BRIGHT_YELLOW}SLOWLORIS:{Colors.RESET} Keeps HTTP connections open by sending incomplete headers.")
            print(f"{Colors.BRIGHT_YELLOW}SLOWREAD:{Colors.RESET} Reads server responses very slowly to exhaust resources.")
            print(f"{Colors.BRIGHT_YELLOW}UDP:{Colors.RESET} Floods target with UDP packets.")
            print(f"{Colors.BRIGHT_YELLOW}SYN:{Colors.RESET} Floods with TCP SYN packets to exhaust connection tables.")
            print(f"{Colors.BRIGHT_YELLOW}DNS:{Colors.RESET} Uses DNS amplification/reflection for high-volume attacks.")
            print(f"{Colors.BRIGHT_YELLOW}ICMP:{Colors.RESET} Floods with ICMP echo requests (ping flood).\n")
        elif choice == 3:
            print(Styles.subheader("\nTypes of DDoS Traffic\n"))
            print(f"{Colors.BRIGHT_CYAN}Volumetric:{Colors.RESET} Overwhelms bandwidth with massive traffic (UDP, ICMP, DNS amp).")
            print(f"{Colors.BRIGHT_CYAN}Protocol:{Colors.RESET} Exploits protocol weaknesses (SYN flood, fragmented packets).")
            print(f"{Colors.BRIGHT_CYAN}Application:{Colors.RESET} Targets application layer (HTTP, SLOWLORIS, SLOWREAD).\n")
            print(Styles.educational_note("How DDoS Attacks Differ", "Volumetric attacks saturate bandwidth. Protocol attacks exhaust server resources. Application attacks target specific services. RedLoad-X can simulate all three for defense testing.") )
        elif choice == 4:
            print(Styles.subheader("\nCredits\n"))
            print(f"  Author: {Colors.BRIGHT_GREEN}{AUTHOR}{Colors.RESET}")
            print(f"  Contact: {Colors.BRIGHT_CYAN}{CONTACT}{Colors.RESET}")
            print(f"  Version: {Colors.BRIGHT_YELLOW}{VERSION}{Colors.RESET}")
            print(f"  Contributors: See GitHub repository")
            print(f"  License: MIT\n")
        elif choice == 5:
            print(Styles.subheader("\nLEGAL DISCLAIMER\n"))
            print(f"{Colors.BRIGHT_RED}This tool is for educational and authorized testing only. Unauthorized use is illegal and may result in prosecution. The author assumes no liability for misuse.\n{Colors.RESET}")
            print(Styles.educational_note("Ethical Use Reminder", "Always obtain written permission before testing. Use responsibly and respect all applicable laws."))
        elif choice == 6:
            print(Styles.info("Exiting about menu.\n"))
            break
        else:
            print(Styles.error("Invalid selection. Please choose a valid number.\n"))

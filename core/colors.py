"""
ANSI Color codes for terminal output
Provides clean, professional CLI interface without aggressive language

Author: voltsparx
Contact: voltsparx@gmail.com
"""

class Colors:
    """ANSI color codes for terminal output"""
    
    # Reset
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Foreground Colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright Foreground Colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background Colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'


class Styles:
    """Helper methods for styled output"""
    
    @staticmethod
    def success(text: str) -> str:
        """Green success message"""
        return f"{Colors.BRIGHT_GREEN}[+] {text}{Colors.RESET}"
    
    @staticmethod
    def error(text: str) -> str:
        """Red error message"""
        return f"{Colors.BRIGHT_RED}[-] {text}{Colors.RESET}"
    
    @staticmethod
    def warning(text: str) -> str:
        """Yellow warning message"""
        return f"{Colors.BRIGHT_YELLOW}[!] {text}{Colors.RESET}"
    
    @staticmethod
    def info(text: str) -> str:
        """Cyan info message"""
        return f"{Colors.BRIGHT_CYAN}[*] {text}{Colors.RESET}"
    
    @staticmethod
    def header(text: str) -> str:
        """Bold white header"""
        return f"{Colors.BOLD}{Colors.WHITE}{text}{Colors.RESET}"
    
    @staticmethod
    def subheader(text: str) -> str:
        """Cyan subheader"""
        return f"{Colors.CYAN}{Colors.BOLD}{text}{Colors.RESET}"
    
    @staticmethod
    def section(text: str) -> str:
        """Blue section separator"""
        return f"{Colors.BRIGHT_BLUE}{'='*60}{Colors.RESET}\n{Colors.BRIGHT_BLUE}{text.center(60)}{Colors.RESET}\n{Colors.BRIGHT_BLUE}{'='*60}{Colors.RESET}"
    
    @staticmethod
    def table_row(label: str, value: str, color: str = Colors.WHITE) -> str:
        """Formatted table row"""
        return f"{Colors.CYAN}{label:<25}{Colors.RESET} {color}{value}{Colors.RESET}"
    
    @staticmethod
    def metric(label: str, value: str) -> str:
        """Metric display"""
        return f"{Colors.BRIGHT_CYAN}{label:<20}{Colors.RESET} {Colors.BRIGHT_GREEN}{value}{Colors.RESET}"
    
    @staticmethod
    def option(number: str, text: str, description: str = "") -> str:
        """Menu option formatting"""
        opt = f"{Colors.BRIGHT_YELLOW}[{number}]{Colors.RESET} {Colors.WHITE}{text}{Colors.RESET}"
        if description:
            opt += f" {Colors.DIM}{description}{Colors.RESET}"
        return opt    
    @staticmethod
    def educational_note(title: str, content: str) -> str:
        """Educational note with styling"""
        lines = [
            f"{Colors.BOLD}{Colors.BRIGHT_MAGENTA}{'='*60}{Colors.RESET}",
            f"{Colors.BOLD}{Colors.BRIGHT_MAGENTA}EDUCATIONAL NOTE: {title}{Colors.RESET}",
            f"{Colors.BOLD}{Colors.BRIGHT_MAGENTA}{'='*60}{Colors.RESET}",
            f"{Colors.WHITE}{content}{Colors.RESET}",
            f"{Colors.BOLD}{Colors.BRIGHT_MAGENTA}{'='*60}{Colors.RESET}"
        ]
        return '\n'.join(lines)
    
    @staticmethod
    def prompt(text: str) -> str:
        """Styled prompt"""
        return f"{Colors.BRIGHT_CYAN}>>> {text}{Colors.RESET} "
    
    @staticmethod
    def danger(text: str) -> str:
        """Danger/critical message in magenta"""
        return f"{Colors.BRIGHT_MAGENTA}[!!] {text}{Colors.RESET}"
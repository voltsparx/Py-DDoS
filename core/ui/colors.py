"""
ANSI Color codes for terminal output
Provides clean CLI interface without aggressive language

Author: voltsparx
Contact: voltsparx@gmail.com
"""

class Colors:
    """ANSI color codes for terminal output"""
    
    # Reset
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Foreground Colors (all bright red for unified aesthetic)
    BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = '\033[91m'
    
    # Bright Foreground Colors (also bright red)
    BRIGHT_BLACK = BRIGHT_RED = BRIGHT_GREEN = BRIGHT_YELLOW = BRIGHT_BLUE = BRIGHT_MAGENTA = BRIGHT_CYAN = BRIGHT_WHITE = '\033[91m'
    
    # Background Colors (red background)
    BG_BLACK = BG_RED = BG_GREEN = BG_YELLOW = BG_BLUE = BG_MAGENTA = BG_CYAN = BG_WHITE = '\033[41m'


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
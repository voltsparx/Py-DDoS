"""
Enhanced logging system with better readability

Author: voltsparx
Contact: voltsparx@gmail.com
"""

from pathlib import Path
from datetime import datetime
import sys
from ..ui.colors import Colors, Styles


class AttackLogger:
    """Enhanced attack logging with color-coded levels and better formatting"""
    
    # Log level colors
    LEVELS = {
        'DEBUG': Colors.BRIGHT_CYAN,
        'INFO': Colors.BRIGHT_BLUE,
        'SUCCESS': Colors.BRIGHT_GREEN,
        'WARNING': Colors.BRIGHT_YELLOW,
        'ERROR': Colors.BRIGHT_RED,
        'CRITICAL': Colors.BRIGHT_MAGENTA,
    }
    
    def __init__(self):
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / f"redloadx_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    def log(self, message, level="INFO"):
        """Log message with timestamp and level"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        color = self.LEVELS.get(level, Colors.WHITE)
        
        # Create log entry
        log_entry = f"[{timestamp}] [{level:<8}] {message}"
        
        # Console output with color
        colored_output = f"{color}[{timestamp}] [{level:<8}]{Colors.RESET} {message}"
        print(colored_output)
        
        # File output (no color codes)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    
    def info(self, message):
        """Log info level message"""
        self.log(message, "INFO")
    
    def success(self, message):
        """Log success level message"""
        self.log(message, "SUCCESS")
    
    def warning(self, message):
        """Log warning level message"""
        self.log(message, "WARNING")
    
    def error(self, message):
        """Log error level message"""
        self.log(message, "ERROR")
    
    def critical(self, message):
        """Log critical level message"""
        self.log(message, "CRITICAL")
    
    def debug(self, message):
        """Log debug level message"""
        self.log(message, "DEBUG")
    
    def get_log_path(self):
        """Get path to current log file"""
        return str(self.log_file)

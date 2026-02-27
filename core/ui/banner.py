# -*- coding: utf-8 -*-
from rich.console import Console
from rich.panel import Panel
from core.config.metadata import AUTHOR, CONTACT, VERSION

def print_banner(console):
    banner = f"""
 _____          _ _                     _     __   __
|  __ \        | | |                   | |    \ \ / /
| |__) |___  __| | |     ___   __ _  __| |_____\ V / 
|  _  // _ \/ _` | |    / _ \ / _` |/ _` |______> <  
| | \ \  __/ (_| | |___| (_) | (_| | (_| |     / . \ 
|_|  \_\___|\__,_|______\___/ \__,_|\__,_|    /_/ \_\\
                                  v{VERSION}
    Operational Network Stress Testing Tool
"""
    info = f"Author: {AUTHOR}    Contact: {CONTACT}    Version: {VERSION}"
    console.print(Panel(banner, title=info, style="bold red", border_style="bright_red"))
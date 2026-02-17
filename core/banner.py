# -*- coding: utf-8 -*-
from rich.console import Console
from rich.panel import Panel
from core.metadata import AUTHOR, CONTACT, VERSION

def print_banner(console):
    banner = f"""
      ____              ____  ____       _____
     / __ \__  __      / __ \/ __ \____ / ___/
    / /_/ / / / /_____/ / / / / / / __ \\__ \
   / ____/ /_/ /_____/ /_/ / /_/ / /_/ /__/ /
  /_/    \__, /     /_____/_____/\____/____/
      /____/                               
                                  v{VERSION}
    Operational Network Stress Testing Tool
"""
    info = f"Author: {AUTHOR}    Contact: {CONTACT}    Version: {VERSION}"
    console.print(Panel(banner, title=info, style="bold cyan", border_style="bright_blue"))
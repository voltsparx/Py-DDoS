# -*- coding: utf-8 -*-
"""
Project Metadata for Py-DDoS
Centralized version, author, and repository information

Author: voltsparx
Contact: voltsparx@gmail.com
"""

# Version information
VERSION = "7.5.0"
VERSION_NAME = "Advanced Features Release"
VERSION_DATE = "2026-02-17"

# Repository information
REPOSITORY = "https://github.com/voltsparx/Py-DDoS"
REPOSITORY_OWNER = "voltsparx"
LICENSE = "MIT"

# Author information
AUTHOR = "voltsparx"
AUTHOR_EMAIL = "voltsparx@gmail.com"
CONTACT = "voltsparx@gmail.com"

# Project information
PROJECT_NAME = "Py-DDoS"
PROJECT_DESCRIPTION = "Advanced network stress testing framework with multi-protocol support"
PROJECT_URL = "https://github.com/voltsparx/Py-DDoS"

# Feature flags
FEATURES = {
    "rate_limiting": True,
    "async_engine": True,
    "structured_logging": True,
    "dry_run_mode": True,
    "warmup_phase": True,
    "adaptive_load_control": True,
    "test_harness": True,
    "tor_support": True,
}

# Dependencies
REQUIRED_PACKAGES = [
    "rich>=13.0.0",
    "requests>=2.28.0",
    "matplotlib>=3.5.0",
    "scapy>=2.4.0",
    "stem>=1.8.0",
]

OPTIONAL_PACKAGES = [
    "aiohttp>=3.8.0",  # For async_engine high-scale testing
]

# Banner
BANNER = f"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║               {PROJECT_NAME.center(49)}                   ║
║                 Version {VERSION.center(45)}                  ║
║            {PROJECT_DESCRIPTION.center(49)}  ║
║                                                           ║
║  Repository: {REPOSITORY.ljust(48)}║
║  Author:     {AUTHOR.ljust(48)}║
║  Contact:    {CONTACT.ljust(48)}║
║  License:    {LICENSE.ljust(48)}║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

# Help text
HELP_TEXT = f"""
{PROJECT_NAME} v{VERSION} - {PROJECT_DESCRIPTION}

Usage:
    python py-ddos.py

For more information, visit: {PROJECT_URL}
Report bugs to: {CONTACT}
"""


def get_version_string() -> str:
    """Get formatted version string"""
    return f"{VERSION} ({VERSION_NAME}) - {VERSION_DATE}"


def get_banner() -> str:
    """Get formatted banner"""
    return BANNER


def get_help() -> str:
    """Get help text"""
    return HELP_TEXT


def print_banner() -> None:
    """Print banner to console"""
    print(BANNER)


def print_version() -> None:
    """Print version information"""
    print(f"{PROJECT_NAME} {get_version_string()}")


__all__ = [
    "VERSION",
    "VERSION_NAME",
    "VERSION_DATE",
    "REPOSITORY",
    "REPOSITORY_OWNER",
    "LICENSE",
    "AUTHOR",
    "AUTHOR_EMAIL",
    "CONTACT",
    "PROJECT_NAME",
    "PROJECT_DESCRIPTION",
    "PROJECT_URL",
    "FEATURES",
    "REQUIRED_PACKAGES",
    "OPTIONAL_PACKAGES",
    "BANNER",
    "HELP_TEXT",
    "get_version_string",
    "get_banner",
    "get_help",
    "print_banner",
    "print_version",
]

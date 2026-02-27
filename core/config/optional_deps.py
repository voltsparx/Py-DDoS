# -*- coding: utf-8 -*-
"""
Optional Dependency Handler for RedLoad-X
Provides graceful error handling for optional libraries (aiohttp, etc.)

Author: voltsparx
Contact: voltsparx@gmail.com
"""

import sys
from typing import Optional, Callable, Any


def check_aiohttp_available() -> tuple[bool, Optional[str]]:
    """
    Check if aiohttp is available
    
    Returns:
        Tuple of (is_available, error_message)
        error_message is None if available, string if not
    """
    try:
        import aiohttp  # noqa: F401
        return True, None
    except ImportError as e:
        return False, str(e)


def get_aiohttp_install_instructions() -> str:
    """Get aiohttp installation instructions"""
    return """
aiohttp is not installed. Install it with one of these commands:

  # Install aiohttp directly
  pip install aiohttp>=3.8.0

  # Install RedLoad-X with async support
  pip install -e ".[async]"

  # Or install all optional dependencies
  pip install -r requirements.txt
"""


def require_aiohttp(func_name: str = "AsyncHTTPFlood") -> None:
    """
    Require aiohttp to be installed, raise with helpful error if not
    
    Args:
        func_name: Name of function/class requiring aiohttp
    
    Raises:
        ImportError: With installation instructions
    """
    available, error = check_aiohttp_available()
    if not available:
        raise ImportError(
            f"{func_name} requires aiohttp library which is not installed.\n"
            f"{get_aiohttp_install_instructions()}\n"
            f"Original error: {error}"
        )


def get_optional_module(module_name: str, min_version: Optional[str] = None) -> Any:
    """
    Import optional module with helpful error handling
    
    Args:
        module_name: Name of module to import (e.g., 'aiohttp')
        min_version: Minimum required version (e.g., '3.8.0')
    
    Returns:
        Imported module
    
    Raises:
        ImportError: With installation instructions
    """
    try:
        module = __import__(module_name)
        
        # Check version if specified
        if min_version and hasattr(module, '__version__'):
            installed_version = module.__version__
            if installed_version < min_version:
                raise ImportError(
                    f"{module_name} version {installed_version} is too old. "
                    f"Minimum required: {min_version}. "
                    f"Install with: pip install {module_name}>={min_version}"
                )
        
        return module
    except ImportError as e:
        raise ImportError(
            f"Optional dependency '{module_name}' is not installed.\n"
            f"Install with: pip install {module_name}"
            + (f">={min_version}" if min_version else "")
            + f"\n\nOriginal error: {e}"
        ) from e


__all__ = [
    'check_aiohttp_available',
    'get_aiohttp_install_instructions',
    'require_aiohttp',
    'get_optional_module',
]

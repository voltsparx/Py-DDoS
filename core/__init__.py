from .engine import RedLoadX, PyDDoS  # PyDDoS remains for compatibility
from .config.config import Config
from .safety.safety_locks import SafetyLocks
from .ui.colors import Colors, Styles
from .config import optional_deps
from .config.optional_deps import (
    check_aiohttp_available,
    get_aiohttp_install_instructions,
    require_aiohttp,
    get_optional_module,
)

__all__ = [
    'RedLoadX',
    'PyDDoS',  # alias for legacy code
    'Config',
    'SafetyLocks',
    'Colors',
    'Styles',
    'check_aiohttp_available',
    'get_aiohttp_install_instructions',
    'require_aiohttp',
    'get_optional_module',
]

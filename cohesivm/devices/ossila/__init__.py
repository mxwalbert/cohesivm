import importlib

try:
    importlib.import_module('xtralien')
    xtralien_available = True
except ImportError:
    xtralien_available = False

if xtralien_available:
    from . import OssilaX200

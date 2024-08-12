import importlib

try:
    importlib.import_module('pyvisa')
    pyvisa_available = True
except ImportError:
    pyvisa_available = False

if pyvisa_available:
    from . import Agilent4156C, Agilent4284A

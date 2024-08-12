from __future__ import annotations
import importlib


class CompatibilityError(Exception):
    """Raised if the components/parameters of a composite class are not compatible with each other."""


from . import experiment, database, devices, channels, interfaces, measurements, analysis
from . import data_stream, plots
from . import config


try:
    importlib.import_module('bqplot')
    bqplot_available = True
except ImportError:
    bqplot_available = False

if bqplot_available:
    from . import gui

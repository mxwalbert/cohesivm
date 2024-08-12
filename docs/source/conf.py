import sys
import os

sys.path.insert(0, os.path.abspath('../..'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'COHESIVM'
copyright = '2024, Maximilian Wolf, Selina Götz, Georg K.H. Madsen, Theodoros Dimopoulos'
author = 'Maximilian Wolf, Selina Götz, Georg K.H. Madsen, Theodoros Dimopoulos'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_rtd_theme',
    'sphinx.ext.mathjax'
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable', None),
    'matplotlib': ('https://matplotlib.org/stable', None),
    'bqplot': ('https://bqplot.github.io/bqplot/', None)
}

templates_path = ['_templates']
exclude_patterns = [
    'readme/*'
]
autodoc_member_order = 'bysource'
autodoc_type_aliases = {
    'cohesivm.channels.TChannel': 'cohesivm.channels.TChannel',
    'cohesivm.devices.ossila.OssilaX200.TChannel': 'cohesivm.devices.ossila.OssilaX200.TChannel',
    'cohesivm.devices.agilent.Agilent4156C.TChannel': 'cohesivm.devices.agilent.Agilent4156C.TChannel',
    'DatabaseValue': 'DatabaseValue',
    'DatabaseDict': 'DatabaseDict',
    'Dataset': 'Dataset'
}
autodoc_type_hints = 'both'
add_module_names = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['css/custom.css']

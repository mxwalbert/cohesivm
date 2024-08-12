"""This module loads the ``config.ini`` file by recursively searching for it in the root of the project folder. It
provides two methods for retrieving the data."""
from __future__ import annotations
import os
import configparser
from typing import Dict, Any

path = 'config.ini'
for _ in range(10):
    if not os.path.isfile(path):
        path = f'../{path}'
    else:
        break
_config = configparser.ConfigParser()
_config.read(path)


def get_section(section: str) -> Dict[str, Any]:
    """
    Retrieves the entire section from the configuration file.

    :param section: The section name in the configuration file.
    :returns: A dictionary containing key-value pairs of the section.
    :raises KeyError: If the section is not found in the configuration file.
    """
    return _config._sections[section]


def get_option(section: str, option: str) -> Any:
    """
    Retrieves the value for a specific option within a given section from the configuration file.

    :param section: The section name in the configuration file.
    :param option: The option name within the section.
    :returns: The value corresponding to the specified section and option.
    :raises NoSectionError: If the section is not found in the configuration file.
    :raises NoOptionError: If the option is not found within the section in the configuration file.
    """
    return _config.get(section, option)

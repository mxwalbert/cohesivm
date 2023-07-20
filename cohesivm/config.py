import os
import configparser
from typing import Dict, Any

path = 'config.ini'
if not os.path.isfile(path):
    path = f'../{path}'
_config = configparser.ConfigParser()
_config.read(path)


def get_section(section: str) -> Dict[str, Any]:
    return _config._sections[section]


def get_option(section: str, option: str) -> Any:
    return _config.get(section, option)

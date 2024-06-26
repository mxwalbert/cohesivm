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
    return _config._sections[section]


def get_option(section: str, option: str) -> Any:
    return _config.get(section, option)

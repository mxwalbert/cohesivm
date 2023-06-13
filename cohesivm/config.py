import configparser
from typing import Dict, Any

_config = configparser.ConfigParser()
_config.read('config.ini')


def get_section(section: str) -> Dict[str, Any]:
    return _config._sections[section]


def get_option(section: str, option: str) -> Any:
    return _config.get(section, option)

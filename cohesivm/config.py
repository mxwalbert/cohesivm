import configparser

__config = configparser.ConfigParser()
__config.read('config.ini')


def get(section: str, option: str):
    return __config.get(section, option)

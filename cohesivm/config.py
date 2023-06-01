import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def get(section: str, option: str):
    return config.get(section, option)

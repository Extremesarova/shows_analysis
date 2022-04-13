import os
from configparser import ConfigParser


class ConfigReader:
    def __init__(self, path=os.path.join("config", "config.ini")):
        self.path = path
        self.config = self._reading_config()

    def _reading_config(self) -> ConfigParser:
        config = ConfigParser()
        if os.path.isfile(self.path):
            config.read(self.path)
        else:
            print("Config file not found")
        return config

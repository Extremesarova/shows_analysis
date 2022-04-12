from configparser import ConfigParser


class ConfigReader:
    def __init__(self, path="config/config.ini"):
        self.path = path
        self.config = self._reading_config()

    def _reading_config(self) -> ConfigParser:
        config = ConfigParser()
        config.read(self.path)

        return config

import configparser

class ConfigurationManagerClass:
    def __init__(self,configPath):
        self.configPath = configPath

    def getConnectionString(self):
        config = configparser.RawConfigParser()
        config.read(self.configPath)
        connectionStringPath = config.get("Data","ConnectionString")
        return connectionStringPath
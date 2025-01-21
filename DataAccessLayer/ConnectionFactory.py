import os
import pyodbc
from Utility.ConfigurationManager import ConfigurationManagerClass

class ConnectionFactoryClass:
    def __init__(self):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        CONFIG_PATH = os.path.join(ROOT_DIR, '../configuration.ini')
        configManager = ConfigurationManagerClass(CONFIG_PATH)
        self.ConnectionString = configManager.getConnectionString()

    def makeConnection(self):
        return pyodbc.connect(self.ConnectionString)
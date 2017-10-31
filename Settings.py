from DataConnection import DataConnection
import Utilities
from ast import literal_eval

budgetThreshold = 70  #TODO: Store in db

class Settings:
    settingsTable = "Setting"
    settingIdColumn = "ID"
    settingDictionaryColumn = "Dictionary"
    
    def __init__(self, settingId, settingDictionary):
        self.settingId = settingId
        self.settingDictionary = settingDictionary
    
    def getExistingSettings():
        connection = DataConnection()
        query = "SELECT {2}, {0} FROM {1};".format(Settings.settingDictionaryColumn, Settings.settingsTable, Settings.settingIdColumn)
        result = connection.runQuery(query).fetchone()
        connection.closeConnection()
        
        if result != None:
            settingId = result[0]
            settingDictionary = literal_eval(result[1])
            return Settings(settingId, settingDictionary)
        else:
            return None
    
    def updateExistingSettings(self, newDictionary):
        connection = DataConnection()        
        query = """UPDATE {0} SET {1} = "{2}" WHERE {3} = {4};""".format(Settings.settingsTable, Settings.settingDictionaryColumn, newDictionary, Settings.settingIdColumn, self.settingId)
        connection.updateData(query)
        connection.closeConnection()
        
        print("Successfully updated dictionary to {}".format(newDictionary))
        self.settingDictionary = newDictionary
    
    def __str__(self):
        message = "Setting ID = " + str(self.settingId) + "\n"
        message += "Dictionary = " + str(self.settingDictionary)
        return message
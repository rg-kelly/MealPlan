from DataConnection import DataConnection
import Utilities
from datetime import datetime
from ast import literal_eval

class Settings:
    settingsTable = "Settings"
    settingIdColumn = "Setting_ID"
    settingDictionaryColumn = "Setting_Dictionary"
    
    def __init__(self, settingId, settingDictionary):
        self.settingId = settingId
        self.settingDictionary = settingDictionary
    
    def getExistingSetting(key):
        connection = DataConnection()
        query = """SELECT {3}, {0} FROM {1} WHERE {0} LIKE "%'{2}':%";""".format(Settings.settingDictionaryColumn, Settings.settingsTable, key, Settings.settingIdColumn)
        result = connection.runQuery(query).fetchone()
        connection.closeConnection()
        
        if result != None:
            settingId = result[0]
            settingDictionary = literal_eval(result[1])
            return Settings(settingId, settingDictionary)
        else:
            return None
    
    def updateExistingSetting(self, key, newValue):
        newDictionary = self.settingDictionary
        newDictionary[key] = newValue
        
        if newDictionary != self.settingDictionary:            
            connection = DataConnection()        
            query = """UPDATE {0} SET {1} = "{2}" WHERE {3} = {4};""".format(Settings.settingsTable, Settings.settingDictionaryColumn, self.settingDictionary, Settings.settingIdColumn, self.settingId)
            connection.updateData(query)
            connection.closeConnection()
            
            print("Successfully updated dictionary from {} to {}.".format(self.settingDictionary, newDictionary))
            self.settingDictionary = newDictionary
    
    def __str__(self):
        message = "Setting ID = " + str(self.settingId) + "\n"
        message += "Dictionary = " + str(self.settingDictionary)
        return message
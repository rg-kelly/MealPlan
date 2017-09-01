from DataConnection import DataConnection
import Utilities

class Amount_Units:
    amountUnitsTable = "Amount_Units"
    unitIdColumn = "Unit_ID"
    unitNameColumn = "Unit_Name"
    
    def __init__(self, unitsId, unitsName):
        self.unitsId = unitsId
        self.unitsName = unitsName
        
    def __str__(self):
        message = "Unit: " + self.unitsName
        
        return message
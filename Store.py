from DataConnection import DataConnection
import Utilities

class Store:
    storeTable = "Store"
    storeIdColumn = "Store_ID"
    storeNameColumn = "Store_Name"
    
    def __init__(self, storeId, storeName):
        self.storeId = storeId
        self.storeName = storeName
        
    def __str__(self):
        message = "Unit: " + self.storeName
        
        return message
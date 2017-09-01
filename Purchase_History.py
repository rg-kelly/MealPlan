from DataConnection import DataConnection
import Utilities
from Store import Store
from Amount_Units import Amount_Units
from Ingredient import Ingredient

class Purchase_History:
    purchaseHistoryTable = "Purchase_History"    
    purchaseIdColumn = "Purchase_ID"
    pricePerUnitColumn = "Price_Per_Unit"
    
    def __init__(self, ingredientName, amount, units, purchasePrice, store, pricePerUnit):
        self.ingredientName = ingredientName
        self.amount = amount
        self.units = units
        self.purchasePrice = purchasePrice
        self.store = store
        self.pricePerUnit = pricePerUnit
    
    @classmethod
    def createNewPurchase(cls, ingredientName, amount, units, purchasePrice, store):
        pricePerUnit = (float(purchasePrice) / float(amount))
        
        return Purchase_History(ingredientName, amount, units, purchasePrice, store, pricePerUnit)
    
    def add(self):
        unitId = Utilities.getKnownInfo(self.units, Amount_Units.unitIdColumn, Amount_Units.unitNameColumn, Amount_Units.amountUnitsTable, False)
        ingredientId = Utilities.getKnownInfo(self.ingredientName, Ingredient.ingredientIdColumn, Ingredient.ingredientNameColumn, Ingredient.ingredientTable, False)
        storeId = Utilities.getKnownInfo(self.store, Store.storeIdColumn, Store.storeNameColumn, Store.storeTable, False)
        
        connection = DataConnection()
        query = "INSERT INTO {} ({}, {}, {}, {}) VALUES (%s, %s, %s, %s);".format(Purchase_History.purchaseHistoryTable, Purchase_History.pricePerUnitColumn, Ingredient.ingredientIdColumn, Store.storeIdColumn, Amount_Units.unitIdColumn)
        insertValues = (self.pricePerUnit, ingredientId, storeId, unitId)
        connection.updateData(query, insertValues)
        connection.closeConnection()
    
    def __str__(self):
        if self.units.endswith("s"): self.units = self.units.strip("s")
        
        message = "-------- Summary --------\n"
        message += "Ingredient Name: {}\n".format(self.ingredientName)
        message += "Amount purchased: {} {}\n".format(self.amount, self.units)
        message += "Purchase price: {}\n".format(self.purchasePrice)
        message += "Store: {}\n".format(self.store)
        message += "Price per {}: ${:.2f}".format(self.units, self.pricePerUnit)
        
        return message
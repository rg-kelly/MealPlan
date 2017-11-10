from DataConnection import DataConnection
import Utilities
from Store import Store
from Amount_Units import Amount_Units
from Ingredient import Ingredient
from WeekOfDate import WeekOfDate

class Purchase_History:
    purchaseHistoryTable = "Purchase_History"    
    purchaseIdColumn = "Purchase_ID"
    pricePerUnitColumn = "Price_Per_Unit"
    amountColumn = "Amount"
    notesColumn = "Notes"
    
    def __init__(self, ingredientName, amount, units, purchasePrice, store, pricePerUnit, weekOfDate, notes):
        self.ingredientName = ingredientName
        self.amount = amount
        self.units = units
        self.purchasePrice = purchasePrice
        self.store = store
        self.pricePerUnit = pricePerUnit
        self.weekOfDate = weekOfDate
        self.amount = amount
        self.notes = notes
    
    @classmethod
    def createNewPurchase(cls, ingredientName, amount, units, purchasePrice, store, weekOfDate, notes):
        pricePerUnit = (float(purchasePrice) / float(amount))
        
        return Purchase_History(ingredientName, amount, units, purchasePrice, store, pricePerUnit, weekOfDate, notes)
    
    def add(self):
        unitId = Utilities.getKnownInfo(self.units, Amount_Units.unitIdColumn, Amount_Units.unitNameColumn, Amount_Units.amountUnitsTable, False)
        ingredientId = Utilities.getKnownInfo(self.ingredientName, Ingredient.ingredientIdColumn, Ingredient.ingredientNameColumn, Ingredient.ingredientTable, False)
        storeId = Utilities.getKnownInfo(self.store, Store.storeIdColumn, Store.storeNameColumn, Store.storeTable, False)
        dateId = Utilities.getKnownInfo(self.weekOfDate, WeekOfDate.dateIdColumn, WeekOfDate.dateNameColumn, WeekOfDate.dateTable, False)
        
        connection = DataConnection()
        query = "INSERT INTO {} ({}, {}, {}, {}, {}, {}, {}) VALUES (%s, %s, %s, %s, %s, %s, %s);".format(Purchase_History.purchaseHistoryTable,
                                                                                                          Purchase_History.pricePerUnitColumn,
                                                                                                          Ingredient.ingredientIdColumn,
                                                                                                          Store.storeIdColumn,
                                                                                                          Amount_Units.unitIdColumn,
                                                                                                          WeekOfDate.dateIdColumn,
                                                                                                          Purchase_History.amountColumn,
                                                                                                          Purchase_History.notesColumn)
        insertValues = (self.pricePerUnit, ingredientId, storeId, unitId, dateId, self.amount, self.notes)
        connection.updateData(query, insertValues)
        connection.closeConnection()
    
    def getMostCommonUnit(ingredientName, returnAmount = False):
        query = """SELECT {0}, {1}, {2}, {3}, MAX(Number_Of_Uses) FROM 
                    (SELECT {4}.{0}, {4}.{1}, {5}.{2}, {6}.{3}, COUNT({5}.{7}) AS Number_Of_Uses
                    FROM {5}
                    JOIN {6} ON {5}.{8} = {6}.{8}
                    JOIN {4} ON {4}.{0} = {5}.{0}
                    WHERE {4}.{1} = '{9}'
                    GROUP BY {4}.{0}, {4}.{1}, {5}.{2}, {6}.{3}) AS Count;""".format(Ingredient.ingredientIdColumn,
                                                                                     Ingredient.ingredientNameColumn,
                                                                                     Purchase_History.amountColumn,
                                                                                     Amount_Units.unitNameColumn,
                                                                                     Ingredient.ingredientTable,
                                                                                     Purchase_History.purchaseHistoryTable,
                                                                                     Amount_Units.amountUnitsTable,
                                                                                     Purchase_History.purchaseIdColumn,
                                                                                     Amount_Units.unitIdColumn,
                                                                                     ingredientName)
        
        connection = DataConnection()
        result = connection.runQuery(query)
        resultList = result.fetchall()
        result.close()
        connection.closeConnection()
        
        if resultList:
            firstRow = 0
            unitsColumnPosition = 3
            units = resultList[firstRow][unitsColumnPosition]
            
            if returnAmount:
                amountColumnPosition = 2
                amount = resultList[firstRow][amountColumnPosition]
                
                return amount, units
            else:
                return units
        else:
            return None

    def getAveragePricePerUnit(ingredientName):
        defaultPrice = 0
        defaultUnits = False
        
        ingredientId = Utilities.getKnownInfo(ingredientName, Ingredient.ingredientIdColumn, Ingredient.ingredientNameColumn, Ingredient.ingredientTable, False)
        if ingredientId:
            query = """SELECT AVG({1}.{0}), {5}.{6}
                        FROM {1} JOIN {5} ON {1}.{4} = {5}.{4}
                        WHERE {1}.{2} = {3}
                        GROUP BY {1}.{2}, {5}.{6};""".format(Purchase_History.pricePerUnitColumn,
                                                    Purchase_History.purchaseHistoryTable,
                                                    Ingredient.ingredientIdColumn,
                                                    ingredientId,
                                                    Amount_Units.unitIdColumn,
                                                    Amount_Units.amountUnitsTable,
                                                    Amount_Units.unitNameColumn)
        else:
            return defaultPrice, defaultUnits
        
        connection = DataConnection()
        result = connection.runQuery(query)
        resultList = result.fetchall()
        result.close()
        connection.closeConnection()
        
        if resultList:
            firstRow = 0
            firstColumn = 0
            secondColumn = 1
            
            averagePrice = resultList[firstRow][firstColumn]    # May need to update if there is a case where more than one row would be returned...
            unit = resultList[firstRow][secondColumn]
                
            return averagePrice, unit
        else: return defaultPrice, defaultUnits
    
    def __str__(self):
        if self.units.endswith("s"): self.units = self.units.strip("s")
        
        message = "-------- Summary --------\n"
        message += "Ingredient Name: {}\n".format(self.ingredientName)
        message += "Amount purchased: {} {}\n".format(self.amount, self.units)
        message += "Purchase price: {}\n".format(self.purchasePrice)
        message += "Store: {}\n".format(self.store)
        message += "Price per {}: ${:.2f}\n".format(self.units, self.pricePerUnit)
        message += "Week of Date: {}".format(self.weekOfDate)
        
        return message

#amount, unit = Purchase_History.getAveragePricePerUnit("Salsa")
#print(amount)
#print(unit)

#print(Purchase_History.getMostCommonUnit('Salsa'))
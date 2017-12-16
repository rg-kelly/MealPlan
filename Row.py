from Sheets import main
from Purchase_History import Purchase_History
from Ingredient import Ingredient
from Store import Store
from WeekOfDate import WeekOfDate
from Amount_Units import Amount_Units
from DataConnection import DataConnection

class Row:
    firstRow = 0
    pricePosition = 1
    unitPosition = 2
    locationPosition = 3
    datePosition = 4    
    
    def __init__(self, itemName, average, recent, recentLocation, recentDate, lowest, lowestLocation, highest, highestLocation):
        self.itemName = itemName
        self.average = average
        self.recent = recent
        self.recentLocation = recentLocation
        self.recentDate = recentDate
        self.lowest = lowest
        self.lowestLocation = lowestLocation
        self.highest = highest
        self.highestLocation = highestLocation
        
    @classmethod
    def createNewRow(cls, itemName):
        average, recent, recentLocation, recentDate, lowest, lowestLocation, highest, highestLocation = Row.getPricePerUnit(itemName)
        
        return Row(itemName, average, recent, recentLocation, recentDate, lowest, lowestLocation, highest, highestLocation)
    
    def getPricePerUnit(itemName):        
        recentOrderBy = "{}.{} DESC ".format(WeekOfDate.dateTable, WeekOfDate.dateNameColumn)
        lowestOrderBy = "{}.{} ASC ".format(Purchase_History.purchaseHistoryTable, Purchase_History.pricePerUnitColumn)
        highestOrderBy = "{}.{} DESC ".format(Purchase_History.purchaseHistoryTable, Purchase_History.pricePerUnitColumn)
        
        recentQuery = Row.getPricePerUnitQuery(itemName, recentOrderBy)
        lowestQuery = Row.getPricePerUnitQuery(itemName, lowestOrderBy)
        highestQuery = Row.getPricePerUnitQuery(itemName, highestOrderBy)
        
        connection = DataConnection()
        recentResult = (connection.runQuery(recentQuery)).fetchall()
        lowestResult = (connection.runQuery(lowestQuery)).fetchall()
        highestResult = (connection.runQuery(highestQuery)).fetchall()
        connection.closeConnection()
        
        if recentResult:
            recent, recentLocation, recentDate = Row.formatPrice(recentResult[Row.firstRow][Row.pricePosition], recentResult[Row.firstRow][Row.unitPosition]), recentResult[Row.firstRow][Row.locationPosition], recentResult[Row.firstRow][Row.datePosition]
        if lowestResult:
            lowest, lowestLocation = Row.formatPrice(lowestResult[Row.firstRow][Row.pricePosition], lowestResult[Row.firstRow][Row.unitPosition]), lowestResult[Row.firstRow][Row.locationPosition]
        if highestResult:
            highest, highestLocation = Row.formatPrice(highestResult[Row.firstRow][Row.pricePosition], highestResult[Row.firstRow][Row.unitPosition]), highestResult[Row.firstRow][Row.locationPosition]
        average = Row.getAveragePricePerUnit(itemName)
        
        return average, recent, recentLocation, recentDate, lowest, lowestLocation, highest, highestLocation
    
    def formatPrice(price, units):
        formattedPrice = "${:.2f}/{}".format(price, units)
        
        return formattedPrice
    
    def getPricePerUnitQuery(itemName, orderBySpecifier):
        query = """SELECT {2}.{4}, {0}.{1}, {8}.{10}, {5}.{7}, {11}.{13}
                        FROM {0}
                        JOIN {2} ON {0}.{3} = {2}.{3}
                        JOIN {5} ON {5}.{6} = {0}.{6}
                        JOIN {8} ON {8}.{9} = {0}.{9}
                        JOIN {11} ON {11}.{12} = {0}.{12}
                        WHERE {2}.{4} = '{14}'
                        ORDER BY {15}
                        LIMIT 1;""".format(Purchase_History.purchaseHistoryTable,
                                           Purchase_History.pricePerUnitColumn,
                                           Ingredient.ingredientTable,
                                           Ingredient.ingredientIdColumn,
                                           Ingredient.ingredientNameColumn,
                                           Store.storeTable,
                                           Store.storeIdColumn,
                                           Store.storeNameColumn,
                                           Amount_Units.amountUnitsTable,
                                           Amount_Units.unitIdColumn,
                                           Amount_Units.unitNameColumn,
                                           WeekOfDate.dateTable,
                                           WeekOfDate.dateIdColumn,
                                           WeekOfDate.dateNameColumn,
                                           itemName,
                                           orderBySpecifier)
        
        return query
    
    def getAveragePricePerUnit(itemName):     
        connection = DataConnection()
        
        averageQuery = """SELECT {2}.{4}, AVG({0}.{1}), {8}.{10}
                            FROM {0}
                            JOIN {2} ON {0}.{3} = {2}.{3}
                            JOIN {5} ON {5}.{6} = {0}.{6}
                            JOIN {8} ON {8}.{9} = {0}.{9}
                            WHERE {2}.{4} = '{11}'
                            GROUP BY {2}.{4}, {8}.{10};""".format(Purchase_History.purchaseHistoryTable,
                                                             Purchase_History.pricePerUnitColumn,
                                                             Ingredient.ingredientTable,
                                                             Ingredient.ingredientIdColumn,
                                                             Ingredient.ingredientNameColumn,
                                                             Store.storeTable,
                                                             Store.storeIdColumn,
                                                             Store.storeNameColumn,
                                                             Amount_Units.amountUnitsTable,
                                                             Amount_Units.unitIdColumn,
                                                             Amount_Units.unitNameColumn,
                                                             itemName)
        averageResult = (connection.runQuery(averageQuery)).fetchall()
        if len(averageResult) == 1:
            averagePricePerUnit = Row.formatPrice(averageResult[Row.firstRow][Row.pricePosition], averageResult[Row.firstRow][Row.unitPosition])
        
        # Elif not same then find most common unit and use pint to convert other(s) to that one and then take average using python
        elif len(averageResult) > 1:
            dataQuery = """SELECT {2}.{4}, {0}.{1}, {8}.{10}
                                FROM {0}
                                JOIN {2} ON {0}.{3} = {2}.{3}
                                JOIN {5} ON {5}.{6} = {0}.{6}
                                JOIN {8} ON {8}.{9} = {0}.{9}
                                WHERE {2}.{4} = '{11}';""".format(Purchase_History.purchaseHistoryTable,
                                                                  Purchase_History.pricePerUnitColumn,
                                                                  Ingredient.ingredientTable,
                                                                  Ingredient.ingredientIdColumn,
                                                                  Ingredient.ingredientNameColumn,
                                                                  Store.storeTable,
                                                                  Store.storeIdColumn,
                                                                  Store.storeNameColumn,
                                                                  Amount_Units.amountUnitsTable,
                                                                  Amount_Units.unitIdColumn,
                                                                  Amount_Units.unitNameColumn,
                                                                  itemName)
            
            

        connection.closeConnection()
        
        return averagePricePerUnit
    
    def __str__(self):
        summaryOfSelf = "Name: {}\n".format(self.itemName)
        summaryOfSelf += "Avg price per unit: {}\n".format(self.average)
        summaryOfSelf += "Lowest price per unit: {} at {}\n".format(self.lowest, self.lowestLocation)
        summaryOfSelf += "Highest price per unit: {} at {}\n".format(self.highest, self.highestLocation)
        summaryOfSelf += "Recent price per unit: {} at {} on {}".format(self.recent, self.recentLocation, self.recentDate)
        
        return summaryOfSelf
    
testRow = Row.createNewRow('Eggs')
print(testRow)
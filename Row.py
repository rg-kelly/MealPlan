from Sheets import main
from Purchase_History import Purchase_History
from Ingredient import Ingredient
from Store import Store
from WeekOfDate import WeekOfDate
from Amount_Units import Amount_Units

class Row:
    def __init__(self, itemName, average, recent, recentLocation, lowest, lowestLocation, highest, highestLocation):
        self.itemName = itemName
        self.average = average
        self.recent = recent
        self.recentLocation = recentLocation
        self.lowest = lowest
        self.lowestLocation = lowestLocation
        self.highest = highest
        self.highestLocation = highestLocation
        
    @classmethod
    def createNewRow(itemName):
        average, recent, recentLocation, lowest, lowestLocation, highest, highestLocation = Row.getPricePerUnit(itemName)
        
        return Row(itemName, average, recent, recentLocation, lowest, lowestLocation, highest, highestLocation)
    
    def getPricePerUnit(itemName):        
        recentOrderBy = "{}.{} DESC ".format(WeekOfDate.dateTable, WeekOfDate.dateNameColumn)
        lowestOrderBy = "{}.{} ASC ".format(Purchase_History.purchaseHistoryTable, Purchase_History.pricePerUnitColumn)
        highestOrderBy = "{}.{} DESC ".format(Purchase_History.purchaseHistoryTable, Purchase_History.pricePerUnitColumn)
        
        recentQuery = Row.getPricePerUnitQuery(itemName, recentOrderBy)
        lowestQuery = Row.getPricePerUnitQuery(itemName, lowestOrderBy)
        highestQuery = Row.getPricePerUnitQuery(itemName, highestOrderBy)
        
        return average, recent, recentLocation, lowest, lowestLocation, highest, highestLocation
    
    def getPricePerUnitQuery(itemName, orderBySpecifier):
        query = """SELECT {2}.{4}, {0}.{1}, {8}.{9}, {5}.{7}, {10}.{12}
                        FROM {0}
                        JOIN {2} ON {0}.{3} = {2}.{3}
                        JOIN {5} ON {5}.{6} = {0}.{6}
                        JOIN {8} ON {8}.{9} = {0}.{9}
                        JOIN {10} ON {10}.{11} = {0}.{11}
                        WHERE {2}.{4} = '{13}'
                        ORDER BY {14}
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
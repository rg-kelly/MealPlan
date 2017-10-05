from DataConnection import DataConnection
import Utilities

class Amount_Units:
    amountUnitsTable = "Amount_Units"
    unitIdColumn = "Unit_ID"
    unitNameColumn = "Unit_Name"
    matchIdColumn = "Match_ID"
    isPluralColumn = "is_Plural"
    
    isPluralIndicator = 1
    isSingularIndicator = 0
    
    pluralWhereClauseBeginning = "{} WHERE {} = ".format(amountUnitsTable, isPluralColumn)
    isPluralWhereClause = "{} {};".format(pluralWhereClauseBeginning, isPluralIndicator)
    isSingularWhereClause = "{} {};".format(pluralWhereClauseBeginning, isSingularIndicator)
    
    def __init__(self, unitId, unitName):
        self.unitId = unitId
        self.unitName = unitName
    
    def getSingularUnit(unitId = False, unitName = False):
        if unitName and not unitId:
            unitId = Utilities.getKnownInfo(unitName, Amount_Units.unitIdColumn, Amount_Units.unitNameColumn, Amount_Units.amountUnitsTable, False)
            if not unitId: return None
        
        isPlural = (Utilities.getKnownInfo(unitId, Amount_Units.isPluralColumn, Amount_Units.unitIdColumn, Amount_Units.amountUnitsTable, True) == 1)
        if isPlural:
            matchId = Utilities.getKnownInfo(unitId, Amount_Units.matchIdColumn, Amount_Units.unitIdColumn, Amount_Units.amountUnitsTable, True)
            if matchId:
                singularUnitName = Utilities.getKnownInfo(matchId, Amount_Units.unitNameColumn, Amount_Units.unitIdColumn, Amount_Units.amountUnitsTable, True)
                if singularUnitName:
                    return singularUnitName
                else: return None
            else: return None
        else:
            if unitName:
                return unitName
            elif unitId:
                return Utilities.getKnownInfo(unitId, Amount_Units.unitNameColumn, Amount_Units.unitIdColumn, Amount_Units.amountUnitsTable, True)

    def __str__(self):
        message = "Unit: " + self.unitsName
        
        return message

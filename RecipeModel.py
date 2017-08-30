from DataConnection import DataConnection
import Utilities

class Recipe:
    recipeTable = "Recipe"
    recipeElementTable = "Recipe_Element"
    recipeIdColumn = "Recipe_ID"
    recipeNameColumn = "Recipe_Name"
    amountNameColumn = "Amount"    
    
    typeTable = "Type"
    typeIdColumn = "Type_ID"
    typeNameColumn = "Type"
    
    mainTypeId = 1
    sideTypeId = 2
    otherTypeId = 3
    
    sideALabelPrefix = "side_A_"
    sideBLabelPrefix = "side_B_"    
    
    whereTypeId ="{0} WHERE {1} = {2} OR {1} = ".format(recipeTable, typeIdColumn, otherTypeId)
    whereMainTypeId = "{} {}".format(whereTypeId, str(mainTypeId))
    whereSideTypeId = "{} {}".format(whereTypeId, str(sideTypeId))

    def __init__(self, recipeId, recipeName, recipeType):
        self.recipeId = recipeId
        self.recipeName = recipeName
        self.recipeType = recipeType

    @classmethod
    def createNewRecipe(cls, recipeName, recipeType):       
        recipeId = Utilities.generateNewKey(Recipe.recipeIdColumn, Recipe.recipeTable)
        
        return Recipe(recipeId, recipeName, recipeType)
    
    @classmethod
    def getExistingRecipe(cls, recipeId, recipeName):
        if recipeId:
            known = recipeId
            select = Recipe.recipeNameColumn
            where = Recipe.recipeIdColumn
            whereIsId = True
        elif recipeName:
            known = recipeName
            select = Recipe.recipeIdColumn
            where = Recipe.recipeNameColumn
            whereIsId = False
        else:
            print("DEBUG: for some reason not setting vars for recipe '{}' id {}".format(recipeName, recipeId))
        
        recipeInfo = Utilities.getKnownInfo(known, select, where, Recipe.recipeTable, whereIsId)
        recipeType = Utilities.getKnownInfo(Utilities.getKnownInfo(known, Recipe.typeIdColumn, where, Recipe.recipeTable, whereIsId), Recipe.typeNameColumn, Recipe.typeIdColumn, Recipe.typeTable, True)
        
        if recipeId:            
            return Recipe(recipeId, recipeInfo, recipeType)
        elif recipeName:
            return Recipe(recipeInfo, recipeName, recipeType)

    def add(self):
        connection = DataConnection()
        
        query = "INSERT INTO {} ({}, {}, {}) VALUES (%s, %s, %s)".format(Recipe.recipeTable, Recipe.recipeIdColumn, Recipe.recipeNameColumn, Recipe.typeIdColumn)
        
        insertValues = (self.recipeId, self.recipeName, Utilities.getKnownInfo(self.recipeType, self.typeIdColumn, self.typeNameColumn, self.typeTable, False))
        connection.updateData(query, insertValues)
        connection.closeConnection()

        print("Successfully added " + "'" + self.recipeName + "' " + "recipe")

    def __str__(self):
        message = "--- Summary ---\n"
        message += "Recipe name: " + self.recipeName + "\n"
        message += "Recipe type: " + self.recipeType

        return message

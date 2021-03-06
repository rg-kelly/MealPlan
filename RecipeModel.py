from DataConnection import DataConnection
import Utilities
import Ingredient
from Amount_Units import Amount_Units
from sys import exc_info

class Recipe:
    recipeTable = "Recipe"
    recipeElementTable = "Recipe_Element"
    recipeIdColumn = "Recipe_ID"
    recipeNameColumn = "Recipe_Name"
    recipeDescriptionColumn = "Description"
    amountNameColumn = "Amount"    
    
    typeTable = "Type"
    typeIdColumn = "Type_ID"
    typeNameColumn = "Type"
    cookbookTypeIdColumn = "Cookbook_Type_ID"
    isCookbookColumn = "isCookbook"
    
    isNotCookbook = 0
    isCookbook = 1
    
    mainTypeId = 1
    sideTypeId = 2
    otherTypeId = 3
    
    sideALabelPrefix = "side_A_"
    sideBLabelPrefix = "side_B_"    
    
    whereTypeId ="{0} JOIN {5} ON {0}.{1} = {5}.{1} WHERE {5}.{3} = {4} AND ({0}.{1} = {2} OR {0}.{1} = ".format(recipeTable, typeIdColumn, otherTypeId, isCookbookColumn, isNotCookbook, typeTable)
    whereMainTypeId = "{} {})".format(whereTypeId, str(mainTypeId))
    whereSideTypeId = "{} {})".format(whereTypeId, str(sideTypeId))

    def __init__(self, recipeId, recipeName, recipeType, cookbookType, ingredients, description):
        self.recipeId = recipeId
        self.recipeName = Utilities.normalizeCasing(recipeName)
        self.recipeType = recipeType
        self.cookbookType = cookbookType
        self.ingredients = ingredients
        self.description = description

    @classmethod
    def createNewRecipe(cls, recipeName, recipeType, cookbookType, ingredients, description):       
        recipeId = Utilities.generateNewKey(Recipe.recipeIdColumn, Recipe.recipeTable)
        
        return Recipe(recipeId, recipeName, recipeType, cookbookType, ingredients, description)
    
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
        
        recipeInfo = Utilities.getKnownInfo(known, select, where, Recipe.recipeTable, whereIsId)
        recipeType = Utilities.getKnownInfo(Utilities.getKnownInfo(known, Recipe.typeIdColumn, where, Recipe.recipeTable, whereIsId), Recipe.typeNameColumn, Recipe.typeIdColumn, Recipe.typeTable, True)
        
        try:
            cookbookType = Utilities.getKnownInfo(Utilities.getKnownInfo(known, Recipe.cookbookTypeIdColumn, where, Recipe.recipeTable, whereIsId), Recipe.typeNameColumn, Recipe.typeIdColumn, Recipe.typeTable, True)
        except:
            cookbookType = "None"
        
        description = Utilities.getKnownInfo(known, Recipe.recipeDescriptionColumn, where, Recipe.recipeTable, whereIsId)
        if description == None: description = ""
        
        if recipeId:  
            ingredients = Ingredient.Ingredient.getRecipeIngredients(recipeId)
            return Recipe(recipeId, recipeInfo, recipeType, cookbookType, ingredients, description)
        elif recipeName:
            ingredients = Ingredient.Ingredient.getRecipeIngredients(recipeInfo)
            return Recipe(recipeInfo, recipeName, recipeType, cookbookType, ingredients, description)

    def add(self):
        connection = DataConnection()
        
        recipeQuery = "INSERT INTO {} ({}, {}, {}, {}, {}) VALUES (%s, %s, %s, %s, %s);".format(Recipe.recipeTable, Recipe.recipeIdColumn, Recipe.recipeNameColumn, Recipe.typeIdColumn, Recipe.cookbookTypeIdColumn, Recipe.recipeDescriptionColumn)
        recipeInsertValues = (self.recipeId, self.recipeName, Utilities.getKnownInfo(self.recipeType, self.typeIdColumn, self.typeNameColumn, self.typeTable, False), Utilities.getKnownInfo(self.cookbookType, self.typeIdColumn, self.typeNameColumn, self.typeTable, False), self.description)
        connection.updateData(recipeQuery, recipeInsertValues)
        
        self.insertIngredients(connection, returnQueryOnly=False)
        #for ingredient in self.ingredients:
            #ingredientId = Utilities.getKnownInfo(ingredient['name'], Ingredient.Ingredient.ingredientIdColumn, Ingredient.Ingredient.ingredientNameColumn, Ingredient.Ingredient.ingredientTable, False)
            #amount = ingredient['amount']
            #amountUnitId = Utilities.getKnownInfo(ingredient['units'], Amount_Units.unitIdColumn, Amount_Units.unitNameColumn, Amount_Units.amountUnitsTable, False)
            
            #bridgeQuery = "INSERT INTO {} ({}, {}, {}, {}) VALUES (%s, %s, %s, %s); ".format(Recipe.recipeElementTable, Recipe.recipeIdColumn, Ingredient.Ingredient.ingredientIdColumn, Recipe.amountNameColumn, Amount_Units.unitIdColumn)
            #bridgeInsertValues = (self.recipeId, ingredientId, amount, amountUnitId)        
            #connection.updateData(bridgeQuery, bridgeInsertValues)
        
        connection.closeConnection()
        print("Successfully added " + "'" + self.recipeName + "' " + "recipe.")
        
    def update(self, newRecipeName, newRecipeType, newCookbookType, newIngredientsList, newDescription, updateIngredients = True):
        queryList = []
        insertValues = []
        updateStatus = False
        
        if self.recipeName != newRecipeName:
            self.recipeName = newRecipeName
            queryList.append("UPDATE {} SET {} = %s WHERE {} = {};".format(Recipe.recipeTable, Recipe.recipeNameColumn, Recipe.recipeIdColumn, self.recipeId))
            insertValues.append((self.recipeName,))
        if self.recipeType != newRecipeType:
            self.recipeType = newRecipeType
            queryList.append("UPDATE {} SET {} = %s WHERE {} = {};".format(Recipe.recipeTable, Recipe.typeIdColumn, Recipe.recipeIdColumn, self.recipeId))
            insertValues.append((Utilities.getKnownInfo(self.recipeType, Recipe.typeIdColumn, Recipe.typeNameColumn, Recipe.typeTable, False),))
        if self.cookbookType != newCookbookType:
            self.cookbookType = newCookbookType
            queryList.append("UPDATE {} SET {} = %s WHERE {} = {};".format(Recipe.recipeTable, Recipe.cookbookTypeIdColumn, Recipe.recipeIdColumn, self.recipeId))
            insertValues.append((Utilities.getKnownInfo(self.cookbookType, Recipe.typeIdColumn, Recipe.typeNameColumn, Recipe.typeTable, False),))
        if self.description != newDescription:
            self.description = newDescription
            
            if newDescription is not None:
                queryList.append("UPDATE {} SET {} = %s WHERE {} = {};".format(Recipe.recipeTable, Recipe.recipeDescriptionColumn, Recipe.recipeIdColumn, self.recipeId))
                insertValues.append((self.description,))
        if updateIngredients:
            self.ingredients = newIngredientsList
            ingredientsQueryList, ingredientInsertValues = self.insertIngredients(None, returnQueryOnly=True)
            queryList.append("DELETE FROM {} WHERE {} = %s;".format(Recipe.recipeElementTable, Recipe.recipeIdColumn))
            insertValues.append((self.recipeId,))
            
            for count in range(len(ingredientsQueryList)):
                queryList.append(ingredientsQueryList[count])
                insertValues.append(ingredientInsertValues[count])
    
        try:
            for element in range(len(queryList)):
                query = queryList[element]
                values = insertValues[element]
                
                connection = DataConnection()
                connection.updateData(query, values)
                connection.closeConnection()
                
                updateStatus = True
        except:
            updateStatus = exc_info()

        return updateStatus
    
    def delete(self):
        recipeElementQuery = "DELETE FROM {} WHERE {} = %s;".format(Recipe.recipeElementTable, Recipe.recipeIdColumn)
        recipeQuery = "DELETE FROM {} WHERE {} = %s;".format(Recipe.recipeTable, Recipe.recipeIdColumn)
        bindValue = (self.recipeId,)
        
        try:
            connection = DataConnection()
            connection.updateData(recipeElementQuery, bindValue)
            connection.updateData(recipeQuery, bindValue)
            connection.closeConnection()
            
            return True
        except:
            return exc_info()
    
    def insertIngredients(self, connectionInstance, returnQueryOnly = False):
        bridgeQueryList = []
        bridgeInsertTupleList = []
        
        for ingredient in self.ingredients:
            ingredientId = Utilities.getKnownInfo(ingredient['name'], Ingredient.Ingredient.ingredientIdColumn, Ingredient.Ingredient.ingredientNameColumn, Ingredient.Ingredient.ingredientTable, False)
            amount = ingredient['amount']
            amountUnitId = Utilities.getKnownInfo(ingredient['units'], Amount_Units.unitIdColumn, Amount_Units.unitNameColumn, Amount_Units.amountUnitsTable, False)
            
            bridgeQuery = "INSERT INTO {} ({}, {}, {}, {}) VALUES (%s, %s, %s, %s); ".format(Recipe.recipeElementTable, Recipe.recipeIdColumn, Ingredient.Ingredient.ingredientIdColumn, Recipe.amountNameColumn, Amount_Units.unitIdColumn)
            bridgeInsertValues = (self.recipeId, ingredientId, amount, amountUnitId)
            if not returnQueryOnly:
                connectionInstance.updateData(bridgeQuery, bridgeInsertValues)
            else:
                bridgeQueryList.append(bridgeQuery)
                bridgeInsertTupleList.append((bridgeInsertValues))
            
        if returnQueryOnly:
            return bridgeQueryList, bridgeInsertTupleList

    def __str__(self):
        newLine = "\n"
        tab = "   "        
        
        message = "--- Summary ---" + newLine
        message += "Recipe name: " + self.recipeName + newLine
        message += "Recipe type: " + str(self.recipeType) + newLine
        message += "Cookbook type: " + str(self.cookbookType) + newLine
        
        if self.ingredients:
            message += "Ingredients: " + newLine
            for ingredient in self.ingredients:
                message += "{} {} {} {} {}".format(tab, ingredient['amount'], ingredient['units'], ingredient['name'], newLine)
        else:
            message += "Ingredients: None" + newLine
        
        message += "Description: " + str(self.description)

        return message
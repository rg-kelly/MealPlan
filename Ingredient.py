from DataConnection import DataConnection
import Utilities
from RecipeModel import *
from Amount_Units import Amount_Units

class Ingredient:
    ingredientTable = "Ingredient"

    ingredientIdColumn = "Ingredient_ID"
    ingredientNameColumn = "Ingredient_Name"

    def __init__(self, ingredientName):
        self.ingredientName = ingredientName     

    def getRecipeIngredients(recipeIdNumber): # Method for returning ingredient information from the database
        ingredientList = []
        
        connection = DataConnection()        
        query = """SELECT {6}.{0}, {4}.{1}, {9}.{2}
                    FROM {3} JOIN {4} ON {3}.{5} = {4}.{5}
                    JOIN {6} ON {6}.{7} = {4}.{7}
                    JOIN {9} ON {9}.{10} = {4}.{10}
                    WHERE {3}.{5} = {8};""".format(Ingredient.ingredientNameColumn,
                                                   Recipe.amountNameColumn,
                                                   Amount_Units.unitNameColumn,
                                                   Recipe.recipeTable,
                                                   Recipe.recipeElementTable,
                                                   Recipe.recipeIdColumn,
                                                   Ingredient.ingredientTable,
                                                   Ingredient.ingredientIdColumn,
                                                   recipeIdNumber,
                                                   Amount_Units.amountUnitsTable,
                                                   Amount_Units.unitIdColumn)

        ingredientsResult = connection.runQuery(query)
        ingredientsResultList = ingredientsResult.fetchall()
        connection.closeConnection()

        if ingredientsResultList:
            for item in ingredientsResultList:
                ingredientList += [[str(item[Ingredient.amountPosition]), item[Ingredient.unitsPosition], item[Ingredient.ingredientNamePosition]]]
            return ingredientList
        else: return None

    def add(self):
        connection = DataConnection()
        query = "INSERT INTO {0} ({1}) VALUES (%s);".format(Ingredient.ingredientTable, Ingredient.ingredientNameColumn)
        insertValue = (self.ingredientName,)
        connection.updateData(query, insertValue)
        connection.closeConnection

    def __str__(self):
        message = "Ingredient name: " + self.ingredientName

        return message

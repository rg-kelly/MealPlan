from DataConnection import DataConnection
import Utilities
import RecipeModel
from Amount_Units import Amount_Units

class Ingredient:
    ingredientTable = "Ingredient"

    ingredientIdColumn = "Ingredient_ID"
    ingredientNameColumn = "Ingredient_Name"
    amountOnHandColumn = "Amount_On_Hand"

    def __init__(self, ingredientName, averagePricePerUnit = 1.00):
        self.ingredientName = ingredientName     
        self.averagePricePerUnit = averagePricePerUnit
        #self.amountOnHand = amountOnHand

    def getRecipeIngredients(recipeIdNumber): # Method for returning ingredient information from the database
        ingredients = []

        connection = DataConnection()        
        query = """SELECT {6}.{0}, {4}.{1}, {9}.{2}
                    FROM {3} JOIN {4} ON {3}.{5} = {4}.{5}
                    JOIN {6} ON {6}.{7} = {4}.{7}
                    JOIN {9} ON {9}.{10} = {4}.{10}
                    WHERE {3}.{5} = {8};""".format(Ingredient.ingredientNameColumn,
                                                   RecipeModel.Recipe.amountNameColumn,
                                                   Amount_Units.unitNameColumn,
                                                   RecipeModel.Recipe.recipeTable,
                                                   RecipeModel.Recipe.recipeElementTable,
                                                   RecipeModel.Recipe.recipeIdColumn,
                                                   Ingredient.ingredientTable,
                                                   Ingredient.ingredientIdColumn,
                                                   recipeIdNumber,
                                                   Amount_Units.amountUnitsTable,
                                                   Amount_Units.unitIdColumn)

        ingredientsResult = connection.runQuery(query)
        ingredientsResultList = ingredientsResult.fetchall()
        ingredientsResult.close()
        connection.closeConnection()

        if ingredientsResultList:
            for item in ingredientsResultList:
                ingredients.append({'name': item[0], 'amount': item[1], 'units': item[2]})
        
        return ingredients       
    
    def getAllIngredients():
        ingredientsList = []
        connection = DataConnection()
        query = "SELECT {} FROM {};".format(Ingredient.ingredientNameColumn, Ingredient.ingredientTable)
        ingredientsListResult = (connection.runQuery(query)).fetchall()
        connection.closeConnection()
        
        for ingredient in ingredientsListResult:
            ingredientsList.append(ingredient[0])
        
        return ingredientsList
    
    def add(self):
        connection = DataConnection()
        query = "INSERT INTO {0} ({1}) VALUES (%s);".format(Ingredient.ingredientTable, Ingredient.ingredientNameColumn)
        insertValue = (self.ingredientName,)
        connection.updateData(query, insertValue)
        connection.closeConnection

    def __str__(self):
        message = "Ingredient name: " + self.ingredientName

        return message
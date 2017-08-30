from DataConnection import DataConnection
import Utilities
from RecipeModel import *

class Ingredient:
    ingredientTable = "Ingredient"

    ingredientIdColumn = "Ingredient_ID"
    ingredientNameColumn = "Ingredient_Name"

    def __init__(self, ingredientId, ingredientName):
        self.ingredientId = ingredientId
        self.ingredientName = ingredientName

    @classmethod
    def createNewIngredient(cls, ingredientName):
        ingredientId = Utilities.generateNewKey(Ingredient.ingredientIdColumn, Ingredient.ingredientTable)
        
        return Ingredient(ingredientId, ingredientName)

    #@classmethod
    #def collectIngredientInfo(cls): # Method for collecting ingredient information from user
        #print("Enter the names of the required ingredients.") # Instructions for entering ingredient information
        #print("After you type the ingredient name, you will be prompted to enter the required amount for that ingredient.")
        #print("Type 'done' when finished entering all the ingredients.")
        
        #ingredientList = []
        #count = 1
        #done = False
        
        #while not done:
            #ingredientName = input("Ingredient #" + str(count) + ": ")

            #if (ingredientName == 'done'): done = True
            #else:           
                #entireElement = input("Enter the required amount for " + ingredientName + " (e.g. 1 cup): ")
                #ingredientList += [[entireElement, ingredientName]]     # Add the input amount/units and ingredient name to list as a list (list within a list format)
                #count += 1
                
        #return ingredientList      

    @classmethod
    def getExistingIngredients(cls, recipeIdNumber): # Method for returning ingredient information from the database
        ingredientList = []
        ingredientNamePosition = 0
        elementAmountPosition = 1
        elementUnitsPosition = 2
        
        connection = DataConnection()

        query = "SELECT I." + Ingredient.ingredientNameColumn + ", E." + Recipe.Recipe.elementAmountColumn + ", E." + Recipe.Recipe.elementUnitsColumn
        query += " FROM " + Recipe.Recipe.recipeTable + " AS R JOIN " + Recipe.Recipe.elementTable + " AS E ON R." + Recipe.Recipe.recipeIdColumn
        query += " = E." + Recipe.Recipe.recipeIdColumn + " JOIN " + Ingredient.ingredientTable + " AS I ON I." + Ingredient.ingredientIdColumn
        query += " = E." + Ingredient.ingredientIdColumn + " WHERE R." + Recipe.Recipe.recipeIdColumn + " = " + str(recipeIdNumber)

        ingredientsResult = connection.runQuery(query)
        ingredientsResultList = ingredientsResult.fetchall()
        connection.closeConnection()

        if ingredientsResultList:
            for item in ingredientsResultList:
                ingredientList += [[str(item[elementAmountPosition]) + " " + item[elementUnitsPosition], item[ingredientNamePosition]]]
            return ingredientList
        else: return None

    def add(self):
        connection = DataConnection()

        query = "INSERT INTO " + Ingredient.ingredientTable + "(" + Ingredient.ingredientIdColumn + ", " + Ingredient.ingredientNameColumn + ") "
        query += "VALUES (%s, %s)"

        insertValues = (self.ingredientId, self.ingredientName)
        connection.updateData(query, insertValues)
        connection.closeConnection      

    def __str__(self):
        message = "Ingredient name: " + self.ingredientName

        return message

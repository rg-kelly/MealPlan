from Sheets import addRowToSheet
from Row import Row
from Ingredient import Ingredient

class Report:
    def createNewReport(cls):
        ingredientsList = Ingredient.getAllIngredients()
        
        for ingredient in ingredientsList:
            row = Row.createNewRow(ingredient)
            addRowToSheet(row) #TODO: row is not in right form right now, needs to be list... either create list at Row level or this point...
from Sheets import addToSheet
from Row import Row
from Ingredient import Ingredient

class Report:
    def createNewReport():
        ingredientsList = Ingredient.getAllIngredients()
        rowList = []
        
        for ingredient in ingredientsList:
            row = Row.createNewRow(ingredient)
            rowList.append(Row.getRowList(row))
        
        #print(rowList)
        addToSheet(rowList)
        print("Done writing to sheet.")

report = Report.createNewReport()

# Issues:
# - 'non-convertible' units like unit, piece, strip and pint
# - need to handle units not being same for all price types, not just avg
#   because otherwise the diff of units makes max/min not accurate

from appJar import gui
from RecipeModel import *
from AddView import addItem
from Utilities import listOptions

daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
newRecipeLabel = "Recipe Name"
recipeTypeLabel = "Recipe Type"
dateEntryLabel = "Week Of: "

headingRow = 0
defaultRow = 0
defaultColumn = 0
dateRow = headingRow + 1
typeHeadingRow = headingRow + 2
submitRow = typeHeadingRow + 10

def configureGui(app, handleOptionBox, press):
    recipeNameMaxLength = 50

    #app.startTabbedFrame("recipeTabbedFrame")
    #app.startTab("Recipes")

    app.startTabbedFrame("recipeSubtabbedFrame")
    app.startTab("Add Recipes")
    addItem(recipeNameMaxLength, "Recipe", app, press)
    handleOptionBox(recipeTypeLabel, "add", Recipe.typeNameColumn, Recipe.typeTable, 1, 2)
    app.stopTab()

    app.startTab("Assign Recipes")
    app.addLabel("assignRecipesTitle", "Assign Recipes", row = headingRow, column = 0, colspan = 4)
    
    app.addLabelEntry(dateEntryLabel, row = dateRow, column = 0) # TODO Change this to editable drop down
    app.setEntryDefault(dateEntryLabel, "yyyy-mm-dd")
    app.addButton("Go", press, row = dateRow, column = 1)
    
    rowCount = typeHeadingRow + 1
    #for day in daysOfWeek:
        #handleOptionBox(day, "add", Recipe.recipeNameColumn, Recipe.whereMainTypeId, row = rowCount, column = 0)
        #handleOptionBox(Recipe.sideALabelPrefix + day, "add", Recipe.recipeNameColumn, Recipe.whereSideTypeId, row = rowCount, column = 1)
        #handleOptionBox(Recipe.sideBLabelPrefix + day, "add", Recipe.recipeNameColumn, Recipe.whereSideTypeId, row = rowCount, column = 2)
        #rowCount += 1
    
    #app.stopTab()
    #app.stopTabbedFrame()

    #app.stopTab()
    #app.stopTabbedFrame()
    
    app.setTabbedFrameSelectedTab("recipeSubtabbedFrame", "Assign Recipes")

from appJar import gui
from RecipeModel import *
from WeekOfDate import *
from DayAssignment import DayAssignment
from AddView import addItem
from Utilities import listOptions
from Settings import Settings
from Amount_Units import Amount_Units
from Ingredient import Ingredient
from Store import Store
from ast import literal_eval

daysOfWeek = listOptions(DayAssignment.dayNameColumn, DayAssignment.dayTable, True, "ORDER BY {} ASC".format(DayAssignment.dayIdColumn))
newRecipeLabel = "Recipe Name "
recipeTypeLabel = "Recipe Type "
recipeCookbookTypeLabel = "Cookbook Type "
dateEntryLabel = "Week Of: "
newDateEntryLabel = "Add: "
noneButtonLabel = "None"
newIngredientLabel = "Ingredient Name "
startLabelDinner = "Start: "
endLabelDinner = "End: "
updateCheckBoxLabel = "Update"
recipeTextBoxLabel = "recipeTextBoxLabel"
amountUnitsLabel = "Unit "
amountEntryLabel = "Amount "
ingredientSelectionPriceLabel = "Ingredient: "
storeSelectionLabel = "Store: "
amountPaidLabel = "$"
amountPurchasedLabel = "Amount: "
amountPurchasedUnitsLabel = "Unit"
updateRecipeLabel = "Recipe Selection"
recipeTypeLabelUpdate = "Recipe Type: "
recipeCookbookTypeLabelUpdate = "Cookbook Type: "
recipeTextBoxLabelUpdate = "updateRecipeTextBoxLabel"
amountUnitsLabelUpdate = "Update Unit "
amountEntryLabelUpdate = "Amount  "
ingredientEntryLabel = "IngredientEntryLabel"

addRecipesTab = "Add Recipe"
assignRecipesTab = "Assign Recipes"
enterPricesTab = "Enter Prices"
updateRecipesTab = "Update Recipe"

headingRow = 0
defaultRow = 0
defaultColumn = 0
dateRow = headingRow + 1
typeHeadingRow = headingRow + 2
submitRow = typeHeadingRow + 10

dateSelectionColumn = 0
newDateEntryColumn = dateSelectionColumn + 1
goButtonColumn = newDateEntryColumn + 1

### Settings values from DB ###
dinnerKey = 'dinner'
startKey = 'start'
endKey = 'end'
updateKey = 'update_calendar'
currentSettings = Settings.getExistingSettings()
startTime = currentSettings.settingDictionary[dinnerKey][startKey]
endTime = currentSettings.settingDictionary[dinnerKey][endKey]
updateCalendar = currentSettings.settingDictionary[updateKey]
###############################

def configureGui(app, handleOptionBox, press):
    recipeNameMaxLength = 50

    app.startTabbedFrame("recipeSubtabbedFrame")
    app.startTab("Calendar Settings")
    app.addCheckBox(updateCheckBoxLabel)
    app.setCheckBox(updateCheckBoxLabel, ticked=updateCalendar, callFunction=False)
    app.addLabel("dinnerSettingsLabel","Dinner Settings")
    app.addLabelEntry(startLabelDinner)
    app.setEntry(startLabelDinner, "{}".format(startTime))
    app.addLabelEntry(endLabelDinner)
    app.setEntry(endLabelDinner, "{}".format(endTime))
    app.addButton("Update", press)
    app.stopTab()
    
    pricesColumnStart = defaultColumn
    app.startTab(enterPricesTab)
    app.addLabel(enterPricesTab, enterPricesTab, row = headingRow, column = pricesColumnStart, colspan = 4)
    handleOptionBox(ingredientSelectionPriceLabel, "add", Ingredient.ingredientNameColumn, Ingredient.ingredientTable, row = headingRow + 1, column = pricesColumnStart)
    app.addLabelEntry(amountPurchasedLabel, row = headingRow + 1, column = pricesColumnStart + 1)
    handleOptionBox(amountPurchasedUnitsLabel, "add", Amount_Units.unitNameColumn, Amount_Units.amountUnitsTable, row = headingRow + 1, column = pricesColumnStart + 2)
    app.addLabelEntry(amountPaidLabel, row = headingRow + 2, column = pricesColumnStart)
    handleOptionBox(storeSelectionLabel, "add", Store.storeNameColumn, Store.storeTable, row = headingRow + 2, column = pricesColumnStart + 1)
    app.setOptionBox(storeSelectionLabel, "Valley West Hy-Vee")
    app.setFocus(amountPurchasedLabel)
    app.addButton("Enter", press, row = headingRow + 4, column = pricesColumnStart, colspan = 3)
    app.stopTab()
    
    app.startTab(addRecipesTab)
    addItem(recipeNameMaxLength, "Recipe", app, press, bottomButton=True)
    handleOptionBox(recipeTypeLabel, "add", Recipe.typeNameColumn, Recipe.typeTable + " WHERE {0} = {1}".format(Recipe.isCookbookColumn, Recipe.isNotCookbook), 1, 2)    
    handleOptionBox(recipeCookbookTypeLabel, "add", Recipe.typeNameColumn, Recipe.typeTable + " WHERE {0} = {1}".format(Recipe.isCookbookColumn, Recipe.isCookbook), 1, 3)
    app.setOptionBox(recipeCookbookTypeLabel, "None")
    addItem(recipeNameMaxLength, "Ingredient", app, press, rowStart=2, columnStart=1, bottomButton=False, isFirstAdd=False)
    app.addLabelEntry(amountEntryLabel, row=3, column=2)
    handleOptionBox(amountUnitsLabel, "add", Amount_Units.unitNameColumn, Amount_Units.amountUnitsTable, 3, 3)
    app.addScrolledTextArea(recipeTextBoxLabel, row = 5, colspan = 4)
    app.stopTab()
    
    updateRecipeColumnStart = defaultColumn
    app.startTab(updateRecipesTab)
    app.addLabel(updateRecipesTab, updateRecipesTab, row = headingRow, column = updateRecipeColumnStart, colspan = 4)
    handleOptionBox(updateRecipeLabel, "add", Recipe.recipeNameColumn, Recipe.recipeTable, row = headingRow + 1, column = updateRecipeColumnStart + 1) # what if you want to change the name of the recipe? or delete it?
    app.addNamedButton("Go", "Update Go", press, row = headingRow + 1, column = updateRecipeColumnStart + 2)
    app.addHorizontalSeparator(row = headingRow + 2, colspan = 4)
    handleOptionBox(recipeTypeLabelUpdate, "add", Recipe.typeNameColumn, Recipe.typeTable + " WHERE {0} = {1}".format(Recipe.isCookbookColumn, Recipe.isNotCookbook), row = headingRow + 3, column = updateRecipeColumnStart)    
    handleOptionBox(recipeCookbookTypeLabelUpdate, "add", Recipe.typeNameColumn, Recipe.typeTable + " WHERE {0} = {1}".format(Recipe.isCookbookColumn, Recipe.isCookbook), row = headingRow + 3, column = updateRecipeColumnStart + 1)
    app.addScrolledTextArea(recipeTextBoxLabelUpdate, row = headingRow + 4, colspan = 4)
    app.addLabel("Ingredient(s)", "Ingredient(s)", row = headingRow + 7, column = updateRecipeColumnStart, colspan = 1)
    app.addEntry(ingredientEntryLabel, row = headingRow + 8, column = updateRecipeColumnStart, colspan = 2)
    app.addLabelEntry(amountEntryLabelUpdate, row = headingRow + 8, column = updateRecipeColumnStart + 2)
    handleOptionBox(amountUnitsLabelUpdate, "add", Amount_Units.unitNameColumn, Amount_Units.amountUnitsTable, row = headingRow + 8, column = updateRecipeColumnStart + 3)
    app.addNamedButton("Update", "Recipe Update", press, row = headingRow + 9, column = updateRecipeColumnStart + 1)
    app.addButton("Delete", press, row = headingRow + 9, column = updateRecipeColumnStart + 2)
    app.stopTab()

    app.startTab(assignRecipesTab)
    app.addLabel(assignRecipesTab, assignRecipesTab, row = headingRow, column = 0, colspan = 4)
    handleOptionBox(dateEntryLabel, "add", WeekOfDate.dateNameColumn, WeekOfDate.dateTable, dateRow, dateSelectionColumn)
    app.addLabelEntry(newDateEntryLabel, row = dateRow, column = newDateEntryColumn)
    app.setEntryDefault(newDateEntryLabel, "yyyy-mm-dd")
    app.addButton("Go", press, row = dateRow, column = goButtonColumn)
    
    app.setTabbedFrameSelectedTab("recipeSubtabbedFrame", updateRecipesTab)

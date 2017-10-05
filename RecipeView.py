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
weekOfDatePurchaseSelectionLabel = "WoD: "
updateRecipeLabel = "Recipe Selection"
ingredientEntryLabel = "IngredientEntryLabel"
recipeSelectionLabel = "Recipe: "
newRecipeEntryLabel = "New: "
recipeGoAgainButton = "Recipe Go Again"
ingredientAddButton = "Add Button Ingredient"
configureIngredientsButton = "Configure Ingredients"
ingredientsWindowTitle = configureIngredientsButton
ingredientsDoneButton = "Done"

addRecipesTab = "Recipes"
assignRecipesTab = "Meal Plan"
enterPricesTab = "Enter Prices"

recipeSelectionColumn = 0
newRecipeColumn = recipeSelectionColumn + 1
goButtonColumn = newRecipeColumn + 1
headingRow = 0
defaultRow = 0
defaultColumn = 0
dateRow = headingRow + 1
typeHeadingRow = headingRow + 2
submitRow = typeHeadingRow + 10
pricesColumnStart = defaultColumn

dateSelectionColumn = 0
newDateEntryColumn = dateSelectionColumn + 1
goButtonColumn = newDateEntryColumn + 1

ingredientStartRow = headingRow + 1

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
    app.startTab("Settings")
    app.addCheckBox(updateCheckBoxLabel)
    app.setCheckBox(updateCheckBoxLabel, ticked=updateCalendar, callFunction=False)
    app.addLabel("dinnerSettingsLabel","Dinner Settings")
    app.addLabelEntry(startLabelDinner)
    app.setEntry(startLabelDinner, "{}".format(startTime))
    app.addLabelEntry(endLabelDinner)
    app.setEntry(endLabelDinner, "{}".format(endTime))
    app.addButton("Update", press)
    app.stopTab()
    
    app.startTab(enterPricesTab)
    app.addLabel(enterPricesTab, enterPricesTab, row = headingRow, column = pricesColumnStart, colspan = 4)
    handleOptionBox(ingredientSelectionPriceLabel, "add", Ingredient.ingredientNameColumn, Ingredient.ingredientTable, row = headingRow + 1, column = pricesColumnStart)
    app.addLabelEntry(amountPurchasedLabel, row = headingRow + 1, column = pricesColumnStart + 1)
    handleOptionBox(amountPurchasedUnitsLabel, "add", Amount_Units.unitNameColumn, Amount_Units.isSingularWhereClause, row = headingRow + 1, column = pricesColumnStart + 2)
    app.addLabelEntry(amountPaidLabel, row = headingRow + 2, column = pricesColumnStart)
    handleOptionBox(storeSelectionLabel, "add", Store.storeNameColumn, Store.storeTable, row = headingRow + 2, column = pricesColumnStart + 1)
    handleOptionBox(weekOfDatePurchaseSelectionLabel, "add", WeekOfDate.dateNameColumn, WeekOfDate.dateTable, row = headingRow + 2, column = pricesColumnStart + 2)
    app.setOptionBox(storeSelectionLabel, "Valley West Hy-Vee")
    app.setFocus(amountPurchasedLabel)
    app.addButton("Enter", press, row = headingRow + 4, column = pricesColumnStart, colspan = 3)
    app.stopTab()
    
    app.startTab(addRecipesTab)
    app.addLabel(addRecipesTab, addRecipesTab, row = headingRow, column = 0, colspan = 4)
    handleOptionBox(recipeSelectionLabel, "add", Recipe.recipeNameColumn, Recipe.recipeTable, dateRow, recipeSelectionColumn)
    app.addLabelEntry(newRecipeEntryLabel, row = dateRow, column = newRecipeColumn)
    app.addNamedButton( "Go", recipeGoAgainButton, press, row = dateRow, column = goButtonColumn)
    app.stopTab()

    app.startTab(assignRecipesTab)
    app.addLabel(assignRecipesTab, assignRecipesTab, row = headingRow, column = 0, colspan = 4)
    handleOptionBox(dateEntryLabel, "add", WeekOfDate.dateNameColumn, WeekOfDate.dateTable, dateRow, dateSelectionColumn)
    app.addLabelEntry(newDateEntryLabel, row = dateRow, column = newDateEntryColumn)
    app.setEntryDefault(newDateEntryLabel, "yyyy-mm-dd")
    app.addButton("Go", press, row = dateRow, column = goButtonColumn)
    
    app.setTabbedFrameSelectedTab("recipeSubtabbedFrame", enterPricesTab)
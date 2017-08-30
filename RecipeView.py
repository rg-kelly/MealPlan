from appJar import gui
from RecipeModel import *
from WeekOfDate import *
from DayAssignment import DayAssignment
from AddView import addItem
from Utilities import listOptions
from Settings import Settings
from ast import literal_eval

daysOfWeek = listOptions(DayAssignment.dayNameColumn, DayAssignment.dayTable, True, "ORDER BY {} ASC".format(DayAssignment.dayIdColumn))
newRecipeLabel = "Recipe Name"
recipeTypeLabel = "Recipe Type"
dateEntryLabel = "Week Of: "
newDateEntryLabel = "Add: "
noneButtonLabel = "None"

headingRow = 0
defaultRow = 0
defaultColumn = 0
dateRow = headingRow + 1
typeHeadingRow = headingRow + 2
submitRow = typeHeadingRow + 10

dateSelectionColumn = 0
newDateEntryColumn = dateSelectionColumn + 1
goButtonColumn = newDateEntryColumn + 1

startLabelDinner = "Start: "
endLabelDinner = "End: "
updateCheckBoxLabel = "Update"
recipeTextBoxLabel = "recipeTextBoxLabel"

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
    
    app.startTab("Add Recipes")
    addItem(recipeNameMaxLength, "Recipe", app, press)
    handleOptionBox(recipeTypeLabel, "add", Recipe.typeNameColumn, Recipe.typeTable, 1, 2)    
    addItem(recipeNameMaxLength, "Ingredient", app, press, rowStart=2, columnStart=1)
    app.addLabelEntry("Amount", row=3, column=2)
    app.addScrolledTextArea(recipeTextBoxLabel, row = 5, colspan = 4)
    app.stopTab()

    app.startTab("Assign Recipes")
    app.addLabel("assignRecipesTitle", "Assign Recipes", row = headingRow, column = 0, colspan = 4)

    handleOptionBox(dateEntryLabel, "add", WeekOfDate.dateNameColumn, WeekOfDate.dateTable, dateRow, dateSelectionColumn)
    app.addLabelEntry(newDateEntryLabel, row = dateRow, column = newDateEntryColumn)
    app.setEntryDefault(newDateEntryLabel, "yyyy-mm-dd")
    app.addButton("Go", press, row = dateRow, column = goButtonColumn)
    
    app.setTabbedFrameSelectedTab("recipeSubtabbedFrame", "Add Recipes")

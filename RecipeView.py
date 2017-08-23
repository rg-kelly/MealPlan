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

### Settings values from DB ###
dinnerKey = 'dinner'
startKey = 'start'
endKey = 'end'
dinnerTimeSetting = Settings.getExistingSetting(dinnerKey)
startTime = dinnerTimeSetting.settingDictionary[dinnerKey][startKey]
endTime = dinnerTimeSetting.settingDictionary[dinnerKey][endKey]

updateKey = 'update_calendar'
updateCalendarSetting = Settings.getExistingSetting(updateKey)
updateCalendar = literal_eval(updateCalendarSetting.settingDictionary[updateKey])
###############################

def configureGui(app, handleOptionBox, press):
    recipeNameMaxLength = 50

    app.startTabbedFrame("recipeSubtabbedFrame")
    app.startTab("Calendar Settings")
    app.addCheckBox(updateCheckBoxLabel)
    app.setCheckBox(updateCheckBoxLabel, ticked=updateCalendar, callFunction=False) # TODO Store in db
    app.addLabel("dinnerSettingsLabel","Dinner Settings")
    app.addLabelEntry(startLabelDinner)
    app.setEntry(startLabelDinner, "{}".format(startTime)) # TODO Store in db
    app.addLabelEntry(endLabelDinner)
    app.setEntry(endLabelDinner, "{}".format(endTime)) # TODO Store in db
    app.addButton("Update", press)
    app.stopTab()
    
    app.startTab("Add Recipes")
    addItem(recipeNameMaxLength, "Recipe", app, press)
    handleOptionBox(recipeTypeLabel, "add", Recipe.typeNameColumn, Recipe.typeTable, 1, 2)
    app.stopTab()

    app.startTab("Assign Recipes")
    app.addLabel("assignRecipesTitle", "Assign Recipes", row = headingRow, column = 0, colspan = 4)

    handleOptionBox(dateEntryLabel, "add", WeekOfDate.dateNameColumn, WeekOfDate.dateTable, dateRow, dateSelectionColumn)
    app.addLabelEntry(newDateEntryLabel, row = dateRow, column = newDateEntryColumn)
    app.setEntryDefault(newDateEntryLabel, "yyyy-mm-dd")
    app.addButton("Go", press, row = dateRow, column = goButtonColumn)
    
    app.setTabbedFrameSelectedTab("recipeSubtabbedFrame", "Assign Recipes")

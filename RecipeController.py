from appJar import gui
from RecipeModel import *
from RecipeView import *
from DayAssignment import DayAssignment
from Utilities import *
import Calendar
from datetime import datetime
from datetime import timedelta
from WeekOfDate import WeekOfDate

app = gui("Meal Plan Configuration")
dateFormat = "%Y-%m-%d" 

def addRecipe(recipeName, recipeType):
    recipe = Recipe.createNewRecipe(recipeName, recipeType)
    recipe.add()

def handleOptionBox(labelName, actionType, nameColumn, tableName, row = defaultRow, column = defaultColumn):
    optionsList = listOptions(nameColumn, tableName, True)
    isAdd = (actionType == "add")
    isUpdate = (actionType == "update")
    isSide = (labelName.__contains__("side"))

    if nameColumn == Recipe.recipeNameColumn:
        optionsList = DayAssignment.updateRecipeList(getDateEntry(), labelName, optionsList, isSide)        
    if nameColumn == WeekOfDate.dateNameColumn:
        optionsList.insert(0, "New")

    if isUpdate:
        app.changeOptionBox(labelName, optionsList)
    elif isAdd:        
        if isSide:
            app.addOptionBox(labelName, optionsList, row, column)
        else:
            app.addLabelOptionBox(labelName, optionsList, row, column)

def validateDateEntry(dateInput):
    try:
        datetime.strptime(dateInput, dateFormat)
        return True
    except ValueError:
        return False
    finally:
        return False

def getDateEntry(notifyIfNew = False):
    selection = app.getOptionBox(dateEntryLabel)
    entry = app.getEntry(newDateEntryLabel)
    
    if selection == "New":
        if entry == "":
            entry = datetime.strftime(WeekOfDate.findClosestWeekOfDate(), dateFormat)
            app.setOptionBox(dateEntryLabel, entry)
        dateEntry = entry
    else:
        dateEntry = selection
    
    dateIsValid = validateDateEntry(dateEntry)
    if dateIsValid:
        if not notifyIfNew:
            return dateEntry
        else:
            return dateEntry, True
    else:
        errorMessage = "Date entered ({}) is incorrect. Ensure it is formatted like YYYY-MM-DD and is a legitimate calendar date.".format(dateEntry)
        app.errorBox("ERROR", errorMessage)
        app.clearEntry(newDateEntryLabel)
        raise Exception(errorMessage)

def press(btn):
    if btn == "Cancel":
        app.stop()
    elif btn == "Add":
        pressRecipeAdd()
    elif btn == "Submit":
        pressRecipeAssign()
    elif btn == "Go":
        pressDateGo()
        
def pressDateGo():
    dateEntry = getDateEntry()
    isNewDate = (Utilities.getKnownInfo(dateEntry, WeekOfDate.dateIdColumn, WeekOfDate.dateNameColumn, WeekOfDate.dateTable, False) == None)
    actionType = getActionType()
    
    if actionType == "add":   
        app.addLabel("mainTitle", "Main", row = typeHeadingRow, column = 0)
        app.addLabel("side1Title", "Side 1", row = typeHeadingRow, column = 1)
        app.addLabel("side2Title", "Side 2", row = typeHeadingRow, column = 2)
        
    if isNewDate:
        wkOfDate = WeekOfDate(dateEntry)
        wkOfDate.add()
        
        for day in daysOfWeek:
            dayObj = DayAssignment.createNewDay(day, dateEntry)
            dayObj.add()

        app.clearEntry(newDateEntryLabel)
        updateDateList(dateEntry)
    
    configureRecipeDropDowns(actionType=actionType)

def updateDateList(newEntry):
    handleOptionBox(dateEntryLabel, "update", WeekOfDate.dateNameColumn, WeekOfDate.dateTable, row = dateRow, column = dateSelectionColumn)
    app.setOptionBox(dateEntryLabel, newEntry)

def getActionType():
    try:
        app.getOptionBox("Monday")
        actionType = "update"
    except:
        actionType = "add"
        
    return actionType

def configureRecipeDropDowns(mainTableParameter = Recipe.whereMainTypeId, sideATableParameter = Recipe.whereSideTypeId, sideBTableParameter = Recipe.whereSideTypeId, actionType = "update"):    
    row = typeHeadingRow + 1
    column = defaultColumn
    
    for day in daysOfWeek:            
        handleOptionBox(day, actionType, Recipe.recipeNameColumn, mainTableParameter, row, column)
        handleOptionBox(Recipe.sideALabelPrefix + day, actionType, Recipe.recipeNameColumn, sideATableParameter, row, column + 1)
        handleOptionBox(Recipe.sideBLabelPrefix + day, actionType, Recipe.recipeNameColumn, sideBTableParameter, row, column + 2)
        
        row += 1

    if actionType == "add":
        app.addButton("Submit", press, row = submitRow, column = 0, colspan = 2)
        app.stopTab()
        app.stopTabbedFrame()
        
def pressRecipeAdd():
    recipeName = app.getEntry(newRecipeLabel)
    recipeType = app.getOptionBox(recipeTypeLabel)
    isNewRecipe = (getKnownInfo(recipeName, Recipe.recipeIdColumn, Recipe.recipeNameColumn, Recipe.recipeTable, False) == None)
    
    if recipeName != "" and isNewRecipe:        
        addRecipe(recipeName, recipeType)
        configureRecipeDropDowns(actionType=getActionType())
        app.infoBox(recipeName, "Successfully added new recipe!")
            
    elif not isNewRecipe:
        errorMessage = "Recipe '{}' already exists. Please enter a unique recipe name.".format(recipeName)
        print(errorMessage)
        app.errorBox("Error: Duplicate Recipe", errorMessage)
    
    app.clearEntry(newRecipeLabel, callFunction=False)

def pressRecipeAssign():
    try:
        for day in daysOfWeek:
            mainDishInput = app.getOptionBox(day)
            sideAInput = app.getOptionBox(Recipe.sideALabelPrefix + day)
            sideBInput = app.getOptionBox(Recipe.sideBLabelPrefix + day)
        
            updateAssignment(day, mainDishInput, sideAInput, sideBInput)
        
        app.infoBox("Success", "Successfully updated recipe assignments!")

    except:
        app.errorBox("ERROR", "Error occurred during recipe assignment. See console log for details.")

    for i in range(2):
        print("=====================================")    
    
def updateAssignment(day, mainDishInput, sideAInput, sideBInput):
    dayObject = DayAssignment.getExistingDay(getDateEntry(), day)
    
    inputsMealIdExists, assignmentHasChanged, inputsMealId = dayObject.checkAssignmentStatus(mainDishInput, sideAInput, sideBInput)
    dayObject.updateRecipeAssignment(mainDishInput, sideAInput, sideBInput, inputsMealIdExists, assignmentHasChanged, inputsMealId)
    checkEntriesForCalendar(dayObject.dayName, dayObject.weekOfDate, mainDishInput, sideAInput, sideBInput, assignmentHasChanged)

def checkEntriesForCalendar(day, weekOfDate, mainDishInput, sideAInput, sideBInput, assignmentHasChanged):
    summary = "{}, {}, {}".format(mainDishInput, sideAInput, sideBInput)     
    nonePhrases = ["None, ", ", None", "None"]
    
    for phrase in nonePhrases:
        if summary.__contains__(phrase):
            summary = summary.replace(phrase, "")
            
    if assignmentHasChanged:
        if app.getCheckBox("Update"):
            addToCalendar(day, weekOfDate, summary)
        else:
            print("Calendar will not be changed because update checkbox is not ticked in settings")
    
def addToCalendar(day, dateEntry, summary):
    dateDict = {}        
    dateDict[day] = datetime.strftime(datetime.strptime(dateEntry, dateFormat) + timedelta(days=daysOfWeek.index(day)), dateFormat) 
    Calendar.main(summary, dateDict[day], app.getEntry(startLabelDinner), app.getEntry(endLabelDinner))

configureGui(app, handleOptionBox, press)
app.go()

# TODO:
# * Checkbox for no meals - would set all meal choices to None automatically
# * Store settings in db
# * Pop ups:
    # - alert that if trying to add new date, need to have drop down set to new
    # - alert when duplicate date is entered
# * double check all logic for which week of dates are shown in list as well as which is selected as default when adding a recipe
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

    if nameColumn == "Recipe_Name":
        optionsList = DayAssignment.updateRecipeList(getDateEntry(), labelName, optionsList, isSide)        
    
    if isUpdate:
        app.changeOptionBox(labelName, optionsList)
    elif isAdd:        
        if isSide:
            app.addOptionBox(labelName, optionsList, row, column)
        else:
            app.addLabelOptionBox(labelName, optionsList, row, column)

def getDateEntry():
    #TODO: Make sure user enters a valid date before proceeding
    return app.getEntry(dateEntryLabel)

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
    dateExists = (Utilities.getKnownInfo(dateEntry, WeekOfDate.dateIdColumn, WeekOfDate.dateNameColumn, WeekOfDate.dateTable, False) != None)
    actionType = "update"
    
    try:
        app.getOptionBox("Monday")
    except:
        actionType = "add"    
        app.addLabel("mainTitle", "Main", row = typeHeadingRow, column = 0)
        app.addLabel("side1Title", "Side 1", row = typeHeadingRow, column = 1)
        app.addLabel("side2Title", "Side 2", row = typeHeadingRow, column = 2)
        
    if not dateExists:
        wkOfDate = WeekOfDate(dateEntry)
        wkOfDate.add()
        
        for day in daysOfWeek:
            dayObj = DayAssignment.createNewDay(day, dateEntry)
            dayObj.add()
    
    #configureRecipeDropDowns(mainTableParameter=DayAssignment.generateJoin(dateEntry, Recipe.mainTypeId, DayAssignment.mainIdColumn), sideATableParameter=DayAssignment.generateJoin(dateEntry, Recipe.sideTypeId, DayAssignment.sideAIdColumn), sideBTableParameter=DayAssignment.generateJoin(dateEntry, Recipe.sideTypeId, DayAssignment.sideBIdColumn), actionType=actionType)
    configureRecipeDropDowns(actionType=actionType)

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
    print(isNewRecipe)
    
    if recipeName != "" and isNewRecipe:        
        addRecipe(recipeName, recipeType)
        configureRecipeDropDowns()
            
    elif not isNewRecipe:
        #TODO give error message pop up
        print("Recipe '{}' already exists. Please enter a unique recipe name.".format(recipeName))
    
    app.clearEntry(newRecipeLabel, callFunction=False)
    app.setOptionBox(recipeTypeLabel, 0, value=True, callFunction=False)    

def pressRecipeAssign():
    for day in daysOfWeek:
        mainDishInput = app.getOptionBox(day)
        sideAInput = app.getOptionBox(Recipe.sideALabelPrefix + day)
        sideBInput = app.getOptionBox(Recipe.sideBLabelPrefix + day)
    
        updateAssignment(day, mainDishInput, sideAInput, sideBInput)
        checkEntriesForCalendar(day, mainDishInput, sideAInput, sideBInput)

def updateAssignment(day, mainDishInput, sideAInput, sideBInput):
    dayObject = DayAssignment.getExistingDay(getDateEntry(), day)
    dayObject.updateRecipeAssignment(mainDishInput, sideAInput, sideBInput)
    
def checkEntriesForCalendar(day, mainDishInput, sideAInput, sideBInput):
    dateUserEntry = getDateEntry()
    summary = "{}, {}, {}".format(mainDishInput, sideAInput, sideBInput)     
    nonePhrases = ["None, ", ", None", "None"]
    
    for phrase in nonePhrases:
        if summary.__contains__(phrase):
            summary = summary.replace(phrase, "")
            
    if dateUserEntry != "" and summary != "":           
        dateEntry = datetime.strptime(dateUserEntry, dateFormat)
        addToCalendar(day, dateEntry, summary)
    elif dateUserEntry == "":
        print("WARNING: Date field was left blank -- will not create calendar event")
        # TODO: Add pop-up
    elif summary == "":
        print("WARNING: No recipes selected for {} -- will not create calendar event".format(day))
        # TODO: Add pop-up        
    
def addToCalendar(day, dateEntry, summary):
    dateDict = {}        
    dateDict[day] = datetime.strftime(dateEntry + timedelta(days=daysOfWeek.index(day)), dateFormat) 
    Calendar.main(summary, dateDict[day])

configureGui(app, handleOptionBox, press)
app.go()

from appJar import gui
from RecipeModel import *
from RecipeView import *
from DayAssignment import DayAssignment
from Utilities import *
import Calendar
from datetime import datetime
from datetime import timedelta
from WeekOfDate import WeekOfDate
from Settings import Settings
from Purchase_History import Purchase_History

app = gui("Meal Plan Configuration")
dateFormat = "%Y-%m-%d"
timeFormat = "%I:%M"
newOption = "- Select or Add New -"
ingredientsList = []

import ctypes
ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 6 )

def addRecipe(recipeName, recipeType, cookbookType, description):
    recipe = Recipe.createNewRecipe(recipeName, recipeType, cookbookType, ingredientsList, description)
    recipe.add()
    
    app.infoBox(recipeName, "Successfully added new recipe!\n\n{}".format(str(recipe)))

def handleOptionBox(labelName, actionType, nameColumn, tableName, row = defaultRow, column = defaultColumn):
    isAdd = (actionType == "add")
    isUpdate = (actionType == "update")
    isSide = (labelName.__contains__("side"))
    isUnit = (labelName.__contains__("Unit"))
    isUnlabeledSelection = (labelName.__contains__("Selection"))

    if nameColumn != WeekOfDate.dateNameColumn:
        optionsList = listOptions(nameColumn, tableName, True)
    if nameColumn == Recipe.recipeNameColumn and labelName.__contains__("day"):
        optionsList = DayAssignment.updateRecipeList(getDateEntry(), labelName, optionsList, isSide)        
    elif nameColumn == WeekOfDate.dateNameColumn:
        optionsList = WeekOfDate.findClosestWeekOfDate(listOptions=True)
        optionsList.insert(0, newOption)

    if isUpdate:
        app.changeOptionBox(labelName, optionsList)
    elif isAdd:        
        if isSide or isUnit or isUnlabeledSelection:
            app.addOptionBox(labelName, optionsList, row, column)
        else:
            app.addLabelOptionBox(labelName, optionsList, row, column)

def validateDateEntry(dateInput):
    try:
        datetime.strptime(dateInput, dateFormat)
        return True
    except ValueError:
        return False

def validateTimeEntries(startTime, endTime):
    try:
        startTime = datetime.strptime(startTime, timeFormat)
        endTime = datetime.strptime(endTime, timeFormat)
        
        if startTime > endTime:
            errorMessage = "Start time must be less than the end time."
            app.error(errorMessage)
            raise Exception(errorMessage)
        
    except:
        errorMessage = "Either start time or end time is not formatted correctly. Make sure it is like 3:00."
        app.error(errorMessage)
        raise Exception(errorMessage)

def getDateEntry(notifyIfManual = False):
    selection = app.getOptionBox(dateEntryLabel)
    entry = app.getEntry(newDateEntryLabel)
    isManual = False
    
    if entry:
        isManual = True
        dateEntry = entry
    elif selection == None:
        entry = datetime.strftime(WeekOfDate.findClosestWeekOfDate(listOptions=False), dateFormat)
        app.setOptionBox(dateEntryLabel, entry)
        dateEntry = entry
    else:
        dateEntry = selection
    
    dateIsValid = validateDateEntry(dateEntry)
    if dateIsValid:
        if notifyIfManual:
            return dateEntry, isManual
        else:
            return dateEntry
    else:
        errorMessage = "Date entered ({}) is incorrect. Ensure it is formatted like YYYY-MM-DD and is a legitimate calendar date.".format(dateEntry)
        app.errorBox("ERROR", errorMessage)
        app.clearEntry(newDateEntryLabel)
        raise Exception(errorMessage)

def press(btn):
    if btn == "Cancel":
        app.stop()
    elif btn.startswith("Add"):
        if btn.endswith("Recipe"):
            pressRecipeAdd()
        elif btn.endswith("Ingredient"):
            pressIngredientAdd()
    elif btn == "Submit":
        pressRecipeAssign()
    elif btn == "Go":
        pressDateGo()
    elif btn == "Update":
        pressSettingsUpdate()
    elif btn.startswith("None"):
        pressNoneMeal(btn)
    elif btn == "Enter":
        pressPurchaseEnter()
    elif btn == "Update Go":
        pressUpdateGo()
    elif btn == "Recipe Update":
        pressRecipeUpdate()
        
def pressUpdateGo():
    recipeName = app.getOptionBox(updateRecipeLabel)
    recipe = Recipe.getExistingRecipe(recipeId=False, recipeName=recipeName)
    
    app.clearAllEntries()
    app.setOptionBox(updateRecipeLabel, recipe.recipeName)
    app.setOptionBox(recipeCookbookTypeLabelUpdate, recipe.cookbookType)
    app.setOptionBox(recipeTypeLabelUpdate, recipe.recipeType)
    app.clearTextArea(recipeTextBoxLabelUpdate)
    app.setTextArea(recipeTextBoxLabelUpdate, recipe.description)
    
    count = 0
    updateRecipeColumnStart = 0
    
    if recipe.ingredients:
        for ingredient in recipe.ingredients:
            if count == 0:
                app.setEntry(ingredientEntryLabel, ingredient['name'])
                app.setEntry(amountEntryLabelUpdate, ingredient['amount'])
                app.setOptionBox(amountUnitsLabelUpdate, ingredient['units'])
            else:
                app.addEntry(ingredientEntryLabel + str(count), row = headingRow + 8 + count, column = updateRecipeColumnStart)
                app.addEntry(amountEntryLabelUpdate + str(count), row = headingRow + 8 + count, column = updateRecipeColumnStart + 2)
                handleOptionBox(amountUnitsLabelUpdate + str(count), "add", Amount_Units.unitNameColumn, Amount_Units.amountUnitsTable, row = headingRow + 8 + count, column = updateRecipeColumnStart + 3)
                app.setEntry(ingredientEntryLabel + str(count), ingredient['name'])
                app.setEntry(amountEntryLabelUpdate + str(count), ingredient['amount'])
                app.setOptionBox(amountUnitsLabelUpdate + str(count), ingredient['units'])
                
            count += 1
    else:
        count = 1

    app.addNamedButton("Update", "Recipe Update", press, row = headingRow + 15 + count, column = updateRecipeColumnStart + 1)
    app.addButton("Delete", press, row = headingRow + 15 + count, column = updateRecipeColumnStart + 2)    
    app.stopTab()
    
def pressPurchaseEnter():
    ingredientName = app.getOptionBox(ingredientSelectionPriceLabel)
    amount = app.getEntry(amountPurchasedLabel)
    units = app.getOptionBox(amountPurchasedUnitsLabel)
    purchasePrice = app.getEntry(amountPaidLabel)
    store = app.getOptionBox(storeSelectionLabel)
    
    newPurchase = Purchase_History.createNewPurchase(ingredientName, amount, units, purchasePrice, store)
    newPurchase.add()
    print(newPurchase)
    
    app.clearEntry(amountPurchasedLabel)
    app.clearEntry(amountPaidLabel)
    app.setFocus(amountPurchasedLabel)
        
def pressIngredientAdd():
    ingredientName = app.getEntry(newIngredientLabel)
    amount = app.getEntry(amountEntryLabel)
    units = app.getOptionBox(amountUnitsLabel)
    isNewIngredient = (getKnownInfo(ingredientName, Ingredient.Ingredient.ingredientIdColumn, Ingredient.Ingredient.ingredientNameColumn, Ingredient.Ingredient.ingredientTable, False) == None)

    if ingredientName != "":  
        ingredientsList.append({'amount': amount, 'name': ingredientName, 'units': units})
        
        if isNewIngredient:
            ingredient = Ingredient.Ingredient(ingredientName)
            ingredient.add()
            
            message = "Successfully added new ingredient!"
            app.info(message)
            
        elif not isNewIngredient:
            message = "Ingredient '{}' already exists.".format(ingredientName)
            app.warn(message)
        
    app.clearEntry(newIngredientLabel)
    app.clearEntry(amountEntryLabel)
    app.setFocus(newIngredientLabel)
    
def pressRecipeAdd():
    recipeName = app.getEntry(newRecipeLabel)
    isNewRecipe = (getKnownInfo(recipeName, Recipe.recipeIdColumn, Recipe.recipeNameColumn, Recipe.recipeTable, False) == None)
    actionType=getActionType()
    
    if recipeName != "" and isNewRecipe:
        recipeType = app.getOptionBox(recipeTypeLabel)
        cookbookType = app.getOptionBox(recipeCookbookTypeLabel)
        description = app.getTextArea(recipeTextBoxLabel)        
        if description == "": description = None
        
        addRecipe(recipeName, recipeType, cookbookType, description)
        
        if actionType == "update":
            configureRecipeDropDowns()
            
    elif not isNewRecipe:
        errorMessage = "Recipe '{}' already exists. Please enter a unique recipe name.".format(recipeName)
        app.warn(errorMessage)
        app.warningBox("Duplicate Recipe", errorMessage)
    
    app.clearEntry(newRecipeLabel, callFunction=False)
    app.clearTextArea(recipeTextBoxLabel, callFunction=False)
    
    global ingredientsList
    ingredientsList = []
    
def pressNoneMeal(buttonTitle):
    day = getDayFromButton(buttonTitle)
    
    app.setOptionBox(day, noneButtonLabel)
    app.setOptionBox(Recipe.sideALabelPrefix + day, noneButtonLabel)
    app.setOptionBox(Recipe.sideBLabelPrefix + day, noneButtonLabel)
    
def getDayFromButton(buttonTitle):
    day = buttonTitle.split("_")[1]
    
    return day
        
def pressSettingsUpdate():
    try:
        dinnerStart = app.getEntry(startLabelDinner)
        dinnerEnd = app.getEntry(endLabelDinner)
        updateCalendar = app.getCheckBox(updateCheckBoxLabel)
        
        validateTimeEntries(dinnerStart, dinnerEnd)

        existingSettings = Settings.getExistingSettings()
        newDictionary = {dinnerKey: {startKey: dinnerStart, endKey: dinnerEnd}, updateKey: updateCalendar}
        existingSettings.updateExistingSettings(newDictionary)
        
        message = "Successfully updated the settings!"
        app.info(message)
        app.infoBox("Success", message)
    except:
        errorMessage = "Error occurred while updating the settings, see console output for details."
        app.error(errorMessage)
        app.errorBox("ERROR", errorMessage)
        
def pressDateGo():
    dateEntry, isManualDateEntry = getDateEntry(notifyIfManual=True)
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

    if isManualDateEntry:
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
        
        if actionType == "add":
            app.addNamedButton("None", noneButtonLabel + "_" + day, press, row = row, column = column + 3)
        
        row += 1

    if actionType == "add":
        app.addButton("Submit", press, row = submitRow, column = 0, colspan = 2)
        app.stopTab()
        app.stopTabbedFrame()

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

configureGui(app, handleOptionBox, press)
app.go()
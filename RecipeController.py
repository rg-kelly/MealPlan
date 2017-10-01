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
import Ingredient
import random

app = gui("Meal Plan Configuration")
app.setLogLevel("ERROR")
#app.setIcon(".\icon.gif")

dateFormat = "%Y-%m-%d"
timeFormat = "%I:%M"
newOption = "- Select or Add New -"
ingredientsList = []
submitButtonSuffix = "__submitButton"
updateButtonSuffix = "__updateButton"
deleteButtonSuffix = "__deleteButton"
cancelButtonSuffix = "__cancelButton"
ingredientRowSymbol = "@"
addToCurrentRow = 0
windowTitleUniqueHiddenLabel = "ID"

import ctypes
ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 6 )

def addRecipe(recipeName, recipeType, cookbookType, description):
    recipe = Recipe.createNewRecipe(recipeName, recipeType, cookbookType, ingredientsList, description)
    recipe.add()
    
    app.infoBox(recipeName, "Successfully added new recipe!\n\n{}".format(str(recipe)))
    
def updateRecipe(recipeName, recipeType, cookbookType, description):
    recipe = Recipe.getExistingRecipe(recipeName=recipeName, recipeId=False)
    updateStatus = recipe.update(recipeName, recipeType, cookbookType, ingredientsList, description, updateIngredients=ingredientsHaveChanged)

    if updateStatus == True: app.infoBox(recipeName, "Successfully updated recipe!\n\n{}".format(str(recipe)))
    elif updateStatus != False: app.errorBox(recipeName, "Error occurred while updating recipe. {}".format(updateStatus))

def handleOptionBox(labelName, actionType, nameColumn, tableName, row = defaultRow, column = defaultColumn):
    isAdd = (actionType == "add")
    isUpdate = (actionType == "update")
    isSide = (labelName.__contains__("side"))
    isUnit = (labelName.__contains__("Unit"))
    isUnlabeledSelection = (labelName.__contains__("Selection"))
    isUniqueLabel = (labelName.__contains__("0."))

    if nameColumn != WeekOfDate.dateNameColumn or labelName == weekOfDatePurchaseSelectionLabel:
        optionsList = listOptions(nameColumn, tableName, True)
    if nameColumn == Recipe.recipeNameColumn and labelName.__contains__("day"):
        optionsList = DayAssignment.updateRecipeList(getDateEntry(), labelName, optionsList, isSide)        
    elif nameColumn == WeekOfDate.dateNameColumn and labelName != weekOfDatePurchaseSelectionLabel:
        optionsList = WeekOfDate.findClosestWeekOfDate(listOptions=True)
        optionsList.insert(0, newOption)

    if isUpdate:
        app.changeOptionBox(labelName, optionsList)
    elif isAdd:        
        if isSide or isUnit or isUnlabeledSelection or isUniqueLabel:
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
    dateEntry, isManual = getEntryLogic(dateEntryLabel, newDateEntryLabel, datetime.strftime(WeekOfDate.findClosestWeekOfDate(listOptions=False), dateFormat), validateDateEntry, "Ensure it is formatted like YYYY-MM-DD and is a legitimate calendar date.", True)
    
    if notifyIfManual:
        return dateEntry, isManual
    else:
        return dateEntry

def getEntryLogic(selectionLabel, entryLabel, defaultEntry, validationFunction, errorMessage = "", notifyIfManual = False):
    selection = app.getOptionBox(selectionLabel)
    entry = app.getEntry(entryLabel)
    isManual = False
    
    if entry:
        isManual = True
        actualEntry = entry
    elif selection == None:
        actualEntry = defaultEntry
        app.setOptionBox(selectionLabel, actualEntry)
    else:
        actualEntry = selection
        
    isValidEntry = validationFunction(actualEntry)
    if isValidEntry:
        if notifyIfManual:
            return actualEntry, isManual
        else:
            return actualEntry
    else:
        message = "Entry '{}' is not valid. {}".format(actualEntry, errorMessage)
        app.errorBox("ERROR", message)
        app.clearEntry(entryLabel)
        raise Exception(message)

def press(btn):
    #print(btn)
    if btn == "Cancel":
        app.stop()
    elif btn.startswith(ingredientAddButton):
        pressIngredientAdd(btn)
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
    elif btn == recipeGoAgainButton:
        pressRecipeGo()
    elif btn.__contains__(" Recipe: "):
        if btn.endswith(updateButtonSuffix) or btn.endswith(submitButtonSuffix):
            pressRecipeSubmit()
        elif btn.endswith(cancelButtonSuffix):
            pressRecipeCancel()
        elif btn.endswith(deleteButtonSuffix):
            pressRecipeDelete(btn)
        if not btn.endswith(deleteButtonSuffix): destroyRecipeWindow(btn)
    elif btn == configureIngredientsButton:
        pressConfigureIngredients()
    elif btn.startswith(ingredientsDoneButton):
        pressIngredientsDone()
        destroySubwindow(btn, ingredientsDoneButton)
        
def pressRecipeCancel():
    pass
    
def pressRecipeDelete(btn):
    recipeName = pressRecipeGo(returnName=True)
    isOkayToDelete = app.yesNoBox(title="Verify Delete", message="Are you sure you want to delete recipe '{}'?".format(recipeName), parent=app.getLabel(windowTitleUniqueHiddenLabel))
    
    if isOkayToDelete:
        recipeToDelete = Recipe.getExistingRecipe(recipeName=recipeName, recipeId=False)
        deleteStatus = recipeToDelete.delete()
        
        if deleteStatus == True:
            app.infoBox(recipeName, "Successfully deleted recipe '{}'.".format(recipeName))
            destroyRecipeWindow(btn)
            handleOptionBox(recipeSelectionLabel, "update", Recipe.recipeNameColumn, Recipe.recipeTable, row = dateRow, column = recipeSelectionColumn)
        else:
            app.errorBox(recipeName, "Error occurred while deleting recipe. {}".format(deleteStatus))

def destroyRecipeWindow(btn):
    if btn.endswith(submitButtonSuffix):
        suffix = submitButtonSuffix
    elif btn.endswith(updateButtonSuffix):
        suffix = updateButtonSuffix
    elif btn.endswith(deleteButtonSuffix):
        suffix = deleteButtonSuffix
    elif btn.endswith(cancelButtonSuffix):
        suffix = cancelButtonSuffix
    
    destroySubwindow(btn, suffix)

def pressIngredientsDone():
    global addToCurrentRow
    addToCurrentRow = 0
    done = False
    count = 1

    while not done:
        amountLabel = getNumberedAmountLabel(count)
        unitsLabel = amountUnitsLabel + uniqueLabel + str(count)
        ingredientNameLabel = ingredientEntryLabel + uniqueLabel + str(count)
        
        try:
            amount = app.getEntry(amountLabel)
            units = app.getOptionBox(unitsLabel)
            ingredientName = app.getEntry(ingredientNameLabel)
           
        except:
            done = True

        if not done:
            isNewIngredient = (getKnownInfo(ingredientName, Ingredient.Ingredient.ingredientIdColumn, Ingredient.Ingredient.ingredientNameColumn, Ingredient.Ingredient.ingredientTable, False) == None)

            if ingredientName != "":  
                ingredientsList.append({'amount': amount, 'name': ingredientName, 'units': units})
                
                if isNewIngredient:
                    ingredient = Ingredient.Ingredient(ingredientName)
                    ingredient.add()
                    handleOptionBox(ingredientSelectionPriceLabel, "update", Ingredient.Ingredient.ingredientNameColumn, Ingredient.Ingredient.ingredientTable, row = headingRow + 1, column = pricesColumnStart)
                    
                    message = "Successfully added new ingredient '{}'!".format(ingredientName)
                    
                elif not isNewIngredient:
                    message = "Ingredient '{}' already exists.".format(ingredientName)
                
                print(message)
        count += 1
    
    #print(ingredientsList)

def getNumberedAmountLabel(row):
    numberedAmountLabel = str(row) + ". "
    return numberedAmountLabel

def pressConfigureIngredients():
    recipeName = getEntryLogic(recipeSelectionLabel, newRecipeEntryLabel, defaultEntry=app.getOptionBox(recipeSelectionLabel), validationFunction=validateRecipeName, errorMessage="", notifyIfManual=False)
    isNewRecipe = (getKnownInfo(recipeName, Recipe.recipeIdColumn, Recipe.recipeNameColumn, Recipe.recipeTable, False) == None)
    uniqueIngredientsWindowTitle = ingredientsWindowTitle + uniqueLabel
    
    app.startSubWindow(uniqueIngredientsWindowTitle, ingredientsWindowTitle, modal=True)
    app.addLabel(uniqueIngredientsWindowTitle, ingredientsWindowTitle + " for '" + recipeName + "'", row = headingRow, column = 0, colspan = 4)
    
    ingredientStartRow = headingRow + 1
    if not isNewRecipe:
        recipe = Recipe.getExistingRecipe(recipeName=recipeName, recipeId=False) 
        global ingredientsHaveChanged
        ingredientsHaveChanged = True
        
        if recipe.ingredients:
            for ingredient in recipe.ingredients:
                amountLabel = getNumberedAmountLabel(ingredientStartRow)
                unitsLabel = amountUnitsLabel + uniqueLabel + str(ingredientStartRow)
                ingredientNameLabel = ingredientEntryLabel + uniqueLabel + str(ingredientStartRow)
                
                addIngredientEntries(amountLabel, unitsLabel, ingredientNameLabel, startRow=ingredientStartRow)
                app.setEntry(amountLabel, ingredient['amount'])
                app.setOptionBox(unitsLabel, ingredient['units'])
                app.setEntry(ingredientNameLabel, ingredient['name'])

                ingredientStartRow += 1
            app.addNamedButton("Add", ingredientAddButton + uniqueLabel + ingredientRowSymbol + str(ingredientStartRow), press, row=ingredientStartRow - len(recipe.ingredients), column=3)
        else:
            addIngredientEntries(amountLabel=getNumberedAmountLabel(ingredientStartRow), unitsLabel=amountUnitsLabel + uniqueLabel + str(ingredientStartRow), ingredientNameLabel=ingredientEntryLabel + uniqueLabel + str(ingredientStartRow), startRow=ingredientStartRow)
            app.addNamedButton("Add", ingredientAddButton + uniqueLabel + ingredientRowSymbol + str(ingredientStartRow), press, row=ingredientStartRow, column=3)                
    elif isNewRecipe:
        addIngredientEntries(amountLabel=getNumberedAmountLabel(ingredientStartRow), unitsLabel=amountUnitsLabel + uniqueLabel + str(ingredientStartRow), ingredientNameLabel=ingredientEntryLabel + uniqueLabel + str(ingredientStartRow), startRow=ingredientStartRow)
        app.addNamedButton("Add", ingredientAddButton + uniqueLabel + ingredientRowSymbol + str(ingredientStartRow), press, row=ingredientStartRow, column=3)                
    
    app.addNamedButton(ingredientsDoneButton, ingredientsDoneButton + uniqueIngredientsWindowTitle, press, row = ingredientStartRow + 1, column=0, colspan=4)
    app.showSubWindow(uniqueIngredientsWindowTitle)

def destroySubwindow(buttonId, suffixToReplace):
    windowTitle = buttonId.replace(suffixToReplace, "")
    app.destroySubWindow(windowTitle)

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
        
def pressIngredientAdd(btn):
    ingredientWindowStartRow = 1

    if btn.__contains__(ingredientRowSymbol):
        currentRow = int(btn.split(ingredientRowSymbol)[1])
        if currentRow == ingredientWindowStartRow: currentRow += 1
        currentRow += addToCurrentRow
        
    app.removeButton(ingredientsDoneButtonUnique)
    addIngredientEntries(amountLabel=getNumberedAmountLabel(currentRow), unitsLabel=amountUnitsLabel + uniqueLabel + str(currentRow), ingredientNameLabel=ingredientEntryLabel + uniqueLabel + str(currentRow), startRow=currentRow)
    app.addNamedButton(ingredientsDoneButton, ingredientsDoneButtonUnique, press, row = currentRow + 1, column=0, colspan=4)
    
    global addToCurrentRow
    addToCurrentRow += 1
    
def pressRecipeSubmit():
    recipeName = pressRecipeGo(returnName=True)
    isNewRecipe = (getKnownInfo(recipeName, Recipe.recipeIdColumn, Recipe.recipeNameColumn, Recipe.recipeTable, False) == None)

    recipeType = app.getOptionBox(recipeTypeLabel + uniqueLabel)
    cookbookType = app.getOptionBox(recipeCookbookTypeLabel + uniqueLabel)
    description = app.getTextArea(recipeTextBoxLabel + uniqueLabel)        
    if description == "": description = None    

    if isNewRecipe:
        addRecipe(recipeName, recipeType, cookbookType, description)
        updateRecipeList(recipeName)
        app.clearEntry(newRecipeEntryLabel)        
    else:
        updateRecipe(recipeName, recipeType, cookbookType, description)
    
    global ingredientsList
    ingredientsList = []
    
    global ingredientsHaveChanged
    ingredientsHaveChanged = False
  
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

def validateRecipeName(recipeName):
    return True   

def addIngredientEntries(amountLabel, unitsLabel, ingredientNameLabel, startRow):
    app.addLabelEntry(amountLabel, row=startRow, column=0)
    handleOptionBox(unitsLabel, "add", Amount_Units.unitNameColumn, Amount_Units.amountUnitsTable, startRow, 1)
    app.addEntry(ingredientNameLabel, row = startRow, column = 2)    

def pressRecipeGo(returnName = False):
    recipeName, isManualEntry = getEntryLogic(recipeSelectionLabel, newRecipeEntryLabel, defaultEntry=app.getOptionBox(recipeSelectionLabel), validationFunction=validateRecipeName, errorMessage="", notifyIfManual=True)
    isNewRecipe = (getKnownInfo(recipeName, Recipe.recipeIdColumn, Recipe.recipeNameColumn, Recipe.recipeTable, False) == None)
    actionType = getActionType(tabType=addRecipesTab)
    
    if returnName: return recipeName
    
    global uniqueLabel
    uniqueLabel = str(random.random())
    
    global ingredientsDoneButtonUnique
    ingredientsDoneButtonUnique = ingredientsDoneButton + ingredientsWindowTitle + uniqueLabel
    
    global ingredientsHaveChanged
    ingredientsHaveChanged = False    

    if isNewRecipe:
        windowTitlePrefix = "Add"
    else:
        windowTitlePrefix = "Update"
    
    windowTitle = "{} Recipe: {}".format(windowTitlePrefix, recipeName)
    windowTitleUnique = windowTitle + uniqueLabel

    app.startSubWindow(name=windowTitleUnique, title=windowTitle, modal=True)
    app.addLabel(windowTitleUniqueHiddenLabel, windowTitleUnique)
    app.hideLabel(windowTitleUniqueHiddenLabel)
    app.addLabel(windowTitleUnique, windowTitle, row=headingRow, column=0, colspan=4)
    app.setLabelFg(windowTitleUnique, "white")
    app.setLabelBg(windowTitleUnique, "gray")
    
    app.addLabel(recipeTypeLabel + "_" + uniqueLabel, recipeTypeLabel, row = headingRow + 1, column=0)
    handleOptionBox(recipeTypeLabel + uniqueLabel, "add", Recipe.typeNameColumn, Recipe.typeTable + " WHERE {0} = {1}".format(Recipe.isCookbookColumn, Recipe.isNotCookbook), headingRow+1, 1)
    app.addLabel(recipeCookbookTypeLabel + "_" + uniqueLabel, recipeCookbookTypeLabel, row = headingRow + 1, column=2)
    handleOptionBox(recipeCookbookTypeLabel + uniqueLabel, "add", Recipe.typeNameColumn, Recipe.typeTable + " WHERE {0} = {1}".format(Recipe.isCookbookColumn, Recipe.isCookbook), headingRow+1, 3)
    
    if not isNewRecipe:
        ingredientStartRow = headingRow + 4
        recipe = Recipe.getExistingRecipe(recipeName=recipeName, recipeId=False) 
        
        app.addHorizontalSeparator(row = headingRow+2, column = 0, colspan = 4)
        app.addButton(configureIngredientsButton, press, row = headingRow + 3, column = 0, colspan=4)
        app.addHorizontalSeparator(row = ingredientStartRow + 1, column = 0, colspan = 4)        
        
        app.addLabel("Instructions:" + uniqueLabel, "Instructions:", row = ingredientStartRow + 2, column = 0)
        app.addScrolledTextArea(recipeTextBoxLabel + uniqueLabel, row = ingredientStartRow + 2, column = 0, colspan = 4)
        app.addNamedButton("Update", windowTitleUnique + updateButtonSuffix, press, row = ingredientStartRow + 3, column=1, colspan=1)
        app.addNamedButton("Delete", windowTitleUnique + deleteButtonSuffix, press, row = ingredientStartRow + 3, column = 2, colspan=1)
        
        app.setOptionBox(recipeTypeLabel + uniqueLabel, recipe.recipeType)
        app.setOptionBox(recipeCookbookTypeLabel + uniqueLabel, recipe.cookbookType)
        app.setTextArea(recipeTextBoxLabel + uniqueLabel, recipe.description)
        
    else:
        app.setOptionBox(recipeCookbookTypeLabel + uniqueLabel, "None")
        
        app.addHorizontalSeparator(row = headingRow+2, column = 0, colspan = 4)
        app.addButton(configureIngredientsButton, press, row = headingRow + 3, column = 0, colspan=4)
        app.addHorizontalSeparator(row = headingRow+5, column = 0, colspan = 4)        
    
        app.addLabel("Instructions:" + uniqueLabel, "Instructions:", row = headingRow+6, column = 0)
        app.addScrolledTextArea(recipeTextBoxLabel + uniqueLabel, row = headingRow+6, column = 0, colspan = 4)
        app.addNamedButton("Submit", windowTitleUnique + submitButtonSuffix, press, row=headingRow + 7, column=1, colspan=1)
        app.addNamedButton("Cancel", windowTitleUnique + cancelButtonSuffix, press, row = headingRow + 7, column = 2, colspan=1)
        
    app.stopSubWindow()
    app.showSubWindow(windowTitleUnique)

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

def updateDropDownList(newItem, optionBoxLabel, nameColumn, table, row, column):
    handleOptionBox(optionBoxLabel, "update", nameColumn, table, row = row, column = column)
    app.setOptionBox(optionBoxLabel, newItem)    

def updateDateList(newEntry):
    updateDropDownList(newEntry, dateEntryLabel, WeekOfDate.dateNameColumn, WeekOfDate.dateTable, row = dateRow, column = dateSelectionColumn)

def updateRecipeList(newRecipeName):
    updateDropDownList(newRecipeName, recipeSelectionLabel, Recipe.recipeNameColumn, Recipe.recipeTable, row=dateRow, column=recipeSelectionColumn)

def getActionType(tabType = assignRecipesTab):
    if tabType == assignRecipesTab:
        try:
            app.getOptionBox("Monday")
            actionType = "update"
        except:
            actionType = "add"
    elif tabType == addRecipesTab:
        try:
            app.getTextArea(recipeTextBoxLabel)
            actionType = "update"
        except:
            actionType = "add"
    elif tabType == "both":
        try:
            app.getOptionBox("Monday")
            app.getTextArea(recipeTextBoxLabel)
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
        
        #stopTabbedFrame = (getActionType("both") == "update")
        #if stopTabbedFrame: app.stopTabbedFrame()
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

configureGui(app, handleOptionBox, press)
app.go()
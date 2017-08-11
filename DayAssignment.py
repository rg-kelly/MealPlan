from DataConnection import DataConnection
from RecipeModel import Recipe
from datetime import datetime
from WeekOfDate import WeekOfDate
import Utilities

class DayAssignment:
    dayTable = "Day"
    dayIdColumn = "Day_ID"
    dayNameColumn = "Day_Name"
    
    dayAssignmentTable = "Day_Assignment"
    mealAssignmentTable = "Meal"
    
    mealIdColumn = "Meal_ID"    
    mainIdColumn = "Main_Dish_ID"
    sideAIdColumn = "Side_A_ID"
    sideBIdColumn = "Side_B_ID"
    noneMealId = 1
    noneRecipeName = "None"

    def __init__(self, dayName, weekOfDate, mainDish, sideA, sideB):
        self.dayName = dayName
        self.weekOfDate = weekOfDate
        self.mainDish = mainDish
        self.sideA = sideA
        self.sideB = sideB
        self.dateId, self.dayId = DayAssignment.getDayAssignmentKeyIds(self.weekOfDate, self.dayName)
    
    @classmethod
    def getExistingDay(cls, weekOfDate, dayOfWeek):
        dateId, dayId = DayAssignment.getDayAssignmentKeyIds(weekOfDate, dayOfWeek)
        
        connection = DataConnection()
        query = "SELECT {} FROM {} WHERE {} = {} AND {} = {};".format(DayAssignment.mealIdColumn, DayAssignment.dayAssignmentTable, WeekOfDate.dateIdColumn, dateId, DayAssignment.dayIdColumn, dayId)
        result = connection.runQuery(query)
        idInfo = result.fetchone()
        connection.closeConnection()
    
        if idInfo != None:
            mealId = idInfo[0]
        else:
            mealId = None
            
        mainDish, sideA, sideB = DayAssignment.getAllRecipeNamesFromMealId(mealId)
        
        return DayAssignment(dayOfWeek, weekOfDate, mainDish, sideA, sideB)    
    
    @classmethod
    def createNewDay(cls, dayName, weekOfDate):        
        return DayAssignment(dayName, weekOfDate, DayAssignment.noneRecipeName, DayAssignment.noneRecipeName, DayAssignment.noneRecipeName) ## Default to 'None' recipes for meal
    
    def getDayAssignmentKeyIds(weekOfDate, dayName):
        dateId = Utilities.getKnownInfo(weekOfDate, WeekOfDate.dateIdColumn, WeekOfDate.dateNameColumn, WeekOfDate.dateTable, False)
        dayId = Utilities.getKnownInfo(dayName, DayAssignment.dayIdColumn, DayAssignment.dayNameColumn, DayAssignment.dayTable, False)
        
        return dateId, dayId
    
    def getRecipeNameFromMealId(mealId, idColumnName):
        recipeName = Recipe.getExistingRecipe(recipeId=Utilities.getKnownInfo(mealId, idColumnName, DayAssignment.mealIdColumn, DayAssignment.mealAssignmentTable, True), recipeName=False).recipeName
        
        return recipeName        
    
    def getAllRecipeNamesFromMealId(mealId):
        mainDish, sideA, sideB = DayAssignment.getRecipeNameFromMealId(mealId, DayAssignment.mainIdColumn), DayAssignment.getRecipeNameFromMealId(mealId, DayAssignment.sideAIdColumn), DayAssignment.getRecipeNameFromMealId(mealId, DayAssignment.sideBIdColumn)
        
        return mainDish, sideA, sideB
    
    def getMealIdFromRecipeNames(mainDish, sideA, sideB):
        connection = DataConnection()
        mainId, sideAId, sideBId = Recipe.getExistingRecipe(False, mainDish).recipeId, Recipe.getExistingRecipe(False, sideA).recipeId, Recipe.getExistingRecipe(False, sideB).recipeId
        
        query = "SELECT {} FROM {} WHERE {} = {} AND {} = {} AND {} = {};".format(DayAssignment.mealIdColumn, DayAssignment.mealAssignmentTable, DayAssignment.mainIdColumn, mainId, DayAssignment.sideAIdColumn, sideAId, DayAssignment.sideBIdColumn, sideBId)
    
        result = connection.runQuery(query)
        idInfo = result.fetchone()
        connection.closeConnection()
    
        if idInfo != None: return idInfo[0]
        else: return None
        
    def updateRecipeAssignment(self, mainDishInput, sideAInput, sideBInput):
        currentMealId = DayAssignment.getMealIdFromRecipeNames(self.mainDish, self.sideA, self.sideB)
        inputsMealId = DayAssignment.getMealIdFromRecipeNames(mainDishInput, sideAInput, sideBInput)
        inputsMealIdExists = (inputsMealId != None)
        
        if currentMealId != inputsMealId:
            connection = DataConnection()
            
            if not inputsMealIdExists:
                inputsMealId = Utilities.generateNewKey(DayAssignment.mealIdColumn, DayAssignment.mealAssignmentTable)
                insertQuery = "INSERT INTO {} VALUES (%s, %s, %s, %s)".format(DayAssignment.mealAssignmentTable)
                insertBindingVariables = (inputsMealId, Recipe.getExistingRecipe(recipeId=False, recipeName=mainDishInput).recipeId, Recipe.getExistingRecipe(recipeId=False, recipeName=sideAInput).recipeId, Recipe.getExistingRecipe(recipeId=False, recipeName=sideBInput).recipeId)
                connection.updateData(insertQuery, insertBindingVariables)
            
            self.mainDish, self.sideA, self.sideB = mainDishInput, sideAInput, sideBInput
            updateQuery = "UPDATE {} SET {} = %s WHERE {} = {}".format(DayAssignment.dayAssignmentTable, DayAssignment.mealIdColumn, DayAssignment.dayIdColumn, str(self.dayId))
            updateBindingVariable = (inputsMealId,)
            connection.updateData(updateQuery, updateBindingVariable)
            
            connection.closeConnection()
        
            print("Successfully updated the meal for {}".format(self.dayName))
            print(self)
            
        else:
            print("Meal assignment didn't change for {} -- nothing to do here".format(self.dayName))
    
    def updateRecipeList(weekOfDate, dayOfWeek, recipeList, isSide = False):
        isSideA = (dayOfWeek.__contains__(Recipe.sideALabelPrefix))
        isSideB = (dayOfWeek.__contains__(Recipe.sideBLabelPrefix))
        
        if isSide:
            mealAssignment = DayAssignment.getExistingDay(weekOfDate, Utilities.extractDayName(dayOfWeek))
            
            if isSideA:
                recipeName = mealAssignment.sideA
            elif isSideB:
                recipeName = mealAssignment.sideB
        else:
            mealAssignment = DayAssignment.getExistingDay(weekOfDate, dayOfWeek)
            recipeName = mealAssignment.mainDish
        
        if recipeList.__contains__(recipeName):
            recipeList.insert(0, recipeList.pop(recipeList.index(recipeName)))
        else:
            print("WARNING: Recipe list '{}' did not contain recipe called '{}'".format(recipeList, recipeName))
    
        return recipeList    
    
    def add(self):
        connection = DataConnection()
        query = "INSERT INTO {0} ({1},{2},{3}) VALUES(%s, %s, %s);".format(DayAssignment.dayAssignmentTable, DayAssignment.dayIdColumn, WeekOfDate.dateIdColumn, DayAssignment.mealIdColumn)

        insertValue = (self.dayId, self.dateId, DayAssignment.noneMealId)
        connection.updateData(query, insertValue)
        connection.closeConnection()

        print("Successfully added day for {}:{}".format(self.weekOfDate, self.dayName))
        print(self)

    def generateJoin(weekOfDate, typeId, recipeTypeIdColumn):
        joinString = """{0} join {1} on {0}.{2} = {1}.{3}
                            join {4} on {1}.{5} = {4}.{5}
                            join {6} on {6}.{7} = {4}.{7}
                        where {6}.{8} = '{9}' and {0}.{10} = {11};""".format(Recipe.recipeTable, DayAssignment.mealAssignmentTable, Recipe.recipeIdColumn, recipeTypeIdColumn, DayAssignment.dayTable, DayAssignment.mealIdColumn, WeekOfDate.dateTable, WeekOfDate.dateIdColumn, WeekOfDate.dateNameColumn, weekOfDate, Recipe.typeIdColumn, typeId)
        
        return joinString

    def __str__(self):        
        message = "--- Summary ---\n"
        message += "Day name: " + self.dayName + "\n"
        message += "Week of date: " + self.weekOfDate + "\n"
        message += "Main dish: " + self.mainDish + "\n"
        message += "Side dish A: " + self.sideA + "\n"
        message += "Side dish B: " + self.sideB

        return message
from DataConnection import DataConnection
from RecipeModel import Recipe
from datetime import datetime
from WeekOfDate import WeekOfDate
import Utilities

class Day:
    dayTable = "Day"
    mealAssignmentTable = "Meal"
    
    dayIdColumn = "Day_ID"
    dayNameColumn = "Day_Name"
    weekOfDateColumn = "Week_Of_Date_ID"
    
    mealIdColumn = "Meal_ID"    
    mainIdColumn = "Main_Dish_ID"
    sideAIdColumn = "Side_A_ID"
    sideBIdColumn = "Side_B_ID"
    noneMealId = 1
    noneRecipeName = "None"

    def __init__(self, dayId, dayName, weekOfDate, mainDish, sideA, sideB):
        self.dayName = dayName
        self.weekOfDate = weekOfDate
        self.dayId = dayId
        self.mainDish = mainDish
        self.sideA = sideA
        self.sideB = sideB        

    @classmethod
    def getExistingDay(cls, dayName):
        dayId = Utilities.getKnownInfo(dayName, Day.dayIdColumn, Day.dayNameColumn, Day.dayTable)
        mealId = Utilities.getKnownInfo(dayId, Day.mealIdColumn, Day.dayIdColumn, Day.dayTable, True)
        weekOfDate = Utilities.getKnownInfo(Utilities.getKnownInfo(dayId, Day.weekOfDateColumn, Day.dayIdColumn, Day.dayTable, True), WeekOfDate.dateNameColumn, WeekOfDate.dateIdColumn, WeekOfDate.dateTable, True)
        mainDish, sideA, sideB = Day.getAllRecipeNamesFromMealId(mealId)
        
        return Day(dayId, dayName, weekOfDate, mainDish, sideA, sideB)
    
    @classmethod
    def createNewDay(cls, dayName, weekOfDate):
        dayId = Utilities.generateNewKey(Day.dayIdColumn, Day.dayTable)
        
        return Day(dayId, dayName, weekOfDate, Day.noneRecipeName, Day.noneRecipeName, Day.noneRecipeName) ## Default to 'None' recipes for meal
    
    def getRecipeNameFromMealId(mealId, idColumnName):
        recipeName = Recipe.getExistingRecipe(recipeId=Utilities.getKnownInfo(mealId, idColumnName, Day.mealIdColumn, Day.mealAssignmentTable, True), recipeName=False).recipeName
        
        return recipeName        
    
    def getAllRecipeNamesFromMealId(mealId):
        mainDish, sideA, sideB = Day.getRecipeNameFromMealId(mealId, Day.mainIdColumn), Day.getRecipeNameFromMealId(mealId, Day.sideAIdColumn), Day.getRecipeNameFromMealId(mealId, Day.sideBIdColumn)
        
        return mainDish, sideA, sideB
    
    def getMealIdFromRecipeNames(mainDish, sideA, sideB):
        connection = DataConnection()
        mainId, sideAId, sideBId = Recipe.getExistingRecipe(False, mainDish).recipeId, Recipe.getExistingRecipe(False, sideA).recipeId, Recipe.getExistingRecipe(False, sideB).recipeId
        
        query = "SELECT {} FROM {} WHERE {} = {} AND {} = {} AND {} = {};".format(Day.mealIdColumn, Day.mealAssignmentTable, Day.mainIdColumn, mainId, Day.sideAIdColumn, sideAId, Day.sideBIdColumn, sideBId)
    
        result = connection.runQuery(query)
        idInfo = result.fetchone()
        connection.closeConnection()
    
        if idInfo != None: return idInfo[0]
        else: return None
        
    def updateRecipeAssignment(self, mainDishInput, sideAInput, sideBInput):
        currentMealId = Day.getMealIdFromRecipeNames(self.mainDish, self.sideA, self.sideB)
        inputsMealId = Day.getMealIdFromRecipeNames(mainDishInput, sideAInput, sideBInput)
        inputsMealIdExists = (inputsMealId != None)
        
        if currentMealId != inputsMealId:
            connection = DataConnection()
            
            if not inputsMealIdExists:
                inputsMealId = Utilities.generateNewKey(Day.mealIdColumn, Day.mealAssignmentTable)
                insertQuery = "INSERT INTO {} VALUES (%s, %s, %s, %s)".format(Day.mealAssignmentTable)
                insertBindingVariables = (inputsMealId, Recipe.getExistingRecipe(recipeId=False, recipeName=mainDishInput).recipeId, Recipe.getExistingRecipe(recipeId=False, recipeName=sideAInput).recipeId, Recipe.getExistingRecipe(recipeId=False, recipeName=sideBInput).recipeId)
                connection.updateData(insertQuery, insertBindingVariables)
            
            self.mainDish, self.sideA, self.sideB = mainDishInput, sideAInput, sideBInput
            updateQuery = "UPDATE {} SET {} = %s WHERE {} = {}".format(Day.dayTable, Day.mealIdColumn, Day.dayIdColumn, str(self.dayId))
            updateBindingVariable = (inputsMealId,)
            connection.updateData(updateQuery, updateBindingVariable)
            
            connection.closeConnection()
        
            print("Successfully updated the meal for {}".format(self.dayName))
            print(self)
            
        else:
            print("Meal assignment didn't change for {} -- nothing to do here".format(self.dayName))
    
    def updateRecipeList(dayOfWeek, recipeList, isSide = False):
        isSideA = (dayOfWeek.__contains__(Recipe.sideALabelPrefix))
        isSideB = (dayOfWeek.__contains__(Recipe.sideBLabelPrefix))
        
        if isSide:
            extractedDayOfWeek = Utilities.extractDayName(dayOfWeek)
            mealAssignment = Day.getExistingDay(extractedDayOfWeek)
            
            if isSideA:
                recipeName = mealAssignment.sideA
            elif isSideB:
                recipeName = mealAssignment.sideB
        else:
            mealAssignment = Day.getExistingDay(dayOfWeek)
            recipeName = mealAssignment.mainDish
        
        if recipeList.__contains__(recipeName):
            recipeList.insert(0, recipeList.pop(recipeList.index(recipeName)))
        else:
            print("WARNING: Recipe list '{}' did not contain recipe called '{}'".format(recipeList, recipeName))
            #recipeList.insert(0, "None")
    
        return recipeList    
    
    def add(self):
        connection = DataConnection()
        query = "INSERT INTO {0} ({1},{2},{4},{3}) VALUES(%s, %s, %s);".format(Day.dayTable, Day.dayIdColumn, Day.dayNameColumn, Day.mealIdColumn, Day.weekOfDateColumn)
        
        weekOfDateId = Utilities.getKnownInfo(self.weekOfDate, WeekOfDate.dateIdColumn, WeekOfDate.dateNameColumn, WeekOfDate.dateTable, False)
        insertValue = (self.dayId, self.dayName, weekOfDateId, Day.noneMealId)
        connection.updateData(query, insertValue)
        connection.closeConnection()

        print("Successfully added " + "'" + self.dayName + "' " + "day")
        print(self)

    def generateJoin(weekOfDate, typeId, recipeTypeIdColumn):
        joinString = """{0} join {1} on {0}.{2} = {1}.{3}
                            join {4} on {1}.{5} = {4}.{5}
                            join {6} on {6}.{7} = {4}.{8}
                        where {6}.{9} = '{10}' and {0}.{11} = {12};""".format(Recipe.recipeTable, Day.mealAssignmentTable, Recipe.recipeIdColumn, recipeTypeIdColumn, Day.dayTable, Day.mealIdColumn, WeekOfDate.dateTable, WeekOfDate.dateIdColumn, Day.weekOfDateColumn, WeekOfDate.dateNameColumn, weekOfDate, Recipe.typeIdColumn, typeId)
        
        return joinString

    def __str__(self):        
        message = "--- Summary ---\n"
        message += "Day name: " + self.dayName + "\n"
        message += "Week of date: " + datetime.strftime(self.weekOfDate, "%Y-%m-%d") + "\n"
        message += "Main dish: " + self.mainDish + "\n"
        message += "Side dish A: " + self.sideA + "\n"
        message += "Side dish B: " + self.sideB

        return message
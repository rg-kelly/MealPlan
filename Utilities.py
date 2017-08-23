from DataConnection import DataConnection
#import Recipe
import Type
import Ingredient

# These methods are written in a class-neutral way so that any class can utitilize them

# ----- DEPRECATED -----
# Use getKnownInfo instead
# Method for getting the primary key value for a user-entered value
def getKeyFromValue(descriptionValue, descriptionColumnName, idColumnName, tableName, descriptionIsInteger = False):
    done = False
    idValuePosition = 0
    
    while not done: 
        connection = DataConnection()
        query = "SELECT " + idColumnName + " FROM " + tableName + " WHERE " + descriptionColumnName + " = "
        
        if descriptionIsInteger: query += str(descriptionValue)
        else: query += "'" + descriptionValue + "'"

        result = connection.runQuery(query)
        idValue = result.fetchone()
        connection.closeConnection()

        if (idValue != None):
            done = True
            return str(idValue[idValuePosition]), descriptionValue
        else:
            descriptionValue = handleInvalidEntry(descriptionValue, tableName)

def extractDayName(labelName):
    dayOfWeek = labelName.split("_")[2]
    
    return dayOfWeek

def getKnownInfo(knownInfo, selectColumn, whereColumn, table, whereColumnIsInteger = False):
    infoPosition = 0    
    connection = DataConnection()

    query = "SELECT {} FROM {} WHERE {} = ".format(selectColumn, table, whereColumn)    
    if whereColumnIsInteger: query += str(knownInfo)
    else: query += "'{}'".format(knownInfo)

    result = connection.runQuery(query)
    info = result.fetchone()
    connection.closeConnection()

    if info != None: return info[infoPosition]
    else: return None

def handleInvalidEntry(handleValue, tableName):
    idValuePosition = 0
    retypeMessage = "Please retype the entry here: "

    print(handleValue + " is not currently a valid entry.")

    if (tableName == Recipe.Recipe.recipeTable): # The Recipe table should not have new recipes added to it in this way so 'Retype' is only option
        handleValue = input(retypeMessage)        
    else:
        response = input("Type 'Retype' if you would like to retype the entry or 'New' if you would like to add " + handleValue + ": ")
                               
        if (tableName == Ingredient.Ingredient.ingredientTable):
            if (response == 'New'):
                newIngredient = Ingredient.Ingredient.createNewIngredient(handleValue)
                newIngredient.add()
            else:
                handleValue = input(retypeMessage)                        

        else:
            if (response == 'New'):
                newType = Type(handleValue)
                newType.add()
            else:
                handleValue = input(retypeMessage)

    return handleValue

# Method for calculating new primary key values based on the currently highest value
def generateNewKey(idColumn, tableName):
    idValuePosition = 0
    incrementValue = 1
    
    connection = DataConnection()
    
    query = "SELECT MAX(" + idColumn + ") FROM " + tableName

    result = connection.runQuery(query)
    maxKey = result.fetchone()[idValuePosition]    
    connection.closeConnection()
    
    if (maxKey != None):
        newKey = int(maxKey) + incrementValue
        return newKey
    else: return None

def listOptions(nameColumn, tableName, returnList = False, orderByClause = ""): # Method for displaying all of the possible input options currently available
    listOfOptions = []
    namePosition = 0
    connection = DataConnection()
    
    query = "SELECT " + nameColumn + " FROM " + tableName + " " + orderByClause

    result = connection.runQuery(query)
    resultList = result.fetchall()
    connection.closeConnection()

    if resultList:
        for element in resultList:
            if not returnList: print(element[namePosition])

            if returnList:
                listOfOptions.append(element[namePosition])
            
    else: print("There are currently no options to list.")

    if returnList: return listOfOptions

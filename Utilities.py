from DataConnection import DataConnection

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
        result.close()
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
    result.close()
    connection.closeConnection()

    if info != None: return info[infoPosition]
    else: return None

# Method for calculating new primary key values based on the currently highest value
def generateNewKey(idColumn, tableName):
    idValuePosition = 0
    incrementValue = 1
    
    connection = DataConnection()
    
    query = "SELECT MAX(" + idColumn + ") FROM " + tableName

    result = connection.runQuery(query)
    maxKey = result.fetchone()[idValuePosition]
    result.close()
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
    result.close()
    connection.closeConnection()

    if resultList:
        for element in resultList:
            if not returnList: print(element[namePosition])

            if returnList:
                listOfOptions.append(element[namePosition])
            
    else: print("There are currently no options to list.")

    if returnList: return listOfOptions

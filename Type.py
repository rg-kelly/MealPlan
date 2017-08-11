from DataConnection import DataConnection
import Utilities

class Type:
    typeTable = "Type"
    
    typeIdColumn = "Type_ID"
    typeNameColumn = "Type"

    def __init__(self, typeName):
        self.typeName = typeName

    @classmethod
    def createNewType(cls):
        print("-------------------Add new recipe type-------------------")
        typeName = input("Enter the name of the recipe type: ")
        return Type(typeName)

    @classmethod
    def getTypeName(cls, typeId):
        typeNamePosition = 0
        
        connection = DataConnection()

        query = "SELECT " + Type.typeNameColumn + " FROM " + Type.typeTable
        query += " WHERE " + Type.typeIdColumn + " = " + str(typeId)

        result = connection.runQuery(query)
        typeName = result.fetchone()
        connection.closeConnection()

        return typeName[typeNamePosition]

    def add(self):
        connection = DataConnection()
        query = "INSERT INTO " + Type.typeTable + "(" + Type.typeNameColumn + ") "
        query += "VALUES(%s);"
        
        insertValue = (self.typeName,)
        connection.updateData(query, insertValue)
        connection.closeConnection()

        print("Successfully added " + "'" + self.typeName + "' " + "recipe type")

    def getRecipeTypeId(message): # Message parameter allows use in different contexts
        typeIdPosition = 0

        print(message + " (see the following list for options)")
        Utilities.listOptions(Type.typeNameColumn, Type.typeTable) # Print the list of current recipe types
        recipeType = input("  Recipe type: ")

        typeId = Utilities.getKeyFromValue(recipeType,
                                             Type.typeNameColumn,
                                             Type.typeIdColumn,
                                             Type.typeTable)[typeIdPosition]        
        return recipeType, typeId

    def __str__(self):
        message = "Type name: " + self.typeName

        return message

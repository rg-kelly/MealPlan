from DataConnection import DataConnection
import Utilities

class WeekOfDate:
    dateTable = "WeekOfDate"
    
    dateIdColumn = "Date_ID"
    dateNameColumn = "Week_Of_Date"

    def __init__(self, weekOfDate):
        self.weekOfDate = weekOfDate

    def add(self):
        connection = DataConnection()
        query = "INSERT INTO {} ({}) VALUES('%s');".format(WeekOfDate.dateTable, WeekOfDate.dateNameColumn)
        
        insertValue = (self.dateNameColumn,)
        connection.updateData(query, insertValue)
        connection.closeConnection()

        print("Successfully added " + "'" + self.dateNameColumn + "' " + "recipe type")
        print(self)
            
    def __str__(self):
        message = "Week of date: " + self.dateNameColumn

        return message

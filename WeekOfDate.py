from DataConnection import DataConnection
import Utilities

class WeekOfDate:
    dateTable = "WeekOfDate"
    
    dateIdColumn = "Date_ID"
    dateNameColumn = "Date"

    def __init__(self, weekOfDate):
        self.weekOfDate = weekOfDate

    def add(self):
        connection = DataConnection()
        query = "INSERT INTO {} ({}) VALUES(%s);".format(WeekOfDate.dateTable, WeekOfDate.dateNameColumn)
        print(self.weekOfDate)
        print(query)
        insertValue = (self.weekOfDate,)
        connection.updateData(query, insertValue)
        connection.closeConnection()

        print("Successfully added " + "'" + self.weekOfDate + "'")
        print(self)
            
    def __str__(self):
        message = "Week of date: " + self.weekOfDate

        return message

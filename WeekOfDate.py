from DataConnection import DataConnection
import Utilities
from datetime import datetime

class WeekOfDate:
    dateTable = "WeekOfDate"
    
    dateIdColumn = "Date_ID"
    dateNameColumn = "Date"

    def __init__(self, weekOfDate):
        self.weekOfDate = weekOfDate

    def add(self):
        connection = DataConnection()
        query = "INSERT INTO {} ({}) VALUES(%s);".format(WeekOfDate.dateTable, WeekOfDate.dateNameColumn)
        
        insertValue = (self.weekOfDate,)
        connection.updateData(query, insertValue)
        connection.closeConnection()

        print("Successfully added " + "'" + self.weekOfDate + "'")
        print(self)
        
    def findClosestWeekOfDate():
        connection = DataConnection()
    
        query = "SELECT MIN({0}) FROM {1} WHERE {0} >= CURDATE();".format(WeekOfDate.dateNameColumn, WeekOfDate.dateTable)
    
        result = connection.runQuery(query)
        closestDateResult = result.fetchone()
        connection.closeConnection()
    
        if closestDateResult != None: return closestDateResult[0]
        else: return None              
        
    def __str__(self):
        message = "Week of date: " + self.weekOfDate

        return message

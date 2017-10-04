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
        
    def findClosestWeekOfDate(listOptions = False):
        connection = DataConnection()
        listOfDates = []
        
        if not listOptions:
            query = "SELECT MIN({0}) FROM {1} WHERE ABS(DATEDIFF({0}, NOW())) <= 6;".format(WeekOfDate.dateNameColumn, WeekOfDate.dateTable)
        else:
            query = "SELECT {0} FROM {1} WHERE DATEDIFF({0}, NOW()) >= -6;".format(WeekOfDate.dateNameColumn, WeekOfDate.dateTable)
    
        result = connection.runQuery(query)
        dateResult = result.fetchall()
        result.close()
        connection.closeConnection()
        
        if dateResult != None:
            for item in dateResult:
                date = item[0]
                if date is not None:
                    if not listOptions:
                        return date
                    else:
                        listOfDates.append(datetime.strftime(date, "%Y-%m-%d"))
                else:
                    query = "SELECT MAX({0}) FROM {1};".format(WeekOfDate.dateNameColumn, WeekOfDate.dateTable)
                    connection = DataConnection()
                    result = connection.runQuery(query)
                    dateResult = result.fetchall()
                    result.close()
                    connection.closeConnection()
                    
                    if dateResult != None:
                        for item in dateResult:
                            if not listOptions:
                                return item[0]
                            else:
                                listOfDates.append(datetime.strftime(item[0], "%Y-%m-%d"))
                    break
        
        if listOptions: return listOfDates
        
    def __str__(self):
        message = "Week of date: " + self.weekOfDate

        return message

import mysql.connector

class SimpleDataSource:

    @classmethod
    def getConnection(cls):
        
        return mysql.connector.connect(user='root', password='Westover@64', host='localhost', database='mealplan')


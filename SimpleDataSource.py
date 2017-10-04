import mysql.connector

class SimpleDataSource:

    @classmethod
    def getConnection(cls):
        
        return mysql.connector.connect(user='root', password='Clark106', host='localhost', database='mealplan', port='3306')


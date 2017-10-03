from SimpleDataSource import SimpleDataSource

class DataConnection:

    def __init__(self):
        self.connection = SimpleDataSource.getConnection()
        
    def runQuery(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor

    def updateData(self, query, arguments = ()):
        cursor = self.connection.cursor()
        cursor.execute(query, arguments)
        cursor.close()
        self.connection.commit()
        
    def closeConnection(self):
        self.connection.close()


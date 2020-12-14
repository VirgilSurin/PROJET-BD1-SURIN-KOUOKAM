import sqlite3

class DataBase:

    def __init__(self, dbName):
        self.conn = sqlite3.connect(dbName + ".db")
        self.c = self.conn.cursor()
        self.name = dbName
        
    def __str__(self):
        return "yeet"
        
    def closeconnection(self):
        self.conn.close()
        
class Table:

    def __init__(self, dbName, tableName):
        self.db = DataBase(dbName)
        self.name = tableName
        self.schema = self.getSchema()
        
    def __str__(self):
        s = ""
        for item in self.schema:
            s += str(item) + "\n"
        return s

    def getSchema(self):
        table = self.runQuerry("SELECT * FROM %s"% self.name)
        schema = ""
        for item in table:
            schema += str(item) #TODO it's not yet formatting correctly
        return table

    def runQuerry(self, querry):
        self.db.c.execute(querry)
        res = self.db.c.fetchall()
        return res

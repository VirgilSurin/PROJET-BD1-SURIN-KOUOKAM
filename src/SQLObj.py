import sqlite3

class DataBase:

    def __init__(self, dbName):
        self.conn = sqlite3.connect(dbName + ".db")
        self.c = self.conn.cursor()
        self.name = dbName
        
    def __str__(self):
        return "yeet"
        
    def close_connection(self):
        self.conn.close()
        
class Table:

    def __init__(self, dbName, tableName):
        self.db = DataBase(dbName)
        self.name = tableName
        self.schema = self.get_schema()
        
    def __str__(self):
        s = ""
        for item in self.schema:
            s += str(item) + "\n"
        return s

    def get_schema(self):
        table = self.run_querry("SELECT * FROM %s"% self.name)
        schema = ""
        for item in table:
            schema += str(item) #TODO it's not yet formatting correctly
        return table

    def run_querry(self, querry):
        self.db.c.execute(querry)
        res = self.db.c.fetchall()
        return res


class Attr:
    """
    Represents an attribute inside a relation/table 
    """
    def __init__(self, attrName):
        self.name = attrName

    def __str__(self):
        return str(self.name)

class Cst:
    """
    Represents a constant
    """
    def __init__(self, cstName):
        self.name = cstName

    def __str__(self):
        return str(self.name)

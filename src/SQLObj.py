import sqlite3



class DataBase:
    def __init(self, dbName):
        self.name = dbName
        # connect to the db
        self.connector = sqlite3.connect(name)
        # create a cursor
        self.cursor = connector.cursor()


class Table:
    """
    Represents a table in a dataBase
    
    Attributes :
    foo : foobar
    """
    
    def __init__(self, db, tableName) :
        self.db = db
        self.name = tableName

class Select:
    def __init__(self, operation, table):
        pass

class Rename:
    def __init__(self, oldName, newName, table):
        pass
        

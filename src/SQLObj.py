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

def print_table(querry_result):
    """
    Given the result of a SQLite querry, formats it and displays it correctly on the shell
    
    querry_result must be a list of tuple

    Credits for this function mainly go to Matt Kleinsmith : https://stackoverflow.com/a/9989441/13287218
    """
    length = max(len(str(el)) for row in querry_result for el in row) + 2
    for row in querry_result:
        print("".join(str(el).ljust(length)+"| " for el in row))

def get_attr(table):
    """
    Given a table, will get all the attributes with their type

    return = [(Attr, type), (Attr, type), ..., (Attr, type)]
    """
    row_attr = table.run_querry("PRAGMA table_info(%s)" % table.name)
    return [(el[1], el[2]) for el in row_attr]

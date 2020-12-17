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

    def __init__(self, attr_list, row_list, db, table_name):
        self.attr_list = attr_list
        self.row_list = row_list

        self.db = db
        self.name = table_name

    def __str__(self):
        s = ""
        for item in self.schema:
            s += str(item) + "\n"
        return s

    def load_table(self, attr_list, row_list):
        """
        Create an alternative table object that is load from a given set of data
        instad of beeing loaded from a database
        """
        self.attr_list = attr_list
        self.row_list = row_list
    
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

    def get_attr(self):
        """
        Will get all the attributes with their type from the table
        
        return = [(Attr, type), (Attr, type), ..., (Attr, type)]
        """
        row_attr = run_querry("PRAGMA table_info(%s)" % self.name)
        return [(el[1], el[2]) for el in row_attr]

    

    
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



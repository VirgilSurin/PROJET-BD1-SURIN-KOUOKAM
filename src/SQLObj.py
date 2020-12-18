import sqlite3

class DataBase:
    """
    represent a database and its connection
    """
    def __init__(self, dbName):
        self.conn = sqlite3.connect(dbName + ".db")
        self.c = self.conn.cursor()
        self.name = dbName
        
    def __str__(self):
        return self.name

    def run_query(self, query):
        return self.c.execute(query).fetchall()
    
    def close_connection(self):
        self.conn.close()
        
class Table:
    """
    Represent a Table. is built in two ways :
    
    If attr_list and row_list are not given, fetch the table from the Database.
    Else, will use the given set of data
    """
    def __init__(self, db, table_name,  attr_list=None, row_list=None):
        self.db = DataBase(db)
        self.name = table_name
        if attr_list == None and row_list == None:
            self.attributes = self.get_attr()
            self.rows = self.get_rows()
        else :
            self.attributes = attr_list
            self.rows = row_list

    def __str__(self):
        s = ""
        #it works, believe me. Credits go partially to some nice user from stack overflow
        # https://stackoverflow.com/a/9989441/13287218
        length = max(max(len(str(el)) for row in self.rows for el in row), \
                     max(len(str(attr[0])) for attr in self.attributes)) + 2
        s += "".join(str(attr[0]).ljust(length)+"| " for attr in self.attributes) + "\n"
        s += "+-".join("-"*(length) for i in range(len(self.attributes))) + "+\n"
        for row in self.rows:
            s += "".join(str(el).ljust(length)+"| " for el in row) + "\n"
        return s
    
    def run_query(self, query):
        return self.db.c.execute(query).fetchall()


    def get_attr(self):
        """
        Will get all the attributes with their type from the table
        
        return = [[Attr, type], [Attr, type], ..., [Attr, type]]
        """
        row_attr = self.run_query("PRAGMA table_info(%s)" % self.name)
        return [[el[1], el[2]] for el in row_attr]

    def get_rows(self):
        """
        Will fetch all the rows from a table
        """
        return self.run_query("SELECT DISTINCT * FROM %s" %self.name)
    
class Attr:
    """
    Represents an attribute inside a relation/table 
    """
    def __init__(self, attrName):
        self.name = attrName

    def __str__(self):
        return str(self.name)

    def __eq__(self, other):
        if isinstance(other, Attr):
            return self.name == other.name
    
class Cst:
    """
    Represents a constant
    """
    def __init__(self, cstName):
        self.name = cstName

    def __str__(self):
        return str(self.name)

    def __eq__(self, other):
        if isinstance(other, Cst):
            return self.name == other.name
        


    

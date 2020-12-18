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
    
    def get_schema(self):
        table = self.run_querry("SELECT * FROM %s"% self.name)
        schema = ""
        for item in table:
            schema += str(item) #TODO it's not yet formatting correctly
        return table

    def run_querry(self, querry):
        return self.db.c.execute(querry).fetchall()

    def get_attr(self):
        """
        Will get all the attributes with their type from the table
        
        return = [(Attr, type), (Attr, type), ..., (Attr, type)]
        """
        row_attr = self.run_querry("PRAGMA table_info(%s)" % self.name)
        return [(el[1], el[2]) for el in row_attr]

    def get_rows(self):
        """
        Will fetch all the rows from a table
        """
        return self.run_querry("SELECT DISTINCT * FROM %s" %self.name)
    
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

class Operation:
    """
    represent a valid SQLite operation
    """
    def __init__(self, op):
        self.op = op
        
    def __str__(self):
        return op

    def exec(self, first, second):
        """
        Given two argument, evaluate the expression with the correct operator
        """
        # cast to float, if integer, cast to int
        try:
            arg1 = float(first)
            arg2 = float(second)
        except:
            raise TypeError(str(arg1) + " and " + str(arg2) + " must be int or float")
        
        if arg1.is_integer():
            arg1 = int(arg1)
        if arg2.is_integer():
            arg2 = int(arg2)
            
        if self.op == "=":
            return arg1 == arg2
        elif self.op == ">":
            return arg1 > arg2
        elif self.op == ">=":
            return arg1 >= arg2
        elif self.op == "<":
            return arg1 < arg2
        elif self.op == "<=":
            return arg1 <= arg2
        elif self.op == "!=":
            return arg1 != arg2

        
def print_table(querry_result):
    """
    Given the result of a SQLite querry, formats it and displays it correctly on the shell
    
    querry_result must be a list of tuple
    Credits for this function mainly go to Matt Kleinsmith : https://stackoverflow.com/a/9989441/13287218
    """
    length = max(len(str(el)) for row in querry_result for el in row) + 2
    for row in querry_result:
        print("".join(str(el).ljust(length)+"| " for el in row))

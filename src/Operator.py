from SQLObj import *


# Constants
operator = ["=", "<=", ">=", "<", ">", "!="]


class MonoOperation:
    """
    Represent an SPJRUD operation that is run on a single relation (called table here)
    """
    
    def __init__(self, args, table):
        self.table = t
        self.args = args
        self.querry = ""

    def __str__(self):
        pass

    def run_querry(self):
        return self.table.db.c.execute(self.querry).fetchall()


    def remove_duplicates(self):
        pass

class DualOperation:
    """
    Represent an SPJRUD operation that is run a two relation (called table here)
    """
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2

    def __str__(self):
        pass

class Select(MonoOperation):

    def __init__(self, arg1, op, arg2, t):
        args = (arg1, op, arg2)
        super().__init__(args, t)

        #Argument check
        if not isinstance(arg1, Attr):
            raise TypeError("Invalid argument : arg1 must be an Attr, not " + str(type(arg1)))
        if not isinstance(arg2, Attr) and not isinstance(arg2, Cst):
            raise TypeError("Invalid argument : arg2 must be an Attr or a Cst not " + str(type(arg2)))
        if op not in operator:
            raise TypeError("Invalid operation : it must be =, <=, >=, <, >, !=")

        # Queery building
        self.querry = "SELECT DISTINCT * FROM " + t.name + " WHERE " + str(arg1) + " " + op
        if type(arg2) == Cst:
            self.querry += " \"" + str(arg2) + "\""
        else :
            self.querry += " " + str(arg2)

    def __str__(self):
        super().__init__()


    
t = Table("client", "clients")
s = Select(Attr("Name"), "=", Cst("Shrek"), t)
s2 = Select(Attr("Wallet"), "<", Cst(1000), t)
print(s.run_querry())
print("-------------------------")
print(s2.run_querry())


from SQLObj import *
from CustomException import *

# Constants
operator = ["=", "<=", ">=", "<", ">", "!="]


class MonoOperation:
    """
    Represent an SPJRUD operation that is run on a single relation (called table here)
    """
    
    def __init__(self, args, table):
        self.table = table
        self.args = args
        self.querry = ""
        self.result = None

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
        if not isinstance(t, Table) and not isinstance(t, MonoOperation) \
           and not isinstance(t, DualOperation):
            raise TypeError("Invalid argument : t must be a Table,"\
                            " not " + str(type(t)))
        if not isinstance(arg1, Attr):
            raise TypeError("Invalid argument : arg1 must be an Attr,"\
                            " not " + str(type(arg1)))
        if not isinstance(arg2, Attr) and not isinstance(arg2, Cst):
            raise TypeError("Invalid argument : arg2 must be an Attr or a Cst,"\
                            " not " + str(type(arg2)))
        if op not in operator:
            raise TypeError("Invalid operation : it must be =, <=, >=, <, >, !=")

        # Querry building
        self.querry = "SELECT DISTINCT * FROM " + t.name + " WHERE " + str(arg1) + " " + op
        if type(arg2) == Cst:
            self.querry += " \"" + str(arg2) + "\""
        else :
            self.querry += " " + str(arg2)

        self.result = self.run_querry()
    def __str__(self):
        super().__str__()


class Projection(MonoOperation):

    def __init__(self, args, t):
        super().__init__(args, t)

        # Arguments check
        if not isinstance(t, Table):
            raise TypeError("Invalid argument : t must be a Table, not " + str(type(t)))
        for a in self.args:
            if not isinstance(a, Attr):
                raise TypeError("Invalid argument : args must be a list of Attr, "\
                                " not " + str(type(a)))

        # Querry building
        self.querry = "SELECT DISTINCT "
        for i in range(len(self.args)-1):
            self.querry += str(args[i]) + ", "
        self.querry += str(args[-1]) + " FROM " + self.table.name

    def __str__(self):
        super().__str__()

class Rename(MonoOperation):

    def __init__(self, arg1, arg2, t):
        args = [arg1, arg2]
        super().__init__(args,t)

        # Arguments check
        if not isinstance(t, Table):
            raise TypeError("Invalid argument : t must be a Table," \
                            " not  " + str(type(t)))
        if not isinstance(arg1, Attr):
            raise TypeError("Invalid argument : arg1 must be an Attr," \
                            " not " + str(type(arg1)))
        if not isinstance(arg2, Attr) and not isinstance(arg2, Cst):
            raise TypeError("Invalid argument : arg2 must be an Attr or a Cst" \
                            "not " + str(type(arg2)))

        attr_list = t.get_attr()
        flag = False
        for attr in attr_list:
            if attr[0] == arg1:
                flag = True
                break;
        if not flag:
            raise ArgumentError(str(arg1) + " is not a valid attribute in " + t.name)
        # Querry building
        

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
        #---------------------------------------------------------------------------
        if not isinstance(arg1, Attr):
            raise TypeError("Invalid argument : arg1 must be an Attr,"\
                            " not " + str(type(arg1)))
        else:
            flag = next((True for item in t.attributes if item[0] == arg1.name), False)
            if not flag:
                raise ArgumentError(str(arg1) + " is not an attribute of the table " + t.name)
        #---------------------------------------------------------------------------
        if not isinstance(arg2, Attr) and not isinstance(arg2, Cst):
            raise TypeError("Invalid argument : arg2 must be an Attr or a Cst,"\
                            " not " + str(type(arg2)))
        elif isinstance(arg2, Attr):
            flag = next((True for item in t.attributes if item[0] == arg2.name), False)
            if not flag:
                raise ArgumentError(str(arg1) + " is not an attribute of the table " + t.name)
        #---------------------------------------------------------------------------    
        if op not in operator:
            raise TypeError("Invalid operation : it must be =, <=, >=, <, >, !=")

        # # Querry building - NO NEEDS TO DO A REQUEST, WITH WORK LOCALLY
        # self.querry = "SELECT DISTINCT * FROM " + t.name + " WHERE " + str(arg1) + " " + op
        # if type(arg2) == Cst:
        #     self.querry += " \"" + str(arg2) + "\""
        # else :
        #     self.querry += " " + str(arg2)

        # self.result = self.run_querry()
        #create the table correspon

        #find the index in the attributes list
        column_index = None
        for i in range(len(t.attributes)):
            if arg1.name == t.attributes[i][0]:
                column_index = i
                break
            
        new_rows = []
        if isinstance(arg2, Cst):
            for row in t.rows:
                if row[column_index] == arg2.name:
                    new_rows.append(row)
        else :
            # arg2 is an Attr
            arg2_index = None
            for i in range(len(t.attributes)):
                if arg2.name == t.attributes[i][0]:
                    arg2_index = i
                    break
            for row in t.rows:
                if row[column_index] == row[arg2_index]:
                    new_rows.append()
        #if new_rows is empty, user has made an incorrect querry
        if len(new_rows) == 0:
            raise ArgumentError(str(arg1) + " %s " + str(arg2) + " has returned an empty table")
        self.res_table = Table(t.db.name, t.name, t.attributes, new_rows)
    def __str__(self):
        return str(self.res_table)


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
        

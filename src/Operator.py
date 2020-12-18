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
        self.query = ""
        self.result = None

    def __str__(self):
        pass

    def run_query(self):
        return self.table.db.c.execute(self.query).fetchall()


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
        # if not isinstance(arg1, Attr):
        #     raise TypeError("Invalid argument : arg1 must be an Attr,"\
        #                     " not " + str(type(arg1)))
        # else:
        #     flag = next((True for item in t.attributes if item[0] == arg1.name), False)
        #     if not flag:
        #         raise ArgumentError(str(arg1) + " is not an attribute of the table " + t.name)
        # #---------------------------------------------------------------------------
        # if not isinstance(arg2, Attr) and not isinstance(arg2, Cst):
        #     raise TypeError("Invalid argument : arg2 must be an Attr or a Cst,"\
        #                     " not " + str(type(arg2)))
        # elif isinstance(arg2, Attr):
        #     flag = next((True for item in t.attributes if item[0] == arg2.name), False)
        #     if not flag:
        #         raise ArgumentError(str(arg1) + " is not an attribute of the table " + t.name)
        # #---------------------------------------------------------------------------    
        # if op not in operator:
        #     raise TypeError("Invalid operation : it must be =, <=, >=, <, >, !=")
        
        # Query 
        self.query = "SELECT DISTINCT * FROM " + get_sql(t) + " WHERE " + str(arg1) + " " + op
        if type(arg2) == Cst:
            self.query += " \"" + str(arg2) + "\""
        else :
            self.query += " " + str(arg2)
        
        

    def __str__(self):
        return self.query


class Projection(MonoOperation):

    def __init__(self, args, t):
        super().__init__(args, t)

        # Arguments check
        if not isinstance(t, Table) and not isinstance(t, MonoOperation) \
           and not isinstance(t, DualOperation):
            raise TypeError("Invalid argument : t must be a Table,"\
                            " not " + str(type(t)))
        
        for a in self.args:
            if not isinstance(a, Attr):
                raise TypeError("Invalid argument : args must be a list of Attr, "\
                                " not " + str(type(a)))

        # Query building
        self.query = "SELECT DISTINCT "
        for i in range(len(self.args)-1):
            self.query += str(args[i]) + ", "
        self.query += str(args[-1]) + " FROM " + get_sql(t)

    def __str__(self):
        return self.query

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
            if attr[0] == arg1.name:
                flag = True
                break;
        if not flag:
            raise ArgumentError(str(arg1) + " is not a valid attribute in " + t.name)
        # Query building
        #TODO
        

        
def get_sql(relation):
    """
    Given a relation, will check its type.

    Depending on it's type, will return a string formatted
    to be inserted into a correct SQLite query
    """
    if isinstance(relation, MonoOperation) or isinstance(relation, DualOperation):
        return "(" + relation.query + ")"
    elif isinstance(relation, Table):
        return relation.name
    else:
        raise TypeError("Incorrect type for query, must be a Table or an Mono/DualOperation")

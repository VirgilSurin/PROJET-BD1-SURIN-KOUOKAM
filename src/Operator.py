from SQLObj import *
from CustomException import *
from copy import deepcopy as copy
# Constants
operator = ["=", "<=", ">=", "<", ">", "!="]



class MonoOperation:
    """
    Represent an SPJRUD operation that is run on a single relation (called table here)
    """
    
    def __init__(self, args, table):
        self.table = table
        self.args = args
        self.db = table.db
        self.query = ""
        self.attributes = copy(table.attributes)
        
    def __str__(self):
        return "aaa"

    def run_query(self):
        res = self.table.db.c.execute(self.query).fetchall()
        formatted_res = self.format_res(res)
        return formatted_res

    def format_res(self, query_res):
        """
        Given a query result, will format it to a nice looking table with the attributes
        """
        s = ""
        length = max(max(len(str(el)) for row in query_res for el in row), \
                     max(len(str(attr[0])) for attr in self.attributes)) + 2
        s += "".join(str(attr[0]).ljust(length)+"| " for attr in self.attributes) + "\n"
        s += "+-".join("-"*(length) for i in range(len(self.attributes))) + "+\n"
        for row in query_res:
            s += "".join(str(el).ljust(length)+"| " for el in row) + "\n"
        return s

        
class DualOperation:
    """
    Represent an SPJRUD operation that is run a two relation (called table here)
    """
    def __init__(self, rel1, rel2):
        #Argument check
        if not isinstance(rel1, Table) and not isinstance(rel1, MonoOperation) and \
           not isinstance(rel1, DualOperation):
            raise TypeError("Invalid argument : rel1 must be a Table or an Mono/DualOperation," \
                            " not  " + str(type(rel1)))
        if not isinstance(rel2, Table) and not isinstance(rel2, MonoOperation) and \
           not isinstance(rel2, DualOperation):
            raise TypeError("Invalid argument : rel2 must be a Table or an Mono/DualOperation," \
                            " not  " + str(type(rel2)))

        self.rel1 = rel1
        self.rel2 = rel2
        self.db = rel1.db
        self.attributes = None
        self.query = ""
        
    def __str__(self):
        return self.query

    def run_query(self):
        res = self.rel1.db.c.execute(self.query).fetchall()
        formatted_res = self.format_res(res)
        return formatted_res

    def format_res(self, query_res):
        """
        Given a query result, will format it to a nice looking table with the attributes
        """
        s = ""
        length = max(max(len(str(el)) for row in query_res for el in row), \
                     max(len(str(attr[0])) for attr in self.attributes)) + 2
        s += "".join(str(attr[0]).ljust(length)+"| " for attr in self.attributes) + "\n"
        s += "+-".join("-"*(length) for i in range(len(self.attributes))) + "+\n"
        for row in query_res:
            s += "".join(str(el).ljust(length)+"| " for el in row) + "\n"
        return s
    
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
        
        # Query 
        self.query = "SELECT DISTINCT * FROM " + get_sql(t) + " WHERE " + str(arg1) + " " + op
        if type(arg2) == Cst:
            self.query += " \"" + str(arg2) + "\""
        else :
            self.query += " " + str(arg2)
        
        

    def __str__(self):
        super().__str__()


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

        self.attributes = list(args)

    def __str__(self):
        super().__str__()

class Rename(MonoOperation):

    def __init__(self, arg1, arg2, t):
        args = [arg1, arg2]
        super().__init__(args,t)

        # Arguments check
        if not isinstance(t, Table) and not isinstance(t, MonoOperation) \
           and not isinstance(t, DualOperation):
            raise TypeError("Invalid argument : t must be a Table," \
                            " not  " + str(type(t)))
        if not isinstance(arg1, Attr):
            raise TypeError("Invalid argument : arg1 must be an Attr," \
                            " not " + str(type(arg1)))
        if not isinstance(arg2, Attr) and not isinstance(arg2, Cst):
            raise TypeError("Invalid argument : arg2 must be an Attr or a Cst" \
                            "not " + str(type(arg2)))

        # Query building
        new_attr = Attr(arg2.name)
        flag = False
        for i in range(len(self.attributes)):
            if self.attributes[i][0] == arg1.name:
                self.attributes[i][0] = new_attr.name
                flag = True
                break
        if not flag:
            raise TypeError(new_attr.name + " is not an attribute of the given table")
        
        self.query = "SELECT DISTINCT "
        # we create the selection for all attribures except the last one in the list
        # if the attributes we are on is the one who has been renamed, we place the alias
        for j in range(len(self.attributes)-1):
            if self.attributes[j][0] == new_attr.name:
                self.query += str(arg1) + " AS " + str(new_attr) + ", "
            else :
                self.query += str(self.attributes[j][0]) + ", "
        #same verification for the last one, as we do not want a ","
        if self.attributes[-1][0] == new_attr.name:
            self.query += str(arg1) + " AS " + str(new_attr)
        else :
            self.query += str(self.attributes[-1][0])
            
        self.query += " FROM " + get_sql(t)

    def __str__(self):
        super().__str__()

        
class Join(DualOperation):
    """
    
    """
    def __init__(self, rel1, rel2):
        super().__init__(rel1, rel2)

        self.attributes = copy(rel1.attributes + rel2.attributes)
        self.query = "SELECT DISTINCT * FROM " + get_sql(rel1) + " NATURAL JOIN " + get_sql(rel2)
    

class Difference(DualOperation):
    """

    """
    def __init__(self, rel1, rel2):
        super().__init__(rel1, rel2)
        
        self.attributes = copy(rel1.attributes)
        self.query = "SELECT DISTINCT * FROM " + get_sql(rel1) + " EXCEPT SELECT DISTINCT * FROM " + get_sql(rel2)

    def __str__(self):
        super().__str__()

class Union(DualOperation):
    """
    
    """
    def __init__(self, rel1, rel2):
        super().__init__(rel1, rel2)

        self.attributes = copy(rel1.attributes)
        self.query = "SELECT DISTINCT * FROM " + get_sql(rel1) + " UNION SELECT DISTINCT * FROM " + get_sql(rel2)

    
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
    


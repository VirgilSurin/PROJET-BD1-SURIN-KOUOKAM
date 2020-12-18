import sqlite3
from SQLObj import *
from Operator import *
"""
We need to translate this kind of inputs :
Proj([’Population’], Join(E2, E1))
from low-level request to high level :

E1 = Select(Eq('Country', Cst('Mali')), Rel('CC'))

E2 = Rename('Name', 'Capital', Rel('Cities'))


"""

def exec_manual_querry():
    conn = sqlite3.connect("TestTables.db")
    c = conn.cursor()
    querry = input("Please enter a valid querry : \n")
    #some formatting
    res = c.execute(querry).fetchall()
    for row in res:
        print("".join(str(el).ljust(20) for el in row))

    
emp = Table("TestTables", "emp")
dept = Table("TestTables", "dept")
print(dept)
# sub_quest = Projection((Attr("job"), Attr("ename"), Attr("deptno")), emp)
# main_quest = Join(emp, dept)
op1 = Select(Attr("job"), "=", Cst("CLERK"), emp)
op2 = Select(Attr("job"), "=", Cst("ANALYST"), emp)
union = Union(op1, op2)
print_table(dept.run_query(union.query))
#print_table(emp.run_query(main_quest.query))
print("command executed successfully")
# commit change
#db.commit()
# close the connection
#db.close()

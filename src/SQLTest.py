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
print(emp)
sub_quest = Select(Attr("job"), '=', Cst("ANALYST"), emp)
main_quest = Select(Attr("deptno"),\
                    "=",\
                    Cst("20"),\
                    sub_quest)

print_table(emp.run_query(sub_quest.query))
print("command executed successfully")
# commit change
#db.commit()
# close the connection
#db.close()

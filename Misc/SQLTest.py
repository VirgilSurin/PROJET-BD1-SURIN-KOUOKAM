import sqlite3 as sql

"""
We need to translate this kind of inputs :
Proj([’Population’], Join(E2, E1))
from low-level request to high level :

E1 = Select(Eq('Country', Cst('Mali')), Rel('CC'))

E2 = Rename('Name', 'Capital', Rel('Cities'))


"""
# connect to the db
conn = sql.connect('client.db')

# create a cursor
c = conn.cursor()

c.execute("SELECT * FROM clients")
print(c.fetchall())




print("command executed successfully")
# commit change
conn.commit()
# close the connection
conn.close()

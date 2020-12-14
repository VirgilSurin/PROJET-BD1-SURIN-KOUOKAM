import sqlite3
from SQLObj import *

"""
We need to translate this kind of inputs :
Proj([’Population’], Join(E2, E1))
from low-level request to high level :

E1 = Select(Eq('Country', Cst('Mali')), Rel('CC'))

E2 = Rename('Name', 'Capital', Rel('Cities'))


"""
# connect to the db
#db = sql.connect("client.db")
#c = db.cursor()
# c.execute("""CREATE TABLE clients(
# Name TEXT,
# Id INTEGER,
# Wallet REAL)
# """)
# many_clients = [("Jef", 42, 66.66),
#            ("Dmitri", 1917, 78524.25),
#            ("Keanu", 808, 99999.9),
#            ("Shrek", 2001, 123)]
# c.executemany("INSERT INTO clients VALUES (?,?,?)", many_clients)

# c.execute("SELECT * FROM clients")
# items = c.fetchall()
# for i in items :
#     print(i)

t = Table("client", "clients")
print(t)


print("command executed successfully")
# commit change
#db.commit()
# close the connection
#db.close()

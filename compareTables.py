import sqlite3

conn = sqlite3.connect('simple.db',isolation_level=None)
c = conn.cursor()

c.execute("SELECT * FROM table0")
for row in c:
    print(row)

print("---------------------------------")

a = []
c.execute("SELECT * FROM table1")
for row in c:
    print(row)
    a.append(row)

print("---------------------------------")

# print(a[0])

# if type(a[0][0]) is int:
#     print("hello")

# if (isinstance(a[0][0],str)):
#     print("hey")

joinStatement = "SELECT * FROM table0 INNER JOIN table1 ON table0.ndc = table1.ndc"
c.execute(joinStatement)
for row in c:
    print(row)

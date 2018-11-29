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

c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = c.fetchall()
for table in tables:
        print(table)
print(len(tables))

cursor = c.execute("SELECT * FROM table0")
latestColumns = list(map(lambda x: x[0], cursor.description))
for col in latestColumns:
    print(col)

joinStatement2 = "SELECT COUNT(*) FROM table0 INNER JOIN table1 ON ("
for col in latestColumns:
    joinStatement2 = joinStatement2 + "table0." + col + " = " + "table1." + col
    joinStatement2 = joinStatement2 + " AND "
joinStatement2 = joinStatement2[:-5] + ")"
print(joinStatement2)

commonRowsCount = []
c.execute(joinStatement2)
for row in c:
    print(row)
    commonRowsCount.append(row)

oldTableRowsCount = []
c.execute("SELECT COUNT(*) FROM table0")
for row in c:
    print(row)
    oldTableRowsCount.append(row)

newTableRowsCount = []
c.execute("SELECT COUNT(*) FROM table1")
for row in c:
    print(row)
    newTableRowsCount.append(row)
print(newTableRowsCount[0][0])

changeCount = 0
if newTableRowsCount[0][0] != oldTableRowsCount[0][0]:
    if newTableRowsCount[0][0] > oldTableRowsCount[0][0]:
        changeCount = newTableRowsCount[0][0] - commonRowsCount[0][0]
    else:
        changeCount = oldTableRowsCount[0][0] - commonRowsCount[0][0]
else:
    if commonRowsCount == 0:
        changeCount = newTableRowsCount[0][0]
    else:
        changeCount = newTableRowsCount[0][0] - commonRowsCount[0][0]

print(changeCount)
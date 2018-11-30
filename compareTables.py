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


oldTableRowsCount = []
c.execute("SELECT COUNT(*) FROM table0")
for row in c:
    #print(row)
    oldTableRowsCount.append(row)

newTableRowsCount = []
c.execute("SELECT COUNT(*) FROM table1")
for row in c:
    #print(row)
    newTableRowsCount.append(row)
#print(newTableRowsCount[0][0])

#print(changeCount)
print("---------------------------------")

rowsRemovedCount = []
leftJoinStatement = "SELECT COUNT(*) FROM table0 LEFT OUTER JOIN table1 ON table0.ndc = table1.ndc WHERE table1.year ISNULL"
c.execute(leftJoinStatement)
for row in c:
    print(row)
    rowsRemovedCount.append(row)

print("---------------------------------")
rowsAddedCount = []
revLeftJoinStatement = "SELECT  COUNT(*) FROM table1 LEFT OUTER JOIN table0 ON table0.ndc = table1.ndc WHERE table0.year ISNULL"
c.execute(revLeftJoinStatement)
for row in c:
    print(row)
    rowsAddedCount.append(row)
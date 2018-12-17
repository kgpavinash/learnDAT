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
leftJoinStatement2 = "SELECT * FROM table0 LEFT OUTER JOIN table1 ON table0.ndc = table1.ndc"
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

print("---------------------------------")

checkEmpty = 0
print(str(rowsRemovedCount[0][0])+ " rows has been removed from the old table which had "+str(oldTableRowsCount[0][0]) + " rows")
print(str(rowsAddedCount[0][0])+ " rows has been added to the new table which now has "+str(newTableRowsCount[0][0]) + " rows")
if int(newTableRowsCount[0][0]) == 0:
    print("Shrinkage of 100%")
    print("Growth of 0%")
    checkEmpty = 1
if int(oldTableRowsCount[0][0]) == 0:
    print("Shrinkage of 0%")
    print("Growth of 100%")
    checkEmpty = 1

if checkEmpty == 0:
    shrinkage = str(int(rowsRemovedCount[0][0]) / int(oldTableRowsCount[0][0]) * 100)
    print("Shrinkage of "+shrinkage+"%")
    
    growth = str(int(rowsAddedCount[0][0]) / int(newTableRowsCount[0][0]) * 100)
    print("Growth of "+growth+"%")


print("---------------------------------")

SelectColCount1 = "SELECT COUNT(coalesce(table1." + latestColumns[0] + ",0)) FROM table1"
ColCount1 = []
c.execute(SelectColCount1)
for row in c:
    print(row)
    ColCount1.append(row)

print(ColCount1[0][0])

for col in latestColumns:
    SelectColDifference = "SELECT table0." + col + " FROM table0, table1 WHERE table0.ndc = table1.ndc AND "+ "(SELECT coalesce(table0." + col + ",0)) <> " + "(SELECT coalesce(table1." + col + ",0))"
    print(SelectColDifference)

# print("---------------------------------")

# print("For quarter")
# SelectColQuarter = "SELECT COUNT(*) FROM table0, table1 WHERE table0.ndc = table1.ndc AND (SELECT coalesce(table0.quarter,0)) <> (SELECT coalesce(table1.quarter,0))"
# c.execute(SelectColQuarter)
# for row in c:
#     print(row)

# print("---------------------------------")

# SelectColNullQuarter0 = "SELECT COUNT(coalesce(table1.quarter,0)) FROM table1"
# c.execute(SelectColNullQuarter0)
# for row in c:
#     print(row)

# SelectColNullQuarter1 = "SELECT COUNT(*) FROM table0, table1 WHERE table0.ndc = table1.ndc AND table1.quarter ISNULL"
# c.execute(SelectColNullQuarter1)
# for row in c:
#     print(row)
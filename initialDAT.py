import sqlite3
import json

#Read data from json (Socrata Database)
f = open("somejson2.txt", "r")
content = f.read()
dict_all = json.loads(content)

#Connection to SQLite Database
conn = sqlite3.connect('testing1.db',isolation_level=None)
c = conn.cursor()

#Get count of all tables in the database
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = c.fetchall()
for table in tables:
        print(table)
print(len(tables))


#Get the actual columns dynamically from the json and get the count of columns
allEntryColumns = []
for data in dict_all:
    for data2 in data.items():
         allEntryColumns.append(data2[0])
columns = []
for x in allEntryColumns:
    if x not in columns:
        columns.append(x)
#print(columns)
#print(len(columns))

#Create the CREATE table query. For now, all datatypes are text. Clarify
tableName = "table" + str(len(tables))
createQuery = 'CREATE TABLE ' + tableName + "("
for col in columns:
    createQuery = createQuery + col + " text" + ","
createQuery = createQuery + "PRIMARY KEY (year, quarter, ndc))"
#print(createQuery)

#Get all the entries from the json
allData = []
i = 0
entries = []
for data in dict_all:
        for x in columns:
            allData.append(dict_all[i][x])
        entries.append(allData)
        allData = []
        i = i + 1
#print(entries)

#calculate number of questions marks. Needed as synthax of insert is c.executemany("INSERT INTO table VALUES (?,?,?,?,?...)", entries)
#Create INSERT query
questionList = []
for x in range(len(columns)):
        questionList.append('?')
insertQuery = ",".join(questionList)
insertQuery = "INSERT INTO " + tableName + " VALUES (" + insertQuery + ")"
#print(insertQuery)


#if there are no tables, create the table and populate it. Name of table is "table" + number of tables
if (len(tables) == 0):
    print("There are no tables")
    c.execute(createQuery)
    c.executemany(insertQuery, entries)
    conn.commit()
    conn.close()
    exit()

#comparing columns
latestTable = "table" + str(len(tables) - 1)
cursor = c.execute("SELECT * FROM "+latestTable)
latestColumns = list(map(lambda x: x[0], cursor.description))
print(latestColumns)
print(columns)
if len(columns) != len(latestColumns):
        print("The number of columns have changed.")
        c.execute(createQuery)
        c.executemany(insertQuery, entries)
        conn.commit()
        conn.close()
        exit()
for i in range(len(latestColumns)):
        if columns[i] != latestColumns[i]:
                print("The columns have changed.")
                c.execute(createQuery)
                c.executemany(insertQuery, entries)
                conn.commit()
                conn.close()
                exit()



print("---------------------------------")

#I have to create a new table in order to do value comparison
newTable = tableName
c.execute(createQuery)
c.executemany(insertQuery, entries)

print(latestTable)
print(newTable)

#Outer joins to check if rows have been added or removed
rowsRemovedCount = []
leftJoinStatement = "SELECT COUNT(*) FROM "+latestTable+" LEFT OUTER JOIN "+newTable+" ON "+latestTable+".ndc = "+newTable+".ndc WHERE "+newTable+".year ISNULL"
c.execute(leftJoinStatement)
for row in c:
    print(row)
    rowsRemovedCount.append(row)
rowsAddedCount = []
revLeftJoinStatement = "SELECT COUNT(*) FROM "+newTable+" LEFT OUTER JOIN "+latestTable+" ON "+latestTable+".ndc = "+newTable+".ndc WHERE "+latestTable+".year ISNULL"
c.execute(revLeftJoinStatement)
for row in c:
    print(row)
    rowsAddedCount.append(row)

latestTableRowsCount = []
c.execute("SELECT COUNT(*) FROM "+latestTable)
for row in c:
    #print(row)
    latestTableRowsCount.append(row)

newTableRowsCount = []
c.execute("SELECT COUNT(*) FROM "+newTable)
for row in c:
    #print(row)
    newTableRowsCount.append(row)

checkEmpty = 0
print(str(rowsRemovedCount[0][0])+ " rows has been removed from the old table which had "+str(latestTableRowsCount[0][0]) + " rows")
print(str(rowsAddedCount[0][0])+ " rows has been added to the new table which now has "+str(newTableRowsCount[0][0]) + " rows")
if int(newTableRowsCount[0][0]) == 0:
    print("Shrinkage of 100%")
    print("Growth of 0%")
    checkEmpty = 1
if int(latestTableRowsCount[0][0]) == 0:
    print("Shrinkage of 0%")
    print("Growth of 100%")
    checkEmpty = 1

if checkEmpty == 0:
    shrinkage = str(int(rowsRemovedCount[0][0]) / int(latestTableRowsCount[0][0]) * 100)
    print("Shrinkage of "+shrinkage+"%")
    
    growth = str(int(rowsAddedCount[0][0]) / int(newTableRowsCount[0][0]) * 100)
    print("Growth of "+growth+"%")


print("---------------------------------")

#Count number of values (including null) in a column
SelectColCount1 = "SELECT COUNT(coalesce("+newTable+"." + latestColumns[0] + ",0)) FROM " +newTable
ColCount1 = []
c.execute(SelectColCount1)
for row in c:
    ColCount1.append(row)

print(ColCount1[0][0])

print("---------------------------------")

#print table values for manual comparison
c.execute("SELECT * FROM "+latestTable)
for row in c:
    print(row)

print("---------------------------------")

c.execute("SELECT * FROM "+newTable)
for row in c:
    print(row)

print("---------------------------------")

#compare values between the two tables
for col in latestColumns:
    SelectColDifference = "SELECT COUNT(coalesce("+latestTable+"." + col + ",0)) FROM "+latestTable+", "+newTable+" WHERE " +latestTable+".ndc = "+newTable+".ndc AND "+ "(SELECT coalesce("+latestTable+"." + col + ",0)) <> " + "(SELECT coalesce("+newTable+"." + col + ",0))"
    print(SelectColDifference)
    c.execute(SelectColDifference)
    for row in c:
        print(row)
        #print(row[0])
        #print(ColCount1[0][0])
        change = str(int(row[0]) / int(ColCount1[0][0]) * 100)
        print("Change of "+change+"% in "+ col)

#delete newtable if there are no changes. Delete always for now.
c.execute("DROP TABLE " + newTable)

#close connection
conn.commit()
conn.close()

import sqlite3
import json

#Connection to SQLite Database
conn = sqlite3.connect('testing3.db',isolation_level=None)
c = conn.cursor()

#Get count of all tables in the database
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = c.fetchall()

#Get all columns and entries from all files.
columns = []
entries = []
f = open("countFile.txt", "r")
fileCount = f.read()
index = -1
while index != int(fileCount):
    index = index + 1
    f = open("jsonResult"+str(index)+".txt", "r")
    content = f.read()
    dict_all = json.loads(content)
    allEntryColumns = []
    for data in dict_all:
        for data2 in data.items():
            allEntryColumns.append(data2[0])
    for x in allEntryColumns:
        if x not in columns:
            columns.append(x)
    allData = []
    i = 0
    for data in dict_all:
        for x in columns:
            try:
                allData.append(dict_all[i][x])
            except:
                allData.append("~")
        entries.append(allData)
        allData = []
        i = i + 1

#Create the CREATE table query. For now, all datatypes are text. Clarify
tableName = "table" + str(len(tables))
createQuery = 'CREATE TABLE ' + tableName + "("
for col in columns:
    createQuery = createQuery + col + " text" + ","
createQuery = createQuery + "PRIMARY KEY (year, quarter, ndc))"
# print(createQuery)

#calculate number of questions marks. Needed as synthax of insert is c.executemany("INSERT INTO table VALUES (?,?,?,?,?...)", entries)
#Create INSERT query
questionList = []
for x in range(len(columns)):
        questionList.append('?')
insertQuery = ",".join(questionList)
insertQuery = "INSERT INTO " + tableName + " VALUES (" + insertQuery + ")"
# print(insertQuery)

#if there are no tables, create the table and populate it. Name of table is "table" + number of tables (Takes around 6 minutes)
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
#print(latestColumns)
#print(columns)
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

print("No Change in number/values of columns")

print("---------------------------------")

#I have to create a new table in order to do value comparison
newTable = tableName
c.execute(createQuery)
c.executemany(insertQuery, entries)

#Outer joins to check if rows have been added/removed. Gets count of rows added/removed
rowsRemovedCount = []
leftJoinStatement = "SELECT COUNT(*) FROM "+latestTable+" LEFT OUTER JOIN "+newTable+" ON "+latestTable+".ndc = "+newTable+".ndc WHERE "+newTable+".year ISNULL"
c.execute(leftJoinStatement)
for row in c:
    #print(row)
    rowsRemovedCount.append(row)
rowsAddedCount = []
revLeftJoinStatement = "SELECT COUNT(*) FROM "+newTable+" LEFT OUTER JOIN "+latestTable+" ON "+latestTable+".ndc = "+newTable+".ndc WHERE "+latestTable+".year ISNULL"
c.execute(revLeftJoinStatement)
for row in c:
    #print(row)
    rowsAddedCount.append(row)

#Gets number of rows from the latest table in the database
latestTableRowsCount = []
c.execute("SELECT COUNT(*) FROM "+latestTable)
for row in c:
    #print(row)
    latestTableRowsCount.append(row)

#Gets number of rows from the new table just inserted into database
newTableRowsCount = []
c.execute("SELECT COUNT(*) FROM "+newTable)
for row in c:
    #print(row)
    newTableRowsCount.append(row)

#Gets count of rows which has same NDC between latest and new table. (Compare with matching NDC)
matchingNDCCount = []
c.execute("SELECT COUNT(*) FROM "+latestTable+", "+newTable+" WHERE " +latestTable+".ndc = "+newTable+".ndc")
for row in c:
        #print(row)
        matchingNDCCount.append(row)

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
    shrinkage = str(int(rowsRemovedCount[0][0]) / int(matchingNDCCount[0][0]) * 100)
    print("Shrinkage of "+shrinkage+"%")
    
    growth = str(int(rowsAddedCount[0][0]) / int(matchingNDCCount[0][0]) * 100)
    print("Growth of "+growth+"%")

#Count number of values (including null) in a column (Maybe change this to just count rows in any one column. Same thing)
SelectColCount1 = "SELECT COUNT(coalesce("+newTable+"." + latestColumns[0] + ",\"~\")) FROM " +newTable
ColCount1 = []
c.execute(SelectColCount1)
for row in c:
    ColCount1.append(row)

#compare values of every element in each column between two tables where the NDC matches
hasChanged = 0
for col in latestColumns:
    SelectColDifference = "SELECT COUNT(coalesce("+latestTable+"." + col + ",\"~\")) FROM "+latestTable+", "+newTable+" WHERE " +latestTable+".ndc = "+newTable+".ndc AND "+ "(SELECT coalesce("+latestTable+"." + col + ",\"~\")) <> " + "(SELECT coalesce("+newTable+"." + col + ",\"~\"))"
    #print(SelectColDifference)
    c.execute(SelectColDifference)
    for row in c:
        #print(row)
        #print(row[0])
        #print(ColCount1[0][0])
        change = str(int(row[0]) / int(ColCount1[0][0]) * 100)
        print("Change of "+change+"% in "+ col)
        if change != 0:
                hasChanged = 1

#delete newtable if there are no changes.
if (hasChanged == 0):
        c.execute("DROP TABLE " + newTable)
        conn.commit()
        conn.close()
        exit()
if (shrinkage == 0):
        c.execute("DROP TABLE " + newTable)
        conn.commit()
        conn.close()
        exit()
if (growth == 0):
        c.execute("DROP TABLE " + newTable)
        conn.commit()
        conn.close()
        exit()

# print(columns)
# print(len(entries))
# print(entries)

# finalQuery = 'SELECT * WHERE year = ' + maxyear +' AND quarter = '+maxQuarter+' ORDER BY ndc DESC LIMIT 50000'
# result = client.get(medic_identifier, query=finalQuery)
# jsonFormat = json.dumps(result, indent=4)
# f = open("jsonResult0.txt", "w+")
# f.write(jsonFormat)
# finalQuery3 = 'SELECT * WHERE year = ' + maxyear +' AND quarter = '+maxQuarter+' ORDER BY ndc DESC OFFSET 50000 LIMIT 50000'

# countFile = 0
# countOffset = 50000
# result = client.get(medic_identifier, query=finalQuery3)
# while result:
#     countFile = countFile + 1
#     countOffset = countOffset + 50000
#     jsonFormat = json.dumps(result, indent=4)
#     f = open("jsonResult"+str(countFile)+".txt", "w+")
#     f.write(jsonFormat)
#     finalQuery3 = 'SELECT * WHERE year = ' + maxyear +' AND quarter = '+maxQuarter+' ORDER BY ndc DESC OFFSET '+str(countOffset)+' LIMIT 50000'
#     result = client.get(medic_identifier, query=finalQuery3)

# #write count of files to file.
# f = open("countFile.txt", "w+")
# f.write(str(countFile))



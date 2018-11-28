import sqlite3
import json

#Read data from json (Socrata Database)
f = open("somejson.txt", "r")
content = f.read()
dict_all = json.loads(content)

#Connection to SQLite Database
conn = sqlite3.connect('example2.db')
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

#Print all entries in a table
# c.execute('''SELECT * FROM table1''')
# for row in c:
#     print(row)

#delete the table
#c.execute("DROP TABLE table0")

#comparing columns
hasColumnChanged = False
latestTable = "table" + str(len(tables) - 1)
cursor = c.execute("SELECT * FROM "+latestTable)
latestColumns = list(map(lambda x: x[0], cursor.description))
print(latestColumns)
print(columns)
if len(columns) != len(latestColumns):
        print("The number of columns have changed.")
for i in range(len(latestColumns)):
        if columns[i] != latestColumns[i]:
                print("The columns have changed.")
                hasColumnChanged = True
                break        
#TBD compare values!

#Create a new table and populate it. (If there are any differences)
#c.execute(createQuery)
#c.executemany(insertQuery, entries)


#Ending
conn.commit()
conn.close()
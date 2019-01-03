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



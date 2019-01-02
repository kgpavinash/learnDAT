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

print(columns)
print(len(entries))
print(entries)





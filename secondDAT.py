import sqlite3
import json

#Connection to SQLite Database
conn = sqlite3.connect('testing3.db',isolation_level=None)
c = conn.cursor()

#Get count of all tables in the database
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = c.fetchall()

columns = []
entries = []

f = open("countFile.txt", "r")
fileCount = f.read()
i = -1
while i != int(fileCount):
    i = i + 1
    f = open("jsonResult"+str(i)+".txt", "r")
    content = f.read()
    dict_all = json.loads(content)
    allEntryColumns = []
    for data in dict_all:
        for data2 in data.items():
            allEntryColumns.append(data2[0])
    for x in allEntryColumns:
        if x not in columns:
            columns.append(x)

print(columns)






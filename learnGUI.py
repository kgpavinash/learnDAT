from tkinter import *
from math import *
import sqlite3
import json
# top = Tk()
# top.title("Data Acquisition Tool")
# top.geometry('400x500')
# top.configure(background="light blue")
# but0 = Button(top,text='Start',width=5,height=3)
# but0.pack()
# top.mainloop()

# fred = Button(self, fg="red", bg="blue")
# fred["fg"] = "red"
# fred["bg"] = "blue"
# fred.config(fg="red", bg="blue")

# class Application(Frame):
#     def __init__(self, master=None):
#         super().__init__(master)
#         self.master = master
#         self.pack()
#         self.create_widgets()

#     def create_widgets(self):
#         self.hi_there = Button(self)
#         self.hi_there["text"] = "Hello World\n(click me)"
#         self.hi_there["command"] = self.say_hi
#         self.hi_there.pack(side="top")

#         self.quit = Button(self, text="QUIT", fg="red",
#                               command=self.master.destroy)
#         self.quit.pack(side="bottom")

#     def say_hi(self):
#         print("hi there, everyone!")

# root = Tk()
# app = Application(master=root)
# app.mainloop()

# lst = ['a', 'b', 'c', 'd']
# root = Tk()
# t = Text(root)
# for x in lst:
#     t.insert(END, x + '\n')
# t.pack()
# root.mainloop()

# def show_entry_fields():
#    print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))

# master = Tk()
# master.geometry('400x500')
# Label(master, text="First Name").grid(row=0)
# Label(master, text="Last Name").grid(row=1)

# e1 = Entry(master)
# e2 = Entry(master)

# e1.grid(row=0, column=1)
# e2.grid(row=1, column=1)

# Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
# Button(master, text='Show', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=4)

# master.mainloop()

# def evaluate(event):
#     res.configure(text = "Ergebnis: " + str(eval(entry.get())))
# w = Tk()
# Label(w, text="Your Expression:").pack()
# entry = Entry(w)
# entry.bind("<Return>", evaluate)
# entry.pack()
# res = Label(w)
# res.pack()
# w.mainloop()

# def evaluate(event):
#     res.configure(text = "Ergebnis: "+entry.get())
# w = Tk()
# entry = Entry(w)
# entry.bind("<Return>", evaluate)
# entry.pack(side="bottom")
# res = Label(w)
# res.pack(side="top")
# w.mainloop()

# def evaluate():
#     res.configure(text = "Text: "+entry.get())

# master = Tk()
# Button(master,text="Click",command=evaluate).grid(row=0, column=0)
# entry = Entry(master)
# entry.grid(row=0, column=1)
# res = Label(master)
# res.grid(row=2, column=0)
# master.mainloop()

columns = []
entries = []
f = open("countFiles.txt", "r")
fileCount = f.read()
index = 0
while index != int(fileCount):
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
    index = index + 1


displayText = ""
master = Tk()
master.geometry('800x800')
master.title("Data Acquisition Tool")
# master.geometry('800x500')
lst = ['package_size_code', 'fda_ther_equiv_code', 'fda_application_number', 'clotting_factor_indicator','year','fda_product_name','sdfsdf','sdfsdf','dsfd']
ents = []
i = 0
j = 1
k = 1
for e in columns:
    if i != 0 and i % 4 == 0:
        j = j + 4
        k = k + 1.35
        i = 0
        # print("hello")
    lab = Label(master, text = e + " %")
    lab.place(x = (i * 200), y = 10 * j)
    e = Entry(master,width=5)
    e.insert(0,"0")
    e.place(x = (i * 200), y = 30 * k)
    ents.append(e)
    i = i + 1
#     Button(master,text=e, height=1,width=1,background="light blue",font=("Courier", 15)).grid(row=i, column=0,padx=10, pady=10)
def started():
    # showText = []
    #Connection to SQLite Database
    conn = sqlite3.connect('testing3.db',isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()

    #Create the CREATE table query. For now, all datatypes are text. Clarify
    tableName = "table" + str(len(tables))
    createQuery = 'CREATE TABLE ' + tableName + "("
    for col in columns:
        createQuery = createQuery + col + " text" + ","
    createQuery = createQuery + "PRIMARY KEY (year, quarter, ndc))"

    #calculate number of questions marks. Needed as synthax of insert is c.executemany("INSERT INTO table VALUES (?,?,?,?,?...)", entries)
    #Create INSERT query
    questionList = []
    for x in range(len(columns)):
        questionList.append('?')
    insertQuery = ",".join(questionList)
    insertQuery = "INSERT INTO " + tableName + " VALUES (" + insertQuery + ")"
    
    if (len(tables) == 0):   
        print("There are no tables")
        # c.execute(createQuery)
        # c.executemany(insertQuery, entries)
        # conn.commit()
        c.execute("begin")
        c.execute(createQuery)
        c.executemany(insertQuery, entries)
        c.execute("commit")
        conn.close()
        # exit()
        textResult.delete('0.0',END)
        displayText = "There are no tables"
        textResult.insert(INSERT, displayText)
        return

    #comparing columns
    latestTable = "table" + str(len(tables) - 1)
    cursor = c.execute("SELECT * FROM "+latestTable)
    latestColumns = list(map(lambda x: x[0], cursor.description))
    #print(latestColumns)
    #print(columns)
    if len(columns) != len(latestColumns):
        print("The number of columns have changed.")
        displayText = "The number of columns have changed\n"
        # c.execute(createQuery)
        # c.executemany(insertQuery, entries)
        # conn.commit()
        c.execute("begin")
        c.execute(createQuery)
        c.executemany(insertQuery, entries)
        c.execute("commit")
        conn.close()
        exit()
    for i in range(len(latestColumns)):
        if columns[i] != latestColumns[i]:
                print("The columns have changed.")
                displayText = "The columns have changed\n"
                # c.execute(createQuery)
                # c.executemany(insertQuery, entries)
                # conn.commit()
                c.execute("begin")
                c.execute(createQuery)
                c.executemany(insertQuery, entries)
                c.execute("commit")
                conn.close()
                exit()
    displayText = "No Change in number/values of columns\n---------------------------------\n"
    #I have to create a new table in order to do value comparison
    newTable = tableName
    # c.execute(createQuery)
    # c.executemany(insertQuery, entries)
    c.execute("begin")
    c.execute(createQuery)
    c.executemany(insertQuery, entries)
    c.execute("commit")

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
    displayText = displayText + str(rowsRemovedCount[0][0])+ " rows has been removed from the old table which had "+str(latestTableRowsCount[0][0]) + " rows\n"
    displayText = displayText + str(rowsAddedCount[0][0])+ " rows has been added to the new table which now has "+str(newTableRowsCount[0][0]) + " rows\n"
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
        displayText = displayText + "Shrinkage of "+shrinkage+"%\n"
        growth = str(int(rowsAddedCount[0][0]) / int(matchingNDCCount[0][0]) * 100)
        print("Growth of "+growth+"%")
        displayText = displayText + "Growth of "+growth+"%\n"
    
    #Count number of values (including null) in a column (Maybe change this to just count rows in any one column. Same thing)
    SelectColCount1 = "SELECT COUNT(coalesce("+newTable+"." + latestColumns[0] + ",\"~\")) FROM " +newTable
    ColCount1 = []
    c.execute(SelectColCount1)
    for row in c:
        ColCount1.append(row)
    
    #compare values of every element in each column between two tables where the NDC matches
    hasChanged = 0
    i = 0
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
            displayText = displayText + "Change of "+change+"% in "+ col + "\n"
            if change != '0.0':
                    hasChanged = 1
            perc = ents[i].get()
            if (int(perc) < int(float(change))):
                displayText = displayText + "HUGE CHANGE!\n"
            i = i + 1
    i = 0

    #delete newtable if there are no changes.
    if (hasChanged == 0 and shrinkage == '0.0' and growth == '0.0'):
        c.execute("DROP TABLE " + newTable)
        conn.commit()
        conn.close()
        print("No changes. The newtable is deleted")
        displayText = displayText + "No changes. The newtable is deleted"
        textResult.delete('0.0',END)
        textResult.insert(INSERT, displayText)
        return
    
    conn.commit()
    conn.close()
    textResult.delete('0.0',END)
    textResult.insert(INSERT, displayText)
    return
def reset():
    textResult.delete('0.0',END)
    textResult.insert(INSERT, "Shows the percentage change/rows removed results.")
    for e in ents:
        e.delete(0,END)
        e.insert(0,"0")

start = Button(text="Start", command=started)
start.place(x = 630, y = 360)
reset = Button(text="Reset", command=reset)
reset.place(x = 680, y = 360)
textResult = Text(master)
textResult.insert(INSERT, "Shows the percentage change/rows removed results.")
textResult.place(x = 75, y = 400)
vscroll = Scrollbar(master, orient=VERTICAL, command=textResult.yview)
vscroll.place(in_=textResult, relx=1.0, relheight=1.0, bordermode="outside")
master.mainloop()

# master = Tk()

# group = LabelFrame(master, text="Group", padx=5, pady=5)
# group.pack(padx=10, pady=10)

# w = Entry(group)
# w.pack()

# mainloop()


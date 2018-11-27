import sqlite3
import json

f = open("somejson.txt", "r")
content = f.read()
dict_all = json.loads(content)

conn = sqlite3.connect('example.db')
c = conn.cursor()

#get the actual fields dynamically from the json.
input0 = []
for data in dict_all:
    for data2 in data.items():
         input0.append(data2[0])

output0 = []
questionCount = 0
for x in input0:
    if x not in output0:
        questionCount = questionCount + 1
        output0.append(x)

#print(output0)
#print(questionCount)

allData = []
i = 0
result = []
for data in dict_all:
        for x in output0:
                allData.append(dict_all[i][x])
                #print(x)
                #print(i)
                #print(dict_all[i][x])
        result.append(allData)
        allData = []
        i = i + 1

#print(result)

#calculates number of question marks(entries) and creates INSERT query
questionList = []
for x in range(questionCount):
        questionList.append('?')
insertString = ",".join(questionList)
insertString = "INSERT INTO drugs2 VALUES (" + insertString + ")"
#print(insertString)

#c.executemany(insertString, result)

#print("\n")

#print(key[0])

# sql = 'DELETE from drugs2'
# c.execute(sql)

# c.execute('''SELECT * FROM drugs''')
# for row in c:
#         print(row)
        

# c.execute('''CREATE TABLE drugs2(
#  package_size_core integer, 
#  fda_ther_equiv_code text, 
#  fda_application_number integer, 
#  clotting_factor_indicator text,
#  year integer, 
#  fda_product_name text,
#  labeler_name text, 
#  ndc integer, 
#  product_code integer, 
#  unit_type text, 
#  fda_approval_date text,
#  market_date text,
#  pediatric_indicator text,
#  package_size_intro_date text, 
#  units_per_pkg_size integer, 
#  labeler_code integer, 
#  desi_indicator integer, 
#  drug_category text,
#  quarter integer, 
#  cod_status integer,
#  PRIMARY KEY (year, quarter, ndc))''')

c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = c.fetchall()
for table in tables:
        print(table)
print(len(tables))


conn.commit()
conn.close()
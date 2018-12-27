import urllib.request, json
import ijson
import time
#  39,642
# columns = []
# parser = ijson.parse(urllib.request.urlopen('https://data.medicaid.gov/resource/4qik-skk9.json?$limit=5'))
# for prefix, event, value  in parser:
#     if (event == 'map_key'):
#         if value not in columns:
#             columns.append(value)
# print(columns)

# print("----")

start_time = time.time()
print(start_time)

item_gen = ijson.items(urllib.request.urlopen('https://data.medicaid.gov/resource/4qik-skk9.json?$limit=10'), 'item')
somelist = []
for item in item_gen:
    somelist.append(item)
    #print(item)

#print(somelist)
#print(somelist[0]["year"])

print("----")

maxYear = 0
maxQuarter = 0

for thing in somelist:
    if (int(thing["year"]) > int(maxYear)):
        maxYear = thing["year"]
print(maxYear)

index = 0

for thing in somelist:
    if(thing["year"] == maxYear):
        if(int(thing["quarter"]) > int(maxQuarter)):
            maxQuarter = thing["quarter"]
print(maxQuarter)

updatedList = []
for thing in somelist:
    if(thing["year"] == maxYear and thing["quarter"] == maxQuarter):
        updatedList.append(thing)

print(updatedList)


# s = str(updatedList)
# f = open("djson.txt", "w+")
# f.write(str(s))

with open('your_file.txt', 'w+') as f:
    for item in updatedList:
        f.write("%s\n" % item)

dict_all = updatedList

allEntryColumns = []
for data in dict_all:
    for data2 in data.items():
         allEntryColumns.append(data2[0])
columns = []
for x in allEntryColumns:
    if x not in columns:
        columns.append(x)
print(columns)

# print("----")

# allData = []
# i = 0
# entries = []
# for data in dict_all:
#         for x in columns:
#             try:
#                 allData.append(dict_all[i][x])
#             except:
#                 allData.append("~")
#         entries.append(allData)
#         allData = []
#         i = i + 1
# print(entries[0])

    

import urllib.request, json
import ijson

# columns = []
# parser = ijson.parse(urllib.request.urlopen('https://data.medicaid.gov/resource/4qik-skk9.json?$limit=5'))
# for prefix, event, value  in parser:
#     if (event == 'map_key'):
#         if value not in columns:
#             columns.append(value)
# print(columns)

# print("----")

item_gen = ijson.items(urllib.request.urlopen('https://data.medicaid.gov/resource/4qik-skk9.json?$limit=5'), 'item')
somelist = []
other = item_gen
for item in item_gen:
    somelist.append(item)
    #print(item)

#print(somelist)
#print(somelist[0]["year"])

#print("----")

s = str(somelist)

mys = s.replace("'",'"')

#print(mys)

dict_all = json.loads(str(mys))
#print(dict_all)

allEntryColumns = []
for data in dict_all:
    for data2 in data.items():
         allEntryColumns.append(data2[0])
columns = []
for x in allEntryColumns:
    if x not in columns:
        columns.append(x)
print(columns)

print("----")

allData = []
i = 0
entries = []
for data in dict_all:
        for x in columns:
            try:
                allData.append(dict_all[i][x])
            except:
                allData.append("~")
        entries.append(allData)
        allData = []
        i = i + 1
print(entries[0])

    

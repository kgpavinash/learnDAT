import json
from sodapy import Socrata


medic_domain = 'data.medicaid.gov'
medic_identifier = 'v48d-4e3e'
client = Socrata(medic_domain,None)

#Get the latest year
resultMaxYear = client.get(medic_identifier, query='SELECT MAX(year)')
jsonFormatYear = json.dumps(resultMaxYear, indent=4)
dict_year = json.loads(jsonFormatYear)
#print(dict_year[0]['max_year'])
maxyear = dict_year[0]['max_year']

#Get the latest quarter from the latest year
quarterQuery = 'SELECT MAX(quarter) where year = ' +maxyear
resultMaxQuarter = client.get(medic_identifier, query=quarterQuery)
jsonFormatQuarter = json.dumps(resultMaxQuarter,indent=4)
dict_quarter = json.loads(jsonFormatQuarter)
maxQuarter = dict_quarter[0]['max_quarter']

#Queries to be used. Limited to 50,000 results per call. Get first 50,000. 
finalQuery = 'SELECT * WHERE year = ' + maxyear +' AND quarter = '+maxQuarter+' ORDER BY ndc DESC LIMIT 50000'
finalQuery2 = 'SELECT COUNT(*) WHERE year = ' + maxyear +' AND quarter = '+maxQuarter
finalQuery3 = 'SELECT * WHERE year = ' + maxyear +' AND quarter = '+maxQuarter+' ORDER BY ndc DESC OFFSET 50000 LIMIT 50000'
result = client.get(medic_identifier, query=finalQuery)
#print(result)
jsonFormat = json.dumps(result, indent=4)
#print(jsonFormat)
#eh = json.loads(jsonFormat)
metadata = client.get_metadata(medic_identifier)
jsonFormatMetadata = json.dumps(metadata, indent=4)
#print(jsonFormatMetadata)

#write first 50,000 results to file
# f = open("jsonResult0.txt", "w+")
# f.write(jsonFormat)

#get actual count of results
result = client.get(medic_identifier, query=finalQuery2)
print(result)
print("-----")

#Keep getting results until it is empty. Write every 50,000 results to file. Keep track of number of files
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

countFiles = 0
countOffset = 0
while 1:
    loopQuery = 'SELECT * WHERE year = ' + maxyear +' AND quarter = '+maxQuarter+' ORDER BY ndc DESC OFFSET '+str(countOffset)+' LIMIT 50000'
    result = client.get(medic_identifier, query=loopQuery)
    if not result:
        break
    jsonFormat = json.dumps(result, indent=4)
    f = open("jsonResult"+str(countFiles)+".txt", "w+")
    f.write(jsonFormat)
    countOffset = countOffset + 50000
    countFiles = countFiles + 1

countFiles = countFiles - 1
f = open("countFile.txt", "w+")
f.write(str(countFiles))
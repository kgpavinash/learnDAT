import json
from sodapy import Socrata

medic_domain = 'data.medicaid.gov'
medic_identifier = 'yns6-zx8k'
medic_token = "fKE9JUu49N4tnTi3XBGQsE2xl"

client = Socrata(medic_domain, medic_token)

resultMaxYear = client.get(medic_identifier, query='SELECT MAX(year)')
maxyear = resultMaxYear[0]['max_year']
# print(maxyear)

monthQuery = 'SELECT MAX(month) where year = ' +maxyear
resultMaxMonth = client.get(medic_identifier, query=monthQuery)
maxMonth = resultMaxMonth[0]['max_month']
maxMonth = '11'
# print(maxMonth)

countQuery = 'SELECT count(*) WHERE year = '+maxyear+' AND month = '+maxMonth
countResult = client.get(medic_identifier,query=countQuery)
print(countResult)

countFiles = 0
countOffset = 0
while 1:
    loopQuery = 'SELECT * WHERE year = ' + maxyear +' AND month = '+maxMonth+' ORDER BY month DESC OFFSET '+str(countOffset)+' LIMIT 50000'
    result = client.get(medic_identifier, query=loopQuery)
    if not result:
        break
    jsonFormat = json.dumps(result, indent=4)
    f = open("jsonResult"+str(countFiles)+".txt", "w+")
    f.write(jsonFormat)
    countOffset = countOffset + 50000
    countFiles = countFiles + 1

f = open("countFiles.txt", "w+")
f.write(str(countFiles))

f = open("identifier.txt","w+")
f.write(str(medic_identifier))
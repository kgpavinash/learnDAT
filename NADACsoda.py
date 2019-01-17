import json
from sodapy import Socrata


medic_domain = 'data.medicaid.gov'
medic_identifier = 'tau9-gfwr'
medic_token = "fKE9JUu49N4tnTi3XBGQsE2xl"

client = Socrata(medic_domain, medic_token)

resultMaxAsOfDate = client.get(medic_identifier, query='SELECT MAX(as_of_date)')
maxyear = resultMaxAsOfDate[0]['MAX_as_of_date']

maxyear = "'%s'" % maxyear  # add quotes to the maxyear. Needed for query to be valid
MaxDateResultQuery = 'SELECT COUNT(*) WHERE as_of_date = '+maxyear
print(MaxDateResultQuery)

result = client.get(medic_identifier,query = MaxDateResultQuery)
print(result)


countFiles = 0
countOffset = 0
while 1:
    loopQuery = 'SELECT * WHERE as_of_date = '+maxyear+' ORDER BY ndc DESC OFFSET '+str(countOffset)+' LIMIT 50000'
    print(loopQuery)
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

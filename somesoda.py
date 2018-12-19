import json
from sodapy import Socrata


medic_domain = 'data.medicaid.gov'
medic_identifier = 'v48d-4e3e'
client = Socrata(medic_domain,None)

resultMaxYear = client.get(medic_identifier, query='SELECT MAX(year)')
jsonFormatYear = json.dumps(resultMaxYear, indent=4)
dict_year = json.loads(jsonFormatYear)
#print(dict_year[0]['max_year'])
maxyear = dict_year[0]['max_year']

quarterQuery = 'SELECT MAX(quarter) where year = ' +maxyear
resultMaxQuarter = client.get(medic_identifier, query=quarterQuery)
jsonFormatQuarter = json.dumps(resultMaxQuarter,indent=4)
dict_quarter = json.loads(jsonFormatQuarter)
maxQuarter = dict_quarter[0]['max_quarter']

finalQuery = 'SELECT * WHERE year = ' + maxyear +' AND quarter = '+maxQuarter+' ORDER BY ndc DESC LIMIT 50000'
finalQuery2 = 'SELECT COUNT(*) WHERE year = ' + maxyear +' AND quarter = '+maxQuarter
result = client.get(medic_identifier, query=finalQuery)
#print(result)
jsonFormat = json.dumps(result, indent=4)
#print(jsonFormat)
#eh = json.loads(jsonFormat)
metadata = client.get_metadata(medic_identifier)
jsonFormatMetadata = json.dumps(metadata, indent=4)
#print(jsonFormatMetadata)

#print(eh[0]['package_size_code'])
#print(eh)

f = open("testjson.txt", "w+")
f.write(jsonFormat)


result = client.get(medic_identifier, query=finalQuery2)
print(result)




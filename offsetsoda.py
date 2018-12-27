import json
from sodapy import Socrata

medic_domain = 'data.medicaid.gov'
medic_identifier = 'v48d-4e3e'
client = Socrata(medic_domain,None)

finalQuery = 'SELECT * LIMIT 2'
finalQuery2 = 'SELECT * OFFSET 2 LIMIT 3'
finalQuery3 = 'SELECT * LIMIT 5'
result = client.get(medic_identifier, query=finalQuery)
jsonFormat = json.dumps(result, indent=4)
print(jsonFormat)
result = client.get(medic_identifier, query=finalQuery2)
jsonFormat2 = json.dumps(result, indent=4)
#print(jsonFormat2)
print("------")
result = client.get(medic_identifier, query=finalQuery3)
jsonFormat3 = json.dumps(result, indent=4)
#print(jsonFormat3)

combjson = jsonFormat2 + jsonFormat3
print(combjson)

import urllib.request, json 
with urllib.request.urlopen("https://data.medicaid.gov/resource/4qik-skk9.json?$limit=50000") as url:
    data = json.loads(url.read().decode())
    #output_dict = [x for x in data if x['year'] == '2018']
    #print(output_dict)
    #jsonFormat = json.dumps(data, indent=4)
    #print(jsonFormat)
    year = 0
    for key in data:
        if int(key['year']) > int(year):
            year = key['year']
    print(year)
    output_dict = [x for x in data if x['ndc'] == "99207085060"]

    print(output_dict)

    # quarter = 0
    # for key in output_dict:
    #     #print(key['quarter'])
    #     if int(key['quarter']) > int(quarter):
    #         quarter = key['quarter']
    # print(quarter)

    # print(output_dict)
    # jsonFormat = json.dumps(output_dict, indent=4)
    # print(jsonFormat)
    


    # print(output_dict)
    # jsonFormat = json.dumps(data, indent=4)
    # print(jsonFormat)

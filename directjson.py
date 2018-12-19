import urllib.request, json 
with urllib.request.urlopen("https://data.medicaid.gov/resource/4qik-skk9.json?$limit=10") as url:
    data = json.loads(url.read().decode())
    print(data)
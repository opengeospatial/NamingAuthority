import json
  
# Opening JSON file
f = open('/glossary.json',)
  
# returns JSON object as
# a dictionary
data = json.load(f)
  
# Iterating through the json
# list
for i in data['GLOSSARY']['INFO']['ENTRIES']['ENTRY']:
    print(""+i['CONCEPT'])
  
# Closing file
f.close()
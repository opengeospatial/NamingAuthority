import json
import urllib.request
import pandas as pd

URL = "https://raw.githubusercontent.com/opengeospatial/NamingAuthority/refs/heads/master/definitions/docs/docs.json"

with urllib.request.urlopen(URL) as resp:
    data = json.load(resp)

df = pd.DataFrame.from_dict(data, orient="index")
df.index.name = "id"
df.reset_index(inplace=True)

df.to_excel("docs.xlsx", index=False)
print("Saved docs.xlsx")

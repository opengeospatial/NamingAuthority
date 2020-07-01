# OGC Catalogue Services 3.0 - General Model
identifier = "12-168r6"
specURL = "http://docs.opengeospatial.org/is/12-168r6/12-168r6.html"
fout = open("../mappings/"+identifier+".csv","w") # output file
fin = open("../specifications/"+identifier+".txt","r") # input file
elementList = []

# processing the input file

for line in fin:
    tokens = line.split()
    for token in tokens:
        if token.endswith(","):
            token = token.replace(",","")
        if token.endswith("."):
            token = token[:len(token)-1]
        if "/req/" in token:
            elementList.append(token)
            elementList.append(token.replace("/req/","/conf/"))

# Handling duplicates

elementList = list(dict.fromkeys(elementList))  # remove duplicates

# Now we write out the output

for e in elementList:
    if e.startswith("http"):
        fout.write(specURL+","+e+"\n")

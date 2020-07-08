# SensorThings API - Part 2 1.0
identifier = "17-079r1"
specURL = "http://docs.opengeospatial.org/is/17-079r1/17-079r1.html"
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
        if "/conf/" in token:
            elementList.append(token)


# Handling duplicates

elementList = list(dict.fromkeys(elementList))  # remove duplicates

# Now we write out the output

for e in elementList:
    if e.startswith("http"):
        fout.write(specURL+","+e+"\n")

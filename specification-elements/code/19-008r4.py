# OGC GeoTIFF
specURL = "http://docs.opengeospatial.org/is/19-008r4/19-008r4.html"
fout = open("../mappings/19-008r4.csv","w")  # output file
fin = open("../specifications/19-008r4.txt","r") # input file
elementList = []

# processing the input file

for line in fin:
    tokens = line.split()
    for token in tokens:
        if token.endswith(","):
            token = token.replace(",","")
        if "/req/" in token:
            elementList.append(token)
        if "/conf/" in token:
            elementList.append(token)

# Handling duplicates

elementList = list(dict.fromkeys(elementList))  # remove duplicates
elementList.remove("http://www.opengis.net/spec/GeoTIFF/1.1/conf/TIFF.Tags.") # this is also a duplicate that is missed by the previous line because of period at end

# Now we write out the output

for e in elementList:
    fout.write(specURL+","+e+"\n")

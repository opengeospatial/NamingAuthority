# CDB 1.1 Vol 5
identifier = "16-004r4"
specURL = "https://portal.opengeospatial.org/files/16-004r4"
fout = open("../mappings/"+identifier+".csv","w") # output file
fin = open("../specifications/"+identifier+".txt","r") # input file
elementList = []

# processing the input file

for line in fin:
    line = line.replace("\n","")
    if "req/" in line:
        elementList.append(line[line.index("req/"):])
    if "conf/" in line:
        elementList.append(line[line.index("conf/"):])


# Handling duplicates

elementList = list(dict.fromkeys(elementList))  # remove duplicates

# Now we write out the output

for e in elementList:
    fout.write(specURL+",http://www.opengis.net/spec/1.1/cdb-radar/"+e.replace("req/","")+"\n")

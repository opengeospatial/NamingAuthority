# CDB 1.1 Vol 4
identifier = "16-070r3"
specURL = "https://portal.opengeospatial.org/files/16-070r3"
fout = open("../mappings/"+identifier+".csv","w") # output file
fin = open("../specifications/"+identifier+".txt","r") # input file
elementList = []

# processing the input file

for line in fin:
    line = line.replace("\n","")
    if "/req/" in line:
        elementList.append(line[line.index("/req/"):])
    if "/conf/" in line:
        elementList.append(line[line.index("/conf/"):])


# Handling duplicates

elementList = list(dict.fromkeys(elementList))  # remove duplicates

# Now we write out the output

for e in elementList:
    if "req/" in e:
        fout.write(specURL+",http://www.opengis.net/spec/cdb/1.1/shapefile"+e.replace("req/","")+"\n")
    if "conf/" in e:
        fout.write(specURL+",http://www.opengis.net/spec/cdb-shapefile/1.0/conf"+e.replace("conf/","")+"\n")

# CDB 1.1 Vol 1
identifier = "15-113r5"
specURL = "https://portal.opengeospatial.org/files/15-113r5"
fout = open("../mappings/"+identifier+".csv","w") # output file
fin = open("../specifications/"+identifier+".txt","r",encoding='utf-8') # input file
elementList = []

# processing the input file
elementtext = {}

currentelement = None
for line in fin:
    line = line.replace("\n","")
    if currentelement and line :
        elementtext[currentelement] = line
        currentelement = None
    if "/req/" in line:
        currentelement = line[line.index("/req/"):]
        elementList.append(currentelement)
    if "/conf/" in line:
        elementList.append(line[line.index("/conf/"):])


# Handling duplicates

elementList = list(dict.fromkeys(elementList))  # remove duplicates

# Now we write out the output

for e in elementList:
    fout.write(specURL+",http://www.opengis.net/spec/cdb/1.0"+e.replace("req/","")+"\n")

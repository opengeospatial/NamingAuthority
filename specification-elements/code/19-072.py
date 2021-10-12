# Draft OGC API - Common - Part : Core
identifier = "19-072"
specURL = "http://docs.ogc.org/DRAFTS/19-072.html"
fout = open("../mappings/"+identifier+".csv","w") # output file
fin = open("../specifications/"+identifier+".txt","r") # input file
elementList = []

# processing the input file

for line in fin:
    if "\"http://www.opengis.net/spec/ogcapi-common" in line:
        token = line[line.index("http://www.opengis.net/spec/ogcapi-common"):]
        token2 = token[:token.index("\"")]
        print(token2)
        fout.write(token2+"\n")

fout.close()
fin.close()

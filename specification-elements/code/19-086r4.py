# OGC API - Environmental Data Retrieval Standard
identifier = "19-086r4"
specURL = "https://docs.ogc.org/is/19-086r4/19-086r4.html"
fout = open("../mappings/"+identifier+".csv","w") # output file
fin = open("../specifications/"+identifier+".txt","r") # input file
elementList = []

# processing the input file

for line in fin:
    if "\"http://www.opengis.net/spec/ogcapi-edr-1/1.0" in line:
        token = line[line.index("http://www.opengis.net/spec/ogcapi-edr-1/1.0"):]
        token2 = token[:token.index("\"")]
        print(token2)
        fout.write(token2+"\n")
    if ">http://www.opengis.net/spec/ogcapi-edr-1/1.0" in line:
        token = line[line.index("http://www.opengis.net/spec/ogcapi-edr-1/1.0"):]
        token2 = token[:token.index("<")]
        print(token2)
        fout.write(token2+"\n")

fout.close()
fin.close()

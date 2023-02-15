# OGC API - Tiles
identifier = "20-057"
specURL = "https://docs.ogc.org/is/20-057/20-057.html"
fout = open("../mappings/"+identifier+".csv","w") # output file
fin = open("../specifications/"+identifier+".html","r") # input file
elementList = []

# processing the input file

fout.write("https://docs.ogc.org/is/20-057/20-057.html,http://www.opengis.net/doc/IS/ogcapi-tiles-1/1.0\n")


for line in fin:
    if ("<table id=" in line) and ("class=\"modspec\"" in line):
        #print(line)
        if "/req/" in line:
            token1 = line[line.index("/req/"):]
            if "</tt>" in token1:
                token2 = token1[:token1.index("</tt>")]
                token_a1 = line[line.index("<table id=")+len("<table id=")+1:line.index("\" class=\"modspec\"")]
                if "ats_" in token_a1:
                    print("Do nothing")
                else:
                    fout.write("https://docs.ogc.org/is/20-057/20-057.html#"+token_a1+","+"http://www.opengis.net/spec/ogcapi-tiles-1/1.0"+token2+"\n")

        if "/conf/" in line:
            token1 = line[line.index("/conf/"):]
            if "</tt>" in token1:
                token2 = token1[:token1.index("</tt>")]
                token_a1 = line[line.index("<table id=")+len("<table id=")+1:line.index("\" class=\"modspec\"")]
                fout.write("https://docs.ogc.org/is/20-057/20-057.html#"+token_a1+","+"http://www.opengis.net/spec/ogcapi-tiles-1/1.0"+token2+"\n")



fout.close()
fin.close()

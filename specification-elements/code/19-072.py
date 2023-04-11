# OGC API - Common - Part : Core
identifier = "19-072"
specURL = "https://docs.ogc.org/is/19-072/19-072.html"
fout = open("../mappings/"+identifier+".csv","w") # output file
fin = open("../specifications/"+identifier+".html","r") # input file
elementList = []

# processing the input file
# Identifier</th><td style=\"border-top:solid windowtext 1.5pt;border-bottom:solid windowtext 1.0pt;\"><tt>

token2 = ""
for line in fin:
    if "Identifier</th><td style=\"border-top:solid windowtext 1.5pt;border-bottom:solid windowtext 1.0pt;\"><tt>" in line:
        token = line[line.index("Identifier</th><td style=\"border-top:solid windowtext 1.5pt;border-bottom:solid windowtext 1.0pt;\"><tt>"):]
        token2 = token[:token.index("</tt>")]
        token2 = token2.replace("Identifier</th><td style=\"border-top:solid windowtext 1.5pt;border-bottom:solid windowtext 1.0pt;\"><tt>","")
        if token2.startswith('/'):
            token2 = "http://www.opengis.net/spec/ogcapi-common-1/1.0"+token2
        print("\n"+token2)
        #fout.write(token2+"\n")
    if "<table id=\"" in line:
        table_token = line[line.index("<table id=\"")+len("<table id=\""):]
        table_token = table_token[:table_token.index("\"")]
        print(table_token)
        fout.write("https://docs.ogc.org/is/19-072/19-072.html#"+table_token+","+token2.replace("\n","")+"\n")
fout.close()
fin.close()

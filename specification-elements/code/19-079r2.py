# OGC API - Features - Part 3

def cleanString(intext):
    intext = intext.replace("\"","")
    if "</" in intext:
        intext = intext[:intext.index("</")]
    if intext.startswith("/req/") or intext.startswith("/conf/") or intext.startswith("/rec/") or intext.startswith("/per/") or intext.startswith("/conf/"):
        intext = "http://www.opengis.net/spec/ogcapi-features-3/1.0"+intext
    return intext

specURL = "https://docs.ogc.org/is/19-079r2/19-079r2.html"
fout = open("../mappings/19-079r2.csv","w")  # output file
fin = open("../specifications/19-079r2.html","r") # input file
elementList = []

# processing the input file

idtoken = ""
readingAnnex = 0

for line in fin:
    tokens = line.split()
    for token in tokens:
        if token.startswith("id=\""):
            idtoken = token.replace("id=\"","")
            idtoken = idtoken[:idtoken.index("\"")]
            print (idtoken)
        if "id=\"_abstract_test_suite_normative\"" in token:
            readingAnnex = 1
        if readingAnnex == 0:
            if "/req/" in token:
                if "http:" in token:
                    token = token[token.index("http:"):]
                    elementList.append(idtoken+","+cleanString(token))
                else:
                    token = token[token.index("/req/"):]
                    elementList.append(idtoken+","+cleanString(token))
            if "/conf/" in token:
                if "http:" in token:
                    token = token[token.index("http:"):]
                    elementList.append(idtoken+","+cleanString(token))
                else:
                    token = token[token.index("/conf/"):]
                    elementList.append(idtoken+","+cleanString(token))
            if "/rec/" in token:
                token = token[token.index("/rec/"):]
                elementList.append(idtoken+","+cleanString(token))
            if "/per/" in token:
                token = token[token.index("/per/"):]
                elementList.append(idtoken+","+cleanString(token))
        if readingAnnex == 1:
            if "/ats/" in token:
                token = token[token.index("/conf/"):]
                elementList.append(idtoken+","+cleanString(token))
# Handling duplicates

elementList = list(dict.fromkeys(elementList))  # remove duplicates

# Now we write out the output

for e in elementList:
    if "example_" not in e:
        fout.write(specURL+"#"+e+"\n")
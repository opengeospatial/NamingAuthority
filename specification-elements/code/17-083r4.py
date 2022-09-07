# 2D TMS v2.0
identifier = "17-083r4"
specURL = "https://docs.ogc.org/is/17-083r4/17-083r4.html"
fout = open("../mappings/"+identifier+".csv","w") # output file
fin = open("../specifications/"+identifier+".txt","r") # input file
elementList = []

# processing the input file

for line in fin:
    if "http://www.opengis.net/spec/tms/2.0/req/" in line:
        print(re.search("(?P<url>https?://[^\s]+)", line).group("url"))
    if "http://www.opengis.net/spec/tms/2.0/conf/" in line:
        print(re.search("(?P<url>https?://[^\s]+)", line).group("url"))


# Handling duplicates

elementList = list(dict.fromkeys(elementList))  # remove duplicates

# Now we write out the output

for e in elementList:
    if e.startswith("http"):
        fout.write(specURL+","+e+"\n")

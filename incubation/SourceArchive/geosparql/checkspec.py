'''
This script is was created to help verify that all URIs in the Standards document are also in the TTL files.
'''


import os, re

path = "/Users/ogckm/Downloads/ogc-geosparql-master/1.1/spec"



files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.adoc' in file:
            files.append(os.path.join(r, file))

fout = open('/Users/gobehobona/Documents/GitHub/NamingAuthority/incubation/geosparql/urlout.txt','w')
for f in files:
    print("### " +f)
    fin = open(str(f),'r')
    lines = fin.readlines()
    for line in lines:
        for url in re.findall('(http://\S+)', line):
            if "http://www.opengis.net/ont/geosparql#":
                print("\n") 
            if "www.opengis.net" in url:
                print(url)
                fout.write(url+"\n")

    fin.close()
fout.close()
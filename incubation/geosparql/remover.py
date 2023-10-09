'''
This script is was created to help verify that all URIs in the Standards document are also in the TTL files.
'''

fin = open('/Users/ogckm/Documents/GitHub/NamingAuthority/incubation/geosparql/urlout.txt','r')
fout = open('/Users/ogckm/Documents/GitHub/NamingAuthority/incubation/geosparql/secondout.txt','w')

lines = fin.readlines()

for line in lines:
    if "http://www.opengis.net/ont/geosparql" in line:
        print("")
    elif "http://www.opengis.net/ont/sf" in line:
        print("")
    elif "http://www.opengis.net/ont/gml" in line:
        print("")
    elif "http://www.opengis.net/def/function/geosparql/" in line:
        print("")
    elif "http://www.opengis.net/def/crs/" in line:
        print("")   
    elif "http://www.opengis.net/kml/2.2" in line:
        print("")  
    elif "http://www.opengis.net/gml/3.2" in line:
        print("")   
    elif "http://www.opengis.net/doc/" in line:
        print("")  
    elif "http://www.opengis.net/def/uom/OGC/1.0/" in line:
        print("")     
    elif "http://www.opengis.net/def/SRS/EPSG/0/4326" in line:
        print("")       
    elif "http://www.opengis.net/def/geosparql/validator" in line:
        print("")    
    elif "http://www.opengis.net/spec/geosparql" in line:
        print("")   
    elif "http://www.opengis.net/def/rule/geosparql" in line:
        print("")                                                                 
    else:
        fout.write(line)

fout.close()
fin.close()
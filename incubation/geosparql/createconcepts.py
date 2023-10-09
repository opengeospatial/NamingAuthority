f = open('/Users/gobehobona/Documents/GitHub/NamingAuthority/incubation/geosparql/alllines.txt','r')
fout = open('/Users/gobehobona/Documents/GitHub/NamingAuthority/incubation/geosparql/fix400errors.ttl','w')

lines = f.readlines()

for line in lines:
    fout.write("<"+line.replace('\n','')+"> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2004/02/skos/core#Concept> .\n")
    fout.write("<"+line.replace('\n','')+"> <http://www.w3.org/2000/01/rdf-schema#label> \""+line[1+line.rindex('/'):].replace('\n','')+"\"@en .\n")
    fout.write("<"+line.replace('\n','')+"> <http://www.w3.org/2004/02/skos/core#prefLabel> \""+line[1+line.rindex('/'):].replace('\n','')+"\"@en .\n")
    fout.write("<"+line.replace('\n','')+"> <http://www.w3.org/2004/02/skos/core#definition> \"Definition of "+line[1+line.rindex('/'):].replace('\n','')+"\"@en .\n")
    fout.write("<"+line.replace('\n','')+"> <http://www.w3.org/2004/02/skos/core#inScheme> <http://www.opengis.net/def/geosparql/funcsrules> .\n")


'''
<https://www.opengis.net/def/property/OGC-EO/0/NadirGroundResolution> <http://purl.org/dc/terms/created> "2023-05-25"^^<http://www.w3.org/2001/XMLSchema#date> .
<https://www.opengis.net/def/property/OGC-EO/0/NadirGroundResolution> <http://purl.org/dc/terms/modified> "2023-05-26"^^<http://www.w3.org/2001/XMLSchema#date> .
<https://www.opengis.net/def/property/OGC-EO/0/NadirGroundResolution> <http://www.w3.org/2002/07/owl#sameAs> <http://www.opengis.net/def/property/OGC-EO/0/NadirGroundResolution> .
<https://www.opengis.net/def/property/OGC-EO/0/NadirGroundResolution> <http://www.w3.org/2004/02/skos/core#inScheme> <https://www.opengis.net/def/alias-register> .
<https://www.opengis.net/def/property/OGC-EO/0/NadirGroundResolution> <http://www.w3.org/2004/02/skos/core#prefLabel> "Alias of https://www.opengis.net/def/property/OGC-EO/0/NadirGroundResolution"@en .
<https://www.opengis.net/def/property/OGC-EO/0/NadirGroundResolution> <http://www.opengis.net/def/metamodel/ogc-na/status> <http://www.opengis.net/def/status/experimental> .
'''

f.close()


import os, re
import rdflib
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD


folderpath = "/Users/gobehobona/Documents/GitHub/NamingAuthority/incubation/geosparql/second_attempt/triples_to_clear"

g = rdflib.Graph()

for root, dirs, files in os.walk(folderpath):
    print (root, "consumes")
    for name in files:
        print(name)
        print(folderpath+"/"+name)
        g.parse(folderpath+"/"+name)
        print(len(g))

g.serialize(destination="/Users/gobehobona/Documents/GitHub/NamingAuthority/incubation/geosparql/geosparqlfiles2.nt",format="nt")



fin = open("/Users/gobehobona/Documents/GitHub/NamingAuthority/incubation/geosparql/geosparqlfiles2.nt",'r')
lines = fin.readlines()

fout = open("/Users/gobehobona/Documents/GitHub/NamingAuthority/incubation/geosparql/20231206_delete_geosparqlfiles.nt",'w')


for line in lines:
    if "_:" in line:
        print("do nothing")
    else:
        fout.write(line);

fout.close()

'''
FIRST START FUSEKI

/Users/ogckm/Tools/apache-jena-fuseki-4.5.0/fuseki-server --file "/Users/ogckm/Downloads/geosparqlfiles.ttl" /geosparql

THEN EXPORT ALL definition triples to all_defs_queryResults.ttl with this:

CONSTRUCT {?subject ?predicate ?object} WHERE {
 ?subject ?predicate ?object
 FILTER (isURI(?subject) && STRSTARTS(str(?subject), str('http://www.opengis.net/def/') ) )
}

Then export distinct def URIs to distinct_def_uris.csv with this:

SELECT DISTINCT ?subject {
 ?subject ?predicate ?object
 FILTER (isURI(?subject) && STRSTARTS(str(?subject), str('http://www.opengis.net/def/') ) )
}


'''


import os, re
import rdflib
import requests
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD

'''
pip3 install rdflib
pip3 install requests
'''

fout = open('/Users/gobehobona/Documents/GitHub/NamingAuthority/incubation/geosparql/20231206_url_statuses.csv','w')


path = "/Users/gobehobona/Documents/GitHub/NamingAuthority/incubation/geosparql/second_attempt/triples_to_add"

g = rdflib.Graph()

for dirpath, subdirs, files in os.walk(path):
    for name in files:
        if name.endswith(".ttl"):
            print(os.path.join(dirpath, name))
            g.parse(os.path.join(dirpath, name))


#g.serialize(destination="/Users/gobehobona/Documents/GitHub/NamingAuthority/incubation/geosparql/20231206_insert_aliases.nt",format="nt")


#g1 = rdflib.Graph()
#g1.parse("file:///Users/gobehobona/Documents/GitHub/NamingAuthority/incubation/geosparql/20231206_insert_aliases.nt")


knows_query = """
SELECT DISTINCT ?subject {
 ?subject ?predicate ?object
 FILTER (isURI(?subject) && STRSTARTS(str(?subject), str('http://www.opengis.net/def/') ) )
}"""

all_def_uris = []

qres = g.query(knows_query)
for row in qres:
    all_def_uris.append(f"{row.subject}")

for subject in all_def_uris:
    print(subject)
    r = requests.head(str(subject))
    if r.status_code == 303:
        r2 = requests.head(r.headers['Location'])
        if not(r2.status_code==200):
            fout.write(str(r2.status_code)+","+str(r.headers['Location']).replace('&_mediatype=text/turtle','').replace('http://defs.opengis.net/vocprez/object?uri=','')+"\n")


fout.close()


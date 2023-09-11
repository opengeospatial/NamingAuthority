import csv
import rdflib
from datetime import datetime
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD


import os


#k = rdflib.URIRef('http://www.opengis.net/def/cs/OGC/1.0')
#print(k)

#if 1<2:
#    exit(0)

def unique(list1):
 
    unique_list = []
 
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    for x in unique_list:
        print(x)



g = rdflib.Graph()

path = '/Users/gobehobona/Documents/GitHub/NamingAuthority/definitions/conceptschemes'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.ttl' in file:
            files.append(os.path.join(r, file))

for f in files:
    print(f)
    if "external_docs.ttl" in str(f):
        print("..SKIPPED")
        continue
    g.parse(str(f))

all_query = """
SELECT ?s ?p ?o
WHERE {
    ?s ?p ?o.
}"""

unique_list = []

qres = g.query(all_query)
print("start...")
for row in qres:
    concept = row.s
    if "http://www.opengis.net/def" in concept:
        if concept not in unique_list:
            unique_list.append(concept)    
print("...end")

print("\nPrint unique list")
fout = open('/Users/ogckm/Documents/GitHub/NamingAuthority/incubation/aliases/alias_register.ttl','w')
for ct in unique_list:
    if "geotiff-tag" not in ct and "?" not in ct: #geotiff-tags already included
        fout.write("\n")
        print(ct)
        ctx = ct.replace("http://","https://")
        fout.write("<https://example.org> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2004/02/skos/core#Concept> .\n".replace("http://example.org",ct).replace("https://example.org",ctx))
        fout.write("<https://example.org> <http://www.w3.org/2000/01/rdf-schema#label> \"Alias of https://example.org\"@en .\n".replace("http://example.org",ct).replace("https://example.org",ctx))
        fout.write("<https://example.org> <http://purl.org/dc/terms/created> \"2023-05-25\"^^<http://www.w3.org/2001/XMLSchema#date> .\n".replace("http://example.org",ct).replace("https://example.org",ctx))
        fout.write("<https://example.org> <http://purl.org/dc/terms/modified> \"2023-05-26\"^^<http://www.w3.org/2001/XMLSchema#date> .\n".replace("http://example.org",ct).replace("https://example.org",ctx))
        fout.write("<https://example.org> <http://www.w3.org/2004/02/skos/core#definition> \"This is an alias of the concept referenced by the sameAs predicate.\"@en .\n".replace("http://example.org",ct).replace("https://example.org",ctx))
        fout.write("<https://example.org> <http://www.w3.org/2002/07/owl#sameAs> <http://example.org> .\n".replace("http://example.org",ct).replace("http://example.org",ct).replace("https://example.org",ctx))
        fout.write("<https://example.org> <http://www.w3.org/2004/02/skos/core#inScheme> <https://www.opengis.net/def/alias-register> .\n".replace("http://example.org",ct).replace("https://example.org",ctx))
        fout.write("<https://example.org> <http://www.w3.org/2004/02/skos/core#prefLabel> \"Alias of https://example.org\"@en .\n".replace("http://example.org",ct).replace("https://example.org",ctx))
        fout.write("<https://example.org> <http://www.opengis.net/def/metamodel/ogc-na/status> <http://www.opengis.net/def/status/experimental> .\n".replace("http://example.org",ct).replace("https://example.org",ctx))

fout.close()

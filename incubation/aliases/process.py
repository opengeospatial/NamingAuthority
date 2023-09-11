import csv
import rdflib
from datetime import datetime
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD


import os

g = rdflib.Graph()

path = '/Users/ogckm/Documents/GitHub/NamingAuthority/definitions/conceptschemes'

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
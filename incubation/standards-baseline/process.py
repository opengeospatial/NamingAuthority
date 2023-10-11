# Script created to support the generation of Turtle-encoded content for the OGC GeoTIFF Tag Register
# Created: 2023-10-11
# Author: Gobe Hobona (OGC)

import csv
import rdflib
from datetime import datetime
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD



g = rdflib.Graph()
g.parse('standards_input.ttl')
fout = open('standards.ttl','w')
fout.write(g.serialize(format="nt"))
fout.close()

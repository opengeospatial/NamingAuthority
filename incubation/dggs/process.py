# cd /incubation/dggs
# then copy this folder https://github.com/opengeospatial/ogcapi-discrete-global-grid-systems/tree/master/registry/dggrs
# pip install rdflib
# python3 process.py

import os
import json
import rdflib
from datetime import datetime
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD


ttlOutputFileName = "dggrs.ttl"
conceptNamespace = "https://www.opengis.net/def/dggrs/OGC/1.0"
schemeURI = "https://www.opengis.net/def/dggrs"
collectionAndSchemeLabel = "DGGRS Register"
collectionAndSchemeDefinition = "This is a register of Discrete Global Grid Reference Systems. "
github_raw_folder = "https://raw.githubusercontent.com/opengeospatial/ogcapi-discrete-global-grid-systems/refs/heads/master/registry/dggrs/OGC/1.0/"


# Do not edit below this line
collectionURI = schemeURI+"/"

g = rdflib.Graph()
g.bind("foaf", FOAF)
g.bind("xsd", XSD)
g.bind("skos", SKOS)
g.bind("dcterms", DCTERMS)

g.add((
  rdflib.URIRef("http://www.opengis.net/def/register/"),
  SKOS.member,
  rdflib.URIRef(collectionURI)
))

# Generation of Collection

g.add((
  rdflib.URIRef(collectionURI),
  SKOS.inScheme,
  rdflib.URIRef(schemeURI)
))
g.add((
  rdflib.URIRef(collectionURI),
  RDF.type,
  rdflib.URIRef(SKOS.Collection)
))
g.add((
  rdflib.URIRef(collectionURI),
  SKOS.prefLabel,
  rdflib.Literal(collectionAndSchemeLabel)
))
g.add((
  rdflib.URIRef(collectionURI),
  RDFS.label,
  rdflib.Literal(collectionAndSchemeLabel)
))

# Generation of ConceptScheme

g.add((
  rdflib.URIRef(schemeURI),
  SKOS.prefLabel,
  rdflib.Literal(collectionAndSchemeLabel)
))
g.add((
  rdflib.URIRef(schemeURI),
  RDF.type,
  rdflib.URIRef(SKOS.ConceptScheme)
))
g.add((
  rdflib.URIRef(schemeURI),
  RDFS.label,
  rdflib.Literal(collectionAndSchemeLabel)
))

g.add((
  rdflib.URIRef(schemeURI),
  rdflib.URIRef("http://www.opengis.net/def/metamodel/ogc-na/collectionView"),
  rdflib.URIRef(collectionURI)
))


# Generation of Concept




for root, dirs, files in os.walk('dggrs'):
    for file in files:
        if str(file).endswith(".json") :

            with open("./dggrs/OGC/1.0/"+file) as f:
                d = json.load(f)
                print(d['uri'])

                conceptURI = d['uri']
                g.add((
                    rdflib.URIRef(conceptURI),
                    RDF.type,
                    rdflib.URIRef(SKOS.Concept)
                ))
                g.add((
                    rdflib.URIRef(conceptURI),
                    RDFS.label,
                    rdflib.Literal(d['title'])
                ))
                g.add((
                    rdflib.URIRef(conceptURI),
                    SKOS.prefLabel,
                    rdflib.Literal(d['title'])
                ))
                g.add((
                    rdflib.URIRef(conceptURI),
                    SKOS.definition,
                    rdflib.Literal(d['description'])
                ))
                g.add((
                    rdflib.URIRef(conceptURI),
                    RDFS.seeAlso,
                    rdflib.URIRef(github_raw_folder+str(file))
                ))
                g.add((
                    rdflib.URIRef(conceptURI),
                    DCTERMS.created,
                    rdflib.Literal(datetime.now(), datatype=XSD.dateTime)
                ))
                g.add((
                    rdflib.URIRef(collectionURI),
                    SKOS.member,
                    rdflib.URIRef(conceptURI)
                ))

                g.add((
                rdflib.URIRef(conceptURI),
                SKOS.inScheme,
                rdflib.URIRef(schemeURI)
                ))



fout = open(ttlOutputFileName,'w')
fout.write(g.serialize(format="turtle"))
fout.close()

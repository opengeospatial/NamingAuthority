# Script created to support the generation of Turtle-encoded content for the OGC GeoTIFF Tag Register
# Created: 2021-02-16
# Author: Gobe Hobona (OGC)

import csv
import rdflib
from datetime import datetime
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD


csvFileName = "interpolation.csv"
ttlOutputFileName = "interpolation.ttl"
conceptNamespace = "http://www.opengis.net/def/interpolation/OGC/1"
schemeURI = "http://www.opengis.net/def/interpolation/OGC/1"
collectionAndSchemeLabel = "Interpolation Method Register"
collectionAndSchemeDefinition = "This is a register of Interpolation Methods used by OGC Standards. "

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

with open(csvFileName, 'r') as csvfile:
  tagreader = csv.reader(csvfile, delimiter=',')
  for row in tagreader:
      conceptURI = conceptNamespace+"/"+row[0]
      g.add((
          rdflib.URIRef(conceptURI),
          RDF.type,
          rdflib.URIRef(SKOS.Concept)
      ))
      g.add((
          rdflib.URIRef(conceptURI),
          RDFS.label,
          rdflib.Literal(row[2])
      ))
      g.add((
          rdflib.URIRef(conceptURI),
          SKOS.prefLabel,
          rdflib.Literal(row[2])
      ))
      g.add((
          rdflib.URIRef(conceptURI),
          SKOS.definition,
          rdflib.Literal(row[3])
      ))
      g.add((
          rdflib.URIRef(conceptURI),
          RDFS.seeAlso,
          rdflib.URIRef(row[4])
      ))
      g.add((
          rdflib.URIRef(conceptURI),
          DCTERMS.created,
          rdflib.Literal(datetime.now(), datatype=XSD.dateTime)
      ))
      g.add((
      rdflib.URIRef(conceptURI),
      SKOS.inScheme,
      rdflib.URIRef(schemeURI)
      ))

      g.add((
          rdflib.URIRef(collectionURI),
          SKOS.member,
          rdflib.URIRef(conceptURI)
      ))



fout = open(ttlOutputFileName,'w')
fout.write(g.serialize(format="nt"))
fout.close()

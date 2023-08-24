# Script created to support the generation of Turtle-encoded content for the OGC Tile Matrix Set Register
# Created: 2021-02-16
# Modified: 2022-09-26
# Author: Gobe Hobona (OGC)

import csv
import rdflib
from datetime import datetime
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD


csvFileName = "/Users/ogckm/Documents/GitHub/NamingAuthority/incubation/20220926_tile_matrix_set_register/tms.csv"
ttlOutputFileName = "/Users/ogckm/Documents/GitHub/NamingAuthority/incubation/20220926_tile_matrix_set_register/tms.ttl"
conceptNamespace = "http://www.opengis.net/def/tilematrixset/OGC/1.0"
schemeURI = "http://www.opengis.net/def/tms"
collectionAndSchemeLabel = "OGC Tile Matrix Set Register"
collectionAndSchemeDefinition = "This is a register of tile matrix sets used by OGC Standards. "

# Do not edit below this line
collectionURI = schemeURI+"/"

g = rdflib.Graph()
g.bind("foaf", FOAF)
g.bind("xsd", XSD)
g.bind("skos", SKOS)
g.bind("dcterms", DCTERMS)
g.bind("policy","http://www.opengis.net/def/metamodel/ogc-na/")

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
g.add((
  rdflib.URIRef(collectionURI),
  SKOS.definition,
  rdflib.Literal(collectionAndSchemeDefinition)
))
g.add((
  rdflib.URIRef(collectionURI),
  rdflib.URIRef("http://www.opengis.net/def/metamodel/ogc-na/status"),
  rdflib.URIRef("http://www.opengis.net/def/status/valid")
))

# Generation of ConceptScheme

g.add((
  rdflib.URIRef(schemeURI),
  SKOS.prefLabel,
  rdflib.Literal(collectionAndSchemeLabel)
))
g.add((
  rdflib.URIRef(schemeURI),
  SKOS.definition,
  rdflib.Literal(collectionAndSchemeDefinition)
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
g.add((
  rdflib.URIRef(schemeURI),
  rdflib.URIRef("http://www.opengis.net/def/metamodel/ogc-na/status"),
  rdflib.URIRef("http://www.opengis.net/def/status/valid")
))

# Generation of Concept

with open(csvFileName, 'r') as csvfile:
  tagreader = csv.reader(csvfile, delimiter=',')
  for row in tagreader:
      conceptURI = row[0]
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
          rdflib.Literal(row[1])
      ))
      g.add((
          rdflib.URIRef(conceptURI),
          RDFS.seeAlso,
          rdflib.URIRef("https://raw.githubusercontent.com/opengeospatial/2D-Tile-Matrix-Set/master/registry/json/"+row[2]+".json")
      ))
      g.add((
          rdflib.URIRef(conceptURI),
          RDFS.seeAlso,
          rdflib.URIRef("https://raw.githubusercontent.com/opengeospatial/2D-Tile-Matrix-Set/master/registry/xml/"+row[2]+".xml")
      ))
      g.add((
      rdflib.URIRef(conceptURI),
      rdflib.URIRef("http://www.opengis.net/def/metamodel/ogc-na/status"),
      rdflib.URIRef("http://www.opengis.net/def/status/valid")
      ))
      g.add((
          rdflib.URIRef(conceptURI),
          DCTERMS.created,
          rdflib.Literal(row[3]+"T13:00:00Z", datatype=XSD.dateTime)
      ))
      g.add((
          rdflib.URIRef(conceptURI),
          DCTERMS.modified,
          rdflib.Literal(datetime.now(), datatype=XSD.dateTime)
      ))
      g.add((
          rdflib.URIRef(collectionURI),
          SKOS.member,
          rdflib.URIRef(conceptURI)
      ))


fout = open(ttlOutputFileName,'w')
fout.write(g.serialize(format="turtle"))
fout.close()

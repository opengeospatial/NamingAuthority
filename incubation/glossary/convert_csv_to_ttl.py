import csv
import rdflib
from datetime import datetime
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD


csvFileName = "20231013_location_academy_terms.csv"
ttlOutputFileName = "20231013_location_academy_terms.ttl"

# Do not edit below this line

# Generation of Concept


g = rdflib.Graph()
g.bind("foaf", FOAF)
g.bind("xsd", XSD)
g.bind("skos", SKOS)
g.bind("dcterms", DCTERMS)

with open(csvFileName, 'r') as csvfile:
  tagreader = csv.reader(csvfile, delimiter=',')
  next(tagreader)
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
          rdflib.Literal(row[1])
      ))
      g.add((
          rdflib.URIRef(conceptURI),
          SKOS.prefLabel,
          rdflib.Literal(row[1])
      ))

      if not(str(row[2]) == 'NONE'):
        g.add((rdflib.URIRef(conceptURI),SKOS.altLabel,rdflib.Literal(row[2])))      

      g.add((
          rdflib.URIRef(conceptURI),
          RDFS.seeAlso,
          rdflib.URIRef(row[3])
      ))      
      g.add((
          rdflib.URIRef(conceptURI),
          SKOS.definition,
          rdflib.Literal(row[4])
      ))

      g.add((
          rdflib.URIRef(conceptURI),
          DCTERMS.created,
          rdflib.Literal(datetime.now(), datatype=XSD.dateTime)
      ))
      g.add((
          rdflib.URIRef(conceptURI),
          SKOS.inScheme,
          rdflib.URIRef("http://www.opengis.net/def/glossary")
      ))


fout = open(ttlOutputFileName,'w')
fout.write(g.serialize(format="turtle"))
fout.close()

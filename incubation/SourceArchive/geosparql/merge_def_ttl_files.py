import os, re
import rdflib
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD


'''
% find "$PWD" -type f -maxdepth 1 | grep ttl
/Users/ogckm/Downloads/ogc-geosparql-master/1.1/validator.ttl
/Users/ogckm/Downloads/ogc-geosparql-master/1.1/reqs.ttl
/Users/ogckm/Downloads/ogc-geosparql-master/1.1/sf_geometries.ttl
/Users/ogckm/Downloads/ogc-geosparql-master/1.1/geo.ttl
/Users/ogckm/Downloads/ogc-geosparql-master/1.1/funcsrules.ttl
/Users/ogckm/Downloads/ogc-geosparql-master/1.1/profile.ttl
/Users/ogckm/Downloads/ogc-geosparql-master/1.1/sa_functions.ttl
'''

folderpath = "/Users/ogckm/Downloads/ogc-geosparql-master/1.1"

g = rdflib.Graph()

filenames = [
"validator.ttl",
"reqs.ttl",
"sf_geometries.ttl",
"geo.ttl",
"funcsrules.ttl",
"profile.ttl",
"sa_functions.ttl"
]


for filename in filenames:
    print(folderpath+"/"+filename)
    g.parse(folderpath+"/"+filename)
    print(len(g))

g.serialize(destination="/Users/ogckm/Downloads/geosparqlfiles.ttl",format="ttl")


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


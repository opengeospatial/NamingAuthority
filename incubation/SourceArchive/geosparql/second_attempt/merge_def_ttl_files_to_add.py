import os, re
import rdflib
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD


path = "/Users/ogckm/Documents/GitHub/NamingAuthority/incubation/geosparql/second_attempt/triples_to_add"

g = rdflib.Graph()

for dirpath, subdirs, files in os.walk(path):
    for name in files:
        if name.endswith(".ttl"):
            print(os.path.join(dirpath, name))
            g.parse(os.path.join(dirpath, name))


g.serialize(destination="/Users/ogckm/Documents/GitHub/NamingAuthority/incubation/geosparql/20231206_insert_geosparqlfiles.nt",format="nt")

'''

The code below is not used because it is incomplete.

g1 = rdflib.Graph()
g1.parse("file:///Users/ogckm/Documents/GitHub/NamingAuthority/incubation/geosparql/20231206_insert_geosparqlfiles.nt")


knows_query = """
SELECT DISTINCT ?subject {
 ?subject ?predicate ?object
 FILTER (isURI(?subject) && STRSTARTS(str(?subject), str('http://www.opengis.net/def/') ) )
}"""

all_def_uris = []

qres = g1.query(knows_query)
for row in qres:
    all_def_uris.append(f"{row.subject}")


fout2 = open('/Users/ogckm/Documents/GitHub/NamingAuthority/incubation/geosparql/20231206_insert_geosparqlfiles_step2_not_uploaded.nt','w')


for subject in all_def_uris:
    is_concept = False
    triple_to_check = "<"+subject+"> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2004/02/skos/core#Concept>."
    qres = g1.query("ASK {"+triple_to_check+"}")
    for row in qres:
        if str(row) == 'False':
            print(subject + " NOT Concept" + str(row))
        else:
            is_concept = True

    if is_concept == False:
        triple_to_check = "<"+subject+"> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2004/02/skos/core#ConceptScheme>."
        qres = g1.query("ASK {"+triple_to_check+"}")
        for row in qres:
            if str(row) == 'False':
                if is_concept is False:
                    print(subject + " NOT ConceptScheme" + str(row))
                    fout2.write(triple_to_check+"\n")

fout2.close()
'''

'''
legacy instructions - no longer necessary

FIRST START FUSEKI

/Users/ogckm/Tools/apache-jena-fuseki-4.5.0/fuseki-server --file "/Users/ogckm/Downloads/20231206_insert_geosparqlfiles.nt" /geosparql

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


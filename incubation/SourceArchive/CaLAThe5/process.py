import rdflib
from rdflib import Graph, Literal, RDF, URIRef

# first we read the v4 version

g = rdflib.Graph()
g.parse("/Users/gobehobona/Documents/GitHub/NamingAuthority/definitions/conceptschemes/CaLAThe.ttl")

query = """
SELECT * {
 ?s ?p ?o
 FILTER (isURI(?s) && STRSTARTS(str(?s), str('https://www.opengis.net/def/CaLAThe/4.0') ) )
}"""

v4_identifiers = []

qres = g.query(query)
for row in qres:
    if not(str(row.s) in v4_identifiers):
        v4_identifiers.append(str(row.s))
        #print(f"{row.s} prefLabel {row.o}")

# Now we read the v5 version

h = rdflib.Graph()
h.parse("/Users/gobehobona/Documents/GitHub/NamingAuthority/incubation/CaLAThe5/CaLAThe5.rdf")
h.parse("/Users/gobehobona/Documents/GitHub/NamingAuthority/incubation/CaLAThe5/CaLATheCodeList2.rdf")


# Now we compare v4 concepts to v5 concepts to determine which are being deprecated and which are also being superseded

v5_identifiers = []

v5_concept_query = """
SELECT * {
 ?s ?p ?o
 FILTER (isURI(?s) && STRSTARTS(str(?s), str('https://www.opengis.net/def/CaLAThe/5.0') ) )
}"""

v5_concept_qres = h.query(v5_concept_query)
for v5_concept_row in v5_concept_qres:
    if not(str(v5_concept_row.s) in v5_identifiers):
        v5_identifiers.append(str(v5_concept_row.s))
        #print(f"{v5_concept_row.s} prefLabel {v5_concept_row.o}")

v5_codelist_query = """
SELECT * {
 ?s ?p ?o
 FILTER (isURI(?s) && STRSTARTS(str(?s), str('https://www.opengis.net/def/CaLATheCodeList/2.0') ) )
}"""

v5_codelist_qres = h.query(v5_codelist_query)
for v5_codelist_row in v5_codelist_qres:
    if not(str(v5_codelist_row.s) in v5_identifiers):
        v5_identifiers.append(str(v5_codelist_row.s))
        #print(f"{v5_codelist_row.s} prefLabel {v5_codelist_row.o}")


# Then we declare the v4 concepts deprecated and/or superseded. Note that a concept can be deprecated without being superseded

for v4_item in v4_identifiers:
    v4_item_uri = URIRef(v4_item)
    status_uri = URIRef("http://www.opengis.net/def/metamodel/ogc-na/status")
    deprecated_uri = URIRef("http://www.opengis.net/def/status/deprecated")
    if(v4_item.replace("4.0","5.0") in v5_identifiers):
        v5_item_uri = URIRef(v4_item.replace("4.0","5.0"))
        superseded_uri = URIRef("http://www.opengis.net/def/status/superseded")
        isReplacedBy_uri = URIRef("http://purl.org/dc/terms/isReplacedBy")
        replaces_uri = URIRef("http://purl.org/dc/terms/replaces")
        #print("<"+v4_item+"> <http://www.opengis.net/def/metamodel/ogc-na/status> <http://www.opengis.net/def/status/superseded>.\n")
        h.add((v4_item_uri,status_uri,superseded_uri))
        #print("<"+v4_item+"> <http://purl.org/dc/terms/isReplacedBy> <"+v4_item.replace("4.0","5.0")+">.\n")
        h.add((v4_item_uri,isReplacedBy_uri,v5_item_uri))
        #print("<"+v4_item+"> <http://www.opengis.net/def/metamodel/ogc-na/status> <http://www.opengis.net/def/status/deprecated>.\n")
        h.add((v4_item_uri,status_uri,deprecated_uri))
        #print("<"+v4_item.replace("4.0","5.0")+"> <http://purl.org/dc/terms/replaces> <"+v4_item+">.\n")
        h.add((v5_item_uri,replaces_uri,v4_item_uri))
    else:
        #print("<"+v4_item+"> <http://www.opengis.net/def/metamodel/ogc-na/status> <http://www.opengis.net/def/status/deprecated>.\n")
        h.add((v4_item_uri,status_uri,deprecated_uri))



# we now write out v5 to TTL

h.serialize(destination="20220802_CaLAThe5.ttl")

#=================================================

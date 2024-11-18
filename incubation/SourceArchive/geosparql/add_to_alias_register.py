import os, re
import rdflib

outputfile = "/Users/gobehobona/Documents/GitHub/NamingAuthority/incubation/geosparql/20231208_insert_to_alias_register.nt"

g = rdflib.Graph()

filenames = [
"20231206_insert_geosparqlfiles.nt",
"20231206_insert_status_400_fixes.nt",
"20231208_insert_manual_fix.nt"
]


for filepath in filenames:
    print(filepath)
    g.parse(filepath)
    print(len(g))


knows_query = """
SELECT DISTINCT ?subject {
 ?subject ?predicate ?object
 FILTER (isURI(?subject) && STRSTARTS(str(?subject), str('http://www.opengis.net/def/') ) )
}"""

all_def_uris = []

qres = g.query(knows_query)
for row in qres:
    all_def_uris.append(f"{row.subject}")



fout = open('20231208_geosparql_alias_register.nt','w')
for ct in all_def_uris:
        fout.write("\n")
        print(ct)
        ctx = ct.replace("http://","https://")
        fout.write("<https://example.org> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2004/02/skos/core#Concept> .\n".replace("http://example.org",ct).replace("https://example.org",ctx))
        fout.write("<https://example.org> <http://www.w3.org/2000/01/rdf-schema#label> \"Alias of http://example.org\"@en .\n".replace("http://example.org",ct).replace("https://example.org",ctx))
        fout.write("<https://example.org> <http://purl.org/dc/terms/created> \"2023-12-08\"^^<http://www.w3.org/2001/XMLSchema#date> .\n".replace("http://example.org",ct).replace("https://example.org",ctx))
        fout.write("<https://example.org> <http://purl.org/dc/terms/modified> \"2023-12-08\"^^<http://www.w3.org/2001/XMLSchema#date> .\n".replace("http://example.org",ct).replace("https://example.org",ctx))
        fout.write("<https://example.org> <http://www.w3.org/2004/02/skos/core#definition> \"This is an alias of the concept referenced by the sameAs predicate.\"@en .\n".replace("http://example.org",ct).replace("https://example.org",ctx))
        fout.write("<https://example.org> <http://www.w3.org/2002/07/owl#sameAs> <http://example.org> .\n".replace("http://example.org",ct).replace("http://example.org",ct).replace("https://example.org",ctx))
        fout.write("<https://example.org> <http://www.w3.org/2004/02/skos/core#inScheme> <https://www.opengis.net/def/alias-register> .\n".replace("http://example.org",ct).replace("https://example.org",ctx))
        fout.write("<https://example.org> <http://www.w3.org/2004/02/skos/core#prefLabel> \"Alias of http://example.org\"@en .\n".replace("http://example.org",ct).replace("https://example.org",ctx))
        fout.write("<https://example.org> <http://www.opengis.net/def/metamodel/ogc-na/status> <http://www.opengis.net/def/status/experimental> .\n".replace("http://example.org",ct).replace("https://example.org",ctx))

fout.close()



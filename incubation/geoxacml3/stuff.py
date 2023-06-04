fout = open("geoxacml3_insert.ttl",'w')

fout.write("<https://www.opengis.net/def/geoxacml-identifier-register> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2004/02/skos/core#ConceptScheme>.\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register> <http://www.w3.org/2000/01/rdf-schema#label> \"GeoXACML Identifier Register\" .\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register> <http://www.opengis.net/def/metamodel/ogc-na/status> <http://www.opengis.net/def/status/experimental>.\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register>  <http://www.opengis.net/def/metamodel/ogc-na/collectionView> <https://www.opengis.net/def/geoxacml-identifier-register/>.\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register>  <http://purl.org/dc/terms/created> \"2023-04-20\"^^<http://www.w3.org/2001/XMLSchema#date>.\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register>  <http://purl.org/dc/terms/modified> \"2023-06-04\"^^<http://www.w3.org/2001/XMLSchema#date>.\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register>   <http://www.w3.org/2004/02/skos/core#prefLabel> \"GeoXACML Identifier Register\"@en .\n")


fout.write("<https://www.opengis.net/def/geoxacml-identifier-register/> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2004/02/skos/core#Collection>.\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register/> <http://www.w3.org/2000/01/rdf-schema#label> \"GeoXACML Identifier Register\" .\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register/> <http://www.w3.org/2004/02/skos/core#inScheme> <https://www.opengis.net/def/geoxacml-identifier-register> .\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register/>  <http://purl.org/dc/terms/created> \"2023-04-20\"^^<http://www.w3.org/2001/XMLSchema#date>.\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register/>  <http://purl.org/dc/terms/modified> \"2023-06-04\"^^<http://www.w3.org/2001/XMLSchema#date>.\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register/> <http://www.opengis.net/def/metamodel/ogc-na/status> <http://www.opengis.net/def/status/experimental>.\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register/>   <http://www.w3.org/2004/02/skos/core#prefLabel> \"GeoXACML Identifier Register\"@en .\n")


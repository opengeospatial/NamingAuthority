import csv

fout = open("geoxacml3.ttl",'w')


fout.write("<https://www.opengis.net/def/geoxacml-identifier-register> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2004/02/skos/core#ConceptScheme>.\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register> <http://www.w3.org/2000/01/rdf-schema#label> \"GeoXACML Identifier Register\" .\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register> <http://www.opengis.net/def/metamodel/ogc-na/status> <http://www.opengis.net/def/status/valid>.\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register>  <http://www.opengis.net/def/metamodel/ogc-na/collectionView> <https://www.opengis.net/def/geoxacml-identifier-register/>.\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register>  <http://purl.org/dc/terms/created> \"2023-04-20\"^^<http://www.w3.org/2001/XMLSchema#date>.\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register>  <http://purl.org/dc/terms/modified> \"2023-06-04\"^^<http://www.w3.org/2001/XMLSchema#date>.\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register>   <http://www.w3.org/2004/02/skos/core#prefLabel> \"GeoXACML Identifier Register\"@en .\n")


fout.write("<https://www.opengis.net/def/geoxacml-identifier-register/> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2004/02/skos/core#Collection>.\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register/> <http://www.w3.org/2000/01/rdf-schema#label> \"GeoXACML Identifier Register\" .\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register/> <http://www.w3.org/2004/02/skos/core#inScheme> <https://www.opengis.net/def/geoxacml-identifier-register> .\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register/>  <http://purl.org/dc/terms/created> \"2023-04-20\"^^<http://www.w3.org/2001/XMLSchema#date>.\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register/>  <http://purl.org/dc/terms/modified> \"2023-06-04\"^^<http://www.w3.org/2001/XMLSchema#date>.\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register/> <http://www.opengis.net/def/metamodel/ogc-na/status> <http://www.opengis.net/def/status/valid>.\n")
fout.write("<https://www.opengis.net/def/geoxacml-identifier-register/>   <http://www.w3.org/2004/02/skos/core#prefLabel> \"GeoXACML Identifier Register\"@en .\n")



with open('geoxacml3.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['the_label'], row['the_urn'])
        the_label = row['the_label']
        urn_string = row['the_urn']
        fout.write("<"+urn_string+"> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2004/02/skos/core#Concept> .\n")
        fout.write("<"+urn_string+"> <http://www.w3.org/2004/02/skos/core#prefLabel> \""+the_label+"\"@en .\n")
        fout.write("<"+urn_string+"> <http://www.w3.org/2004/02/skos/core#definition> \"The "+the_label+" identifier from the GeoXACML 3.0 Standard.\"@en .\n")
        fout.write("<"+urn_string+"> <http://purl.org/dc/terms/created> \"2023-05-25\"^^<http://www.w3.org/2001/XMLSchema#date> .\n")
        fout.write("<"+urn_string+"> <http://purl.org/dc/terms/modified> \"2023-05-26\"^^<http://www.w3.org/2001/XMLSchema#date> .\n")
        fout.write("<"+urn_string+"> <http://www.w3.org/2004/02/skos/core#inScheme> <https://www.opengis.net/def/geoxacml-identifier-register> .\n")
        fout.write("<"+urn_string+"> <http://www.opengis.net/def/metamodel/ogc-na/status> <http://www.opengis.net/def/status/valid> .\n")            
        fout.write("<"+urn_string+"> <http://www.w3.org/2000/01/rdf-schema#label> \""+the_label+"\"@en .\n")
        fout.write("<https://www.opengis.net/def/geoxacml-identifier-register/> <http://www.w3.org/2004/02/skos/core#member> <"+urn_string+">.\n") 


fout.write("<http://www.opengis.net/def/register/> <http://www.w3.org/2004/02/skos/core#member> <https://www.opengis.net/def/geoxacml-identifier-register/>.\n")


fout.close()
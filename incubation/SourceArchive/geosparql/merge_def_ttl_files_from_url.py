import os, re
import rdflib

'''
% cd /Users/gobehobona/Downloads/ogc-geosparql-gh-pages/
% find "$PWD" -type f -maxdepth 1 | grep ttl

'''


outputfile = "/Users/gobehobona/Documents/GitHub/NamingAuthority/incubation/geosparql/geosparqlfiles.ttl"

g = rdflib.Graph()

filenames = [

"/Users/gobehobona/Downloads/ogc-geosparql-gh-pages/geosparql11/servicedescription_conformanceclasses.ttl",
"/Users/gobehobona/Downloads/ogc-geosparql-gh-pages/geosparql11/servicedescription_all_functions.ttl",
"/Users/gobehobona/Downloads/ogc-geosparql-gh-pages/geosparql11/reqs.ttl",
"/Users/gobehobona/Downloads/ogc-geosparql-gh-pages/geosparql11/sf_geometries.ttl",
"/Users/gobehobona/Downloads/ogc-geosparql-gh-pages/geosparql11/servicedescription_extensions.ttl",
"/Users/gobehobona/Downloads/ogc-geosparql-gh-pages/geosparql11/geo.ttl",
"/Users/gobehobona/Downloads/ogc-geosparql-gh-pages/geosparql11/funcsrules.ttl",
"/Users/gobehobona/Downloads/ogc-geosparql-gh-pages/geosparql11/profile.ttl",
"/Users/gobehobona/Downloads/ogc-geosparql-gh-pages/geosparql10/servicedescription_conformanceclasses.ttl",
"/Users/gobehobona/Downloads/ogc-geosparql-gh-pages/geosparql10/servicedescription_all_functions.ttl",
"/Users/gobehobona/Downloads/ogc-geosparql-gh-pages/geosparql10/sf_geometries.ttl",
"/Users/gobehobona/Downloads/ogc-geosparql-gh-pages/geosparql10/servicedescription_extensions.ttl",
"/Users/gobehobona/Downloads/ogc-geosparql-gh-pages/geosparql10/geo.ttl",
"/Users/gobehobona/Downloads/ogc-geosparql-gh-pages/geosparql10/funcsrules.ttl",
"/Users/gobehobona/Downloads/ogc-geosparql-gh-pages/geosparql10/profile.ttl"


]


for filepath in filenames:
    print(filepath)
    g.parse(filepath)
    print(len(g))

g.serialize(destination=outputfile,format="ttl")


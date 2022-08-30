# from __future__ import print_function
import json
import requests
import sys
import urllib.request
from typing import List, Any
import argparse
import httpx
import rdflib
import os.path
from rdflib import Graph
from rdflib.namespace import DC, DCTERMS, SKOS, OWL, RDF, RDFS, XSD, DCAT
from pyld import jsonld
# load the document register as JSON via a JSON-LD conversion

DOCSURL = "https://docs.google.com/spreadsheets/d/"
# SAMPLE_RANGE_NAME = 'Class Data!A1:D'


def init_graph() -> Graph:
    g = rdflib.Graph()
    g.bind("xsd", XSD)
    g.bind("dct", DCTERMS)
    g.bind("skos", SKOS)
    g.bind("owl", OWL)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    g.bind("dcat", DCAT)
    g.bind("iso", 'http://iso.org/tc211/')
    g.bind("spec", "http://www.opengis.net/def/ont/modspec/")
    g.bind("specrel", "http://www.opengis.net/def/ont/specrel/")
    g.bind("na", "http://www.opengis.net/def/metamodel/ogc-na/")
    g.bind("prov", "http://www.w3.org/ns/prov#")
    return g

DOCCONTEXT = '''
  "@context": [ "http://defs-dev.opengis.net/ogc-na/definitions/profiles/resources/dcterms.jsonld" ,
               
               "http://defs-dev.opengis.net/ogc-na/definitions/profiles/resources/skos.jsonld" ,
               {
                 "@vocab": "http://example.org/vocab#",
                 "type": "http://www.opengis.net/def/metamodel/ogc-na/doctype",
                 "alternative": "skos:altLabel",
                 "title": "skos:definition",
                 "description": "rdfs:comment",
                 "date": "dct:created",
                 "URL": "rdfs:seeAlso"
                 }
                 ]'''

CONTEXT = '''[ "http://defs-dev.opengis.net/ogc-na/definitions/profiles/resources/dcterms.jsonld" ,

               "http://defs-dev.opengis.net/ogc-na/definitions/profiles/resources/skos.jsonld" ,
               { "skos": "http://www.w3.org/2004/02/skos/core#",
                 "@vocab": "http://example.org/vocab#",
                 "type": "http://www.opengis.net/def/metamodel/ogc-na/doctype",
                 "alternative": "skos:altLabel",
                 "title": "skos:definition",
                 "description": "rdfs:comment",
                 "date": "dct:created",
                 "URL": "rdfs:seeAlso"
                 }
                 ]'''

def add_context(data, context):
    return {
        '@context': context,
        '@graph': data
    }

def main():

    g = init_graph()
#    with open("../incubation/bibliography/test.jsonld") as j:
#        g.parse(source=j, format="json-ld")

    jsonld.set_document_loader(jsonld.requests_document_loader(timeout=5000))
    with open("../incubation/bibliography/test.jsonld") as j:

        jdoc = json.load(j)
        jdocld = add_context(jdoc, json.loads(CONTEXT))
        g.parse(data=json.dumps(jsonld.expand(jdocld)), format='json-ld')


    formatted_ttl: str = str(g.serialize(format="turtle"))
    # print(formatted_ttl)
    # with open(outputDir + "/" + spec_id + "_" + spreadsheetId + ".ttl", 'w') as fout_ttl:
    with open("docs.ttl", 'w') as fout_ttl:
        fout_ttl.write(formatted_ttl + "    ")
        fout_ttl.close()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        help="source file (instead of service)",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output directory",
    )


    args = parser.parse_args()
    outputDir = None

    main()

# from __future__ import print_function
import sys
import urllib.request
from typing import List, Any
import argparse
import httpx
import rdflib
import os.path
from rdflib import Graph
from rdflib.namespace import DC, DCTERMS, SKOS, OWL, RDF, RDFS, XSD, DCAT

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


def main():

    g = init_graph()
    with open("../incubation/bibliography/test.jsonld") as j:
        g.parse(source=j, format="json-ld")

    # load_matrix(query, gs_range, gs_sheet_name):)
    for s, p, o in g:
        print(p)
        print(g.value(s, p))
        print((s, p, None) in g)

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

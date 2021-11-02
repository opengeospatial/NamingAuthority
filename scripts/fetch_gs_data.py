# from __future__ import print_function
import sys
import urllib.request
from typing import List, Any
import argparse
import httpx
import rdflib
from rdflib.namespace import DC, DCTERMS, SKOS, OWL, RDF, RDFS, XSD, DCAT


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# var SPREADSHEET_ID = sys.argv[1]
# var DIR_PATH = sys.argv[2]
# SPREADSHEET_ID = '1ydKaFTibayXy7nbJwpMJTyyc78NE75J-axDClDRGg_c'
GS_URL = "https://docs.google.com/spreadsheets/d/"
# SAMPLE_RANGE_NAME = 'Class Data!A1:D'


def parse_spec_data():
    query = "select C, D, F where F is not null"
    gs_range = "C5:F"
    gs_sheet_name = "Specification"

    matrix = load_matrix(query, gs_range, gs_sheet_name)

    spec_uri = matrix[0][2].replace('"', '')
    spec_uri_tokens = spec_uri.split("/")
    spec_id = spec_uri_tokens[len(spec_uri_tokens) - 1]
    g = init_graph()
    spec = rdflib.URIRef(spec_uri)

    for r in matrix[1:]:
        pred = rdflib.URIRef(r[1].replace('"', ''))
        obj = None
        obj = r[0].replace('"', '')
        if obj == "rdfs:Literal":
            g.add((spec, pred, rdflib.Literal(r[2].replace('"', ''), datatype=RDFS.Literal)))
        elif r[0] == "xsd:date":
            g.add((spec, pred, rdflib.Literal(r[2].replace('"', ''), datatype=XSD.date)))
        else:
            g.add((spec, pred, rdflib.URIRef(r[2].replace('"', ''))))
    return spec_id, g


def parse_conf_classes(g):
    query = "select D, B, C where D is not null"
    gs_range = "B2:D"
    gs_sheet_name = "Conformance Classes"

    matrix = load_matrix(query, gs_range, gs_sheet_name)

    for r in matrix:
        conf_class = rdflib.URIRef(trim_citation(r[0]))
        g.add((conf_class, RDF.type, rdflib.URIRef("http://www.opengis.net/def/ont/modspec/ConformanceClass")))
        if trim_citation(r[1]) != "":
            g.add((conf_class, SKOS.prefLabel, rdflib.Literal(trim_citation(r[1]))))
        if trim_citation(r[2]) != "":
            g.add((conf_class, SKOS.definition, rdflib.Literal(trim_citation(r[2]))))

    return g


def parse_conf_relations(g):
    query = "select D, E, F where D is not null and E is not null and F is not null"
    gs_range = "D2:F"
    gs_sheet_name = "ConfClasses relations"

    matrix = load_matrix(query, gs_range, gs_sheet_name)

    for r in matrix:
        g.add((rdflib.URIRef(trim_citation(r[0])),
               rdflib.URIRef(trim_citation(r[1])),
               rdflib.URIRef(trim_citation(r[2]))
               ))

    return g


def trim_citation(s):
    return s.strip('"')


def init_graph():
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


def csv2array(csv):
    m: list[list[Any]] = []
    rows = csv.split('\n')
    for row in rows:
        cells = row.split(",")
        m.append(cells)
    return m


def load_matrix(query, gs_range, gs_sheet_name):
    response = httpx.get(GS_URL + spreadsheetId +
                         "/gviz/tq?tqx=out:csv&sheet=" + gs_sheet_name +
                         "&range=" + gs_range +
                         "&tq=" + query)
    print(response.url)
    csv = response.text
    # print(csv)
    return csv2array(csv)


def main():
    spec_id, g = parse_spec_data()
    g = parse_conf_classes(g)
    g = parse_conf_relations(g)

    formatted_ttl: str = str(g.serialize(format="turtle"), "utf-8")
    print(formatted_ttl)
    with open(outputDir + "/" + spec_id + "_" + spreadsheetId + ".ttl", 'w') as fout_ttl:
        fout_ttl.write(formatted_ttl)
        fout_ttl.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--id",
        help="Spreadsheet ID",
    )

    parser.add_argument(
        "-u",
        "--url",
        help="Spreadsheet URL",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output directory",
    )
    args = parser.parse_args()
    spreadsheetId = None
    outputDir = None
    if args.url:
        # s = args.url.strip('https://docs.google.com/spreadsheets/d/')
        ss = args.url.split('/')
        spreadsheetId = ss[len(ss) - 2]
    if args.id:
        spreadsheetId = args.id
    if args.output:
        outputDir = args.output

    main()

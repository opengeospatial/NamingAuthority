# from __future__ import print_function
import sys
import urllib.request
from typing import List, Any
import argparse
import httpx
import rdflib
import os.path
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
    base_uri = matrix[1][2].replace('"', '')
    spec_uri_tokens = spec_uri.split("/")
    spec_id = spec_uri_tokens[len(spec_uri_tokens) - 1]
    g = init_graph()
    spec = rdflib.URIRef(spec_uri)
    g.add((spec, RDF.type, rdflib.URIRef("http://www.opengis.net/def/ont/modspec/Specification")))
    g.add((spec, rdflib.URIRef("http://www.opengis.net/def/ont/specrel/modspec"), rdflib.URIRef(base_uri)))
    published = accepted = submitted = base_url = None

    for r in matrix[2:]:
        pred_uri = r[1].replace('"', '')
        pred = rdflib.URIRef(pred_uri)
        obj = None
        obj = r[0].replace('"', '')
        if obj == "rdfs:Literal":
            g.add((spec, pred, rdflib.Literal(r[2].replace('"', '')))) #, datatype=RDFS.Literal)))
        elif obj == "xsd:date":
            g.add((spec, pred, rdflib.Literal(r[2].replace('"', ''), datatype=XSD.date)))
        else:
            g.add((spec, pred, rdflib.URIRef(r[2].replace('"', ''))))

        if pred_uri == 'http://purl.org/dc/terms/created':
            base_url = r[2].replace('"', '')
        if pred_uri == 'http://purl.org/dc/terms/dateSubmitted':
            submitted = r[2].replace('"', '')
        if pred_uri == 'http://purl.org/dc/terms/dateAccepted':
            accepted = r[2].replace('"', '')
        if pred_uri == 'http://www.opengis.net/def/ont/modspec/date':
            published = r[2].replace('"', '')

        if published is not None:
            modified = published
        elif accepted is not None:
            modified = accepted
        elif submitted is not None:
            modified = submitted
        else:
            modified = None

        if submitted is not None:
            created = submitted
        else:
            created = None

    return spec_id, g, base_uri, created, modified


def parse_conf_classes(g):
    query = "select E, B, C, D where E is not null"
    gs_range = "B2:E"
    gs_sheet_name = "Conformance Classes"

    matrix = load_matrix(query, gs_range, gs_sheet_name)
    conf_classes = []


    for r in matrix:
        if r is not None and len(r) > 3:
            conf_class = rdflib.URIRef(trim_citation(r[0]))
            conf_classes.append(trim_citation(r[0]))
            g.add((conf_class, RDF.type, rdflib.URIRef("http://www.opengis.net/def/ont/modspec/ConformanceClass")))
            if trim_citation(r[1]) != "":
                g.add((conf_class, SKOS.prefLabel, rdflib.Literal(trim_citation(r[1]))))
            if trim_citation(r[2]) != "":
                g.add((conf_class, SKOS.definition, rdflib.Literal(trim_citation(r[2]))))
            if trim_citation(r[3]) != "":
                g.add((conf_class, DCAT.landingPage, rdflib.Literal(trim_citation(r[3]))))
    return g, conf_classes


def parse_conf_relations(g, conf_classes):
    query = "select D, E, F where D is not null and E is not null and F is not null"
    gs_range = "D2:F"
    gs_sheet_name = "ConfClasses relations"

    matrix = load_matrix(query, gs_range, gs_sheet_name)

    for r in matrix:
        if r is not None and len(r) > 3:
            g.add((rdflib.URIRef(trim_citation(r[0])),
                   rdflib.URIRef(trim_citation(r[1])),
                   rdflib.URIRef(trim_citation(r[2]))
                   ))
            if trim_citation(r[1]) == 'http://purl.org/dc/terms/hasPart':
                conf_classes.remove(trim_citation(r[2]))
            if trim_citation(r[1]) == 'http://www.opengis.net/def/ont/specrel/dependency':
                try:
                    base_url1 = r[0].split("/conf/")[0]
                    base_url2 = r[2].split("/conf/")[0]
                    if base_url1 == base_url2 and conf_classes.__contains__(trim_citation(r[0])):
                        conf_classes.remove(trim_citation(r[0]))
                except Exception:
                    print("cannot remove class with dependencies from the root level: " + r[0])

    return g, conf_classes


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
    print("reading: " + str(response.url))
    csv = response.text
    print("raw data: " + str(csv))
    return csv2array(csv)


def load_predicates_for_deduplication():
    query = "select B where D is not null and E is not null and F is not null"
    gs_range = "D2:F"
    gs_sheet_name = "ConfClasses relations"

'''
<http://www.opengis.net/spec/docs/16-107r2-anno> a owl:Ontology .

<http://www.opengis.net/spec/landinfra/part7/1.0> a skos:ConceptScheme ;
  dct:source <http://www.opengis.net/def/docs/16-107r2> ;
  skos:prefLabel "Specification elements for OGC 16-107r2 LandInfra" ;
  skos:definition "A convenience hierarchy for navigating the elements of a specification using the SKOS model" ;
  dct:modified "2017-06-02"^^xsd:date ;
  dct:created "2017-03-24"^^xsd:date ;
  skos:hasTopConcept <http://www.opengis.net/spec/landinfra/part7/1.0/conf/landdivision> ,
    <http://www.opengis.net/spec/landinfra/part7/1.0/conf/condominium> ;
.
'''

def add_schema(g, spec_id, base_url, date_created, date_modified, top_conf_classes):
    g.add((rdflib.URIRef('http://www.opengis.net/spec/docs/' + spec_id + '-anno'), RDF.type, OWL.Ontology))
    scheme = rdflib.URIRef(base_url)
    spec = rdflib.URIRef('http://www.opengis.net/def/docs/' + spec_id)
    g.add((scheme, RDF.type, SKOS.ConceptScheme))
    g.add((scheme, DCTERMS.source, spec))
    g.add((scheme, SKOS.prefLabel, rdflib.Literal("Specification elements for " + spec_id)))
    g.add((scheme, SKOS.definition, rdflib.Literal("A convenience hierarchy for navigating the elements of a specification using the SKOS model")))

    if date_modified is not None:
        g.add((scheme, DCTERMS.modified, rdflib.Literal(date_modified, datatype=XSD.date)))
    if date_created is not None:
        g.add((scheme, DCTERMS.created, rdflib.Literal(date_created, datatype=XSD.date)))
    if top_conf_classes is not None:
        for cc in top_conf_classes:
            g.add((spec, rdflib.URIRef("http://www.opengis.net/def/ont/modspec/class"), rdflib.URIRef(cc)))

def main(replace):
    spec_id, g, base_url, created, modified = parse_spec_data()
    g, conf_classes = parse_conf_classes(g)
    g, relations = parse_conf_relations(g, conf_classes)
    add_schema(g, spec_id, base_url, created, modified, conf_classes)

    # print("Spreadsheet Graph: " + str(g.serialize(format="turtle")))

    if not replace:
        stored_spec_file = inputDir + "/" + spec_id + ".ttl"

        g2 = rdflib.Graph()
        if os.path.exists(stored_spec_file):
            g2.parse(stored_spec_file, format='ttl')


        # load_matrix(query, gs_range, gs_sheet_name):)
        for s, p, o in g2:
            print(p)
            print(g.value(s, p))
            print((s, p, None) in g)
            if not (s, p, None) in g:
                g.add((s, p, o))
        # print("Merged Graph: " + str(g.serialize(format="turtle")))

    formatted_ttl: str = str(g.serialize(format="turtle"))
    # print(formatted_ttl)
    # with open(outputDir + "/" + spec_id + "_" + spreadsheetId + ".ttl", 'w') as fout_ttl:
    with open(outputDir + "/" + spec_id + ".ttl", 'w') as fout_ttl:
        fout_ttl.write(formatted_ttl + "    ")
        fout_ttl.close()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        help="specification rdf base directory",
    )

    parser.add_argument(
        "-d",
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

    parser.add_argument(
        "-r",
        "--replace",
        const=True, nargs='?',
        help="Replace old file instead of overwriting values/ontology objects"
    )

    args = parser.parse_args()
    spreadsheetId = None
    outputDir = None
    replace = False
    if args.url:
        # s = args.url.strip('https://docs.google.com/spreadsheets/d/')
        ss = args.url.split('/')
        spreadsheetId = ss[len(ss) - 2]
    if args.id:
        spreadsheetId = args.id
    if args.output:
        outputDir = args.output
    if args.input:
        inputDir = args.input
    if args.replace:
        replace = args.replace

    main(replace)

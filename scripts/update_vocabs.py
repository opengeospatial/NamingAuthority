import json
from typing import List
import argparse
from pathlib import Path
import httpx
from pyshacl import validate
from rdflib import Graph, URIRef
from rdflib.namespace import RDF, SKOS
import os

SKOS_RULES = [ 'scripts/skostopconcepts.shapes.ttl']

def add_vocabs(vocabs: List[Path], mappings: dict):
    for vocab in vocabs:
        r = httpx.post(
            #"http://"+os.environ["VOCAB_HOST"] + "/rdf4j-server/repositories/ogc-na" , 
            "http://defs-dev.opengis,net:8080/rdf4j-server/repositories/ogc-na",
            params={"graph": str(mappings[vocab.name])},
            headers={"Content-Type": "text/turtle"},
            content=open(vocab, "rb").read(),
            auth=(os.environ["DB_USERNAME"], os.environ["DB_PASSWORD"])
        )
        assert 200 <= r.status_code <= 300, "Status code was {}".format(r.status_code)
        # add_to_vocab_index(vocab, get_graph_uri_for_vocab(vocab))


def remove_vocabs(vocabs: List[Path], mappings: dict):
    for vocab in vocabs:
        r = httpx.post(
            "http://defs-dev.opengis,net:8080/rdf4j-server/repositories/ogc-na",
            data={"update": "DROP GRAPH <{}>".format(mappings[vocab.name])},
            auth=(os.environ["DB_USERNAME"], os.environ["DB_PASSWORD"])
        )
        assert 200 <= r.status_code <= 300, "Status code was {}".format(r.status_code)
        # remove_from_vocab_index(vocab)


def get_graph_uri_for_vocab(vocab: Path) -> URIRef:
    """We can get the Graph URI for a vocab from the vocab file as we know that all VocPub-conformant vocabs
    have one and only one ConceptScheme per file and that the ICSM VocPrez installation uses the ConceptScheme URI
    as the Graph URI"""
    g = Graph().parse(str(vocab), format="ttl")
    for s in g.subjects(predicate=RDF.type, object=SKOS.ConceptScheme):
        return s


def get_all_vocabs_uris(vocabs: List[Path]) -> dict:
    mappings = {}
    for vocab in vocabs:
        mappings[vocab.name] = get_graph_uri_for_vocab(vocab)

    return mappings


# def add_to_vocab_index(file_path: Path, graph_uri: URIRef):
#     i = Path(__file__).parent.parent / "vocabularies" / "index.json"
#     with open(i, "r") as f:
#         mappings = json.load(f)
#     with open(i, "w") as f:
#         mappings[str(file_path)] = str(graph_uri)
#         f.write(json.dumps(mappings))
#
#
# def remove_from_vocab_index(file_path: Path):
#     i = Path(__file__).parent.parent / "vocabularies" / "index.json"
#     with open(i, "r") as f:
#         mappings = json.load(f)
#     del mappings[str(file_path)]
#     with open(i, "w") as f:
#         f.write(json.dumps(mappings))


def make_rdf(f,g=None):
    if not g:
        g = Graph().parse(str(f), format="ttl")
    #g.serialize(destination=f.replace(".ttl",".rdf"), format="xml")
    g.serialize(destination=f.replace(".ttl", "_entailed.ttl"), format="ttl")


def log(param):
   print ( param)


def perform_skos_entailments(f, g=None):
    """ run skos graph entailments """
    if not g:
        g = Graph().parse(str(f), format="ttl")
    for rules in SKOS_RULES:
        shg = Graph().parse(rules, format="ttl")
        validate(g, shacl_graph=shg, advanced=True, inplace=True )
    return g


if __name__ == "__main__":
    # for testing (until exit()):
    # add_vocabs([Path(__file__).parent.parent / "vocabularies" / "valid.ttl"], {"valid.ttl": URIRef("http://test.com")})
    # add_vocabs([Path(__file__).parent.parent / "vocabularies" / "valid.ttl"], {"valid.ttl": URIRef("http://test.com")})
    # remove_vocabs([Path(__file__).parent.parent / "vocabularies" / "valid.ttl"], {"valid.ttl": URIRef("http://test.com")})
    # exit()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--modified",
        help="Vocabs to be updated in the DB",
    )

    parser.add_argument(
        "-a",
        "--added",
        help="Vocabs to be added to the DB",
    )

    parser.add_argument(
        "-r",
        "--removed",
        help="Vocabs to be removed from the DB",
    )

    args = parser.parse_args()

    modified = []
    if args.modified:
        for f in args.modified.split(","):
            # if the file is in the definitions/conceptschemes/ folder and ends with .ttl, it's a vocab file
            if f.startswith("definitions/conceptschemes/") and f.endswith(".ttl"):
                modified.append(Path(f))
                try:
                    newg = perform_skos_entailments(f)
                    make_rdf(f,newg)
                except Exception as e:
                    log ("Failed to generate {} : ( {}  )".format(f,e))

    added = []
    if args.added:
        for f in args.added.split(","):
            # if the file is in the vocabularies/ folder and ends with .ttl, it's a vocab file
            if f.startswith("definitions/conceptschemes/") and f.endswith(".ttl"):
                p = Path(f)
                added.append(p)

    removed = []
    if args.removed:
        for f in args.removed.split(","):
            # if the file is in the vocabularies/ folder and ends with .ttl, it's a vocab file
            if f.startswith("definitions/conceptschemes/") and f.endswith(".ttl"):
                p = Path(f)
                removed.append(p)

    #i = Path(__file__).parent.parent / "vocabularies" / "index.json"
    #with open(i, "r") as f:
    #    mappings = json.load(f)
    # remove all removed and modified vocabs
    #remove_vocabs(removed + modified, mappings)

    # add all added and modified vocabs
    #add_vocabs(added + modified, mappings)

    # print for testing
    print("modified:")
    print([str(x) for x in modified])
    print("added:")
    print([str(x) for x in added])
    print("removed:")
    print([str(x) for x in removed])

    # rebuild VocPrez' cache
    #r = httpx.get("http://defs-dev.opengis.net/vocprez/cache-reload")
    #assert r.status_code == 200


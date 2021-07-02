import json
from glob import glob
from typing import List
import argparse
from pathlib import Path
import httpx
from pyshacl import validate
from rdflib import Graph, URIRef
from rdflib.namespace import RDF, SKOS
import os

SKOS_RULES = [ 'scripts/skosbasics.shapes.ttl', 'scripts/skos_vocprez.shapes.ttl' ]
COMMON_VALIDATORS = [ "https://w3id.org/profile/vocpub/validator" ]
OWL_RULES = [ 'scripts/owl2skos.shapes.ttl' ] + SKOS_RULES



def get_validation_graph( vlist ):
    for v in vlist:
        r = httpx.get(v)
        assert r.status_code == 200
        return Graph().parse(data=r.text, format="turtle")

SKOS_VALIDATOR = get_validation_graph ( COMMON_VALIDATORS  )
DOMAINS = [ ( "definitions/conceptschemes", SKOS_RULES , SKOS_VALIDATOR ) ]

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


def get_graph_uri_for_vocab(vocab: Path, g: Graph = None) -> URIRef:
    """We can get the Graph URI for a vocab from the vocab file as we know that all VocPub-conformant vocabs
    have one and only one ConceptScheme per file and that the ICSM VocPrez installation uses the ConceptScheme URI
    as the Graph URI"""
    if not g:
        g = Graph().parse(str(vocab), format="ttl")
    for s in g.subjects(predicate=RDF.type, object=SKOS.ConceptScheme):
        yield str(s)


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


def get_entailedpath(f, g:Graph , fmt, rootpattern='/def/'):
    path,filename = os.path.split(f)
    filename = os.path.splitext(filename)[0]
    canonical_filename = None
    for graphuri in get_graph_uri_for_vocab(f,g=g):
        if canonical_filename:
            print ('Warning - file {} contains multiple concept schemes'.format(f))
        canonical_filename = graphuri.rsplit(rootpattern)[1]
        conceptscheme = graphuri
    if not canonical_filename:
        print('Warning - file {} contains no concept schemes'.format(f))
        return None,filename,None,None
    cpaths = os.path.split(canonical_filename)
    return ( os.path.join( path,'entailed',*cpaths) + "." + fmt , filename, canonical_filename , conceptscheme)

FMTS = { 'ttl':'ttl' , 'rdf':'xml'  }

def make_rdf(f,g=None):
    if not g:
        g = Graph().parse(str(f), format="ttl")
    #g.serialize(destination=f.replace(".ttl",".rdf"), format="xml")
    for fmt in FMTS.keys() :
        newpath, filename, canonical_filename, conceptschemeuri = get_entailedpath(f, g, fmt)
        if newpath:
            try:
                Path(Path(newpath).parent).mkdir(parents=True, exist_ok=True)
            except FileExistsError:
                pass
            g.serialize(destination=newpath, format=FMTS[fmt])
    if filename != canonical_filename:
        print("New file name {} -> {} for {}".format(filename, canonical_filename, conceptschemeuri))



def log(param):
   print ( param)


def perform_entailments(rulegraphlist, f, g=None):
    """ run skos graph entailments """
    if not g:
        g = Graph().parse(str(f), format="ttl")
    for rules in rulegraphlist:
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

    parser.add_argument(
        "-i",
        "--initialise",
        help="Initialise Database",
    )

    parser.add_argument(
        "-u",
        "--update",
        help="Update Database",
    )

    parser.add_argument(
        "-b",
        "--batch",
        action='store_true',
        help="Batch entail all vocabs ( use -f to force overwrite of existing entailments )",
    )

    parser.add_argument(
        "-f",
        "--force",
        action='store_true',
        help="force overwrite of existing entailments",
    )

    args = parser.parse_args()
    modlist = []
    addedlist = []
    if args.modified:
        modlist = args.modified.split(",")
    if args.added:
        addedlist = args.added.split(",")

    for scopepath,rules,validator in DOMAINS:
        modified = []
        if args.batch:
            # update modified list to be everything missing, or everything if -f
            if args.force :
                modified = glob(scopepath+"/*.ttl")
            else:
                modified = list ( set(glob(scopepath+"/*.ttl")) - set(glob(scopepath+ "/entailed/*.ttl")))


        for f in modlist:
            # if the file is in the definitions/conceptschemes/ folder and ends with .ttl, it's a vocab file
            if f.startswith(scopepath) and f.endswith(".ttl"):
                modified.append(Path(f))

        added = []
        for f in addedlist:
            # if the file is in the vocabularies/ folder and ends with .ttl, it's a vocab file
            if f.startswith(scopepath) and f.endswith(".ttl"):
                p = Path(f)
                added.append(p)

        for f in modified + added:
            try:
                newg = perform_entailments(rules,f)
                v = validate(data_graph=newg, shacl_graph=validator)
                if not v[0]:
                    with open( str(f).replace('.ttl','.txt') , "w" ) as vr:
                        vr.write(v[2])
                make_rdf(f, newg)
            except Exception as e:
                log("Failed to generate {} : ( {}  )".format(f, e))

        removed = []
        if args.removed:
            for f in args.removed.split(","):
                # if the file is in the vocabularies/ folder and ends with .ttl, it's a vocab file
                if f.startswith(scopepath) and f.endswith(".ttl"):
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
        print ( "Scope : ")
        print("modified:")
        print([str(x) for x in modified])
        print("added:")
        print([str(x) for x in added])
        print("removed:")
        print([str(x) for x in removed])

    # rebuild VocPrez' cache
    #r = httpx.get("http://defs-dev.opengis.net/vocprez/cache-reload")
    #assert r.status_code == 200


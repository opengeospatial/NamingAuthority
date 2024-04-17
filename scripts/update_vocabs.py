from __future__ import annotations

import json
from glob import glob
import re
from typing import List
import argparse
from pathlib import Path
from urllib.parse import urlparse

import httpx
from pyshacl import validate
from rdflib import Graph, URIRef
from rdflib.namespace import RDF, SKOS
import os


def get_closure_graph( vlist: List[str] ):
    g = Graph()
    for v in vlist:
        if v.startswith("http:") or v.startswith("https:"):
            r = httpx.get(v)
            assert r.status_code == 200
            data = r.text
            g += Graph().parse(data=data, format="turtle")
        else:
            g += Graph().parse(source=v, format="turtle")

    return g

SKOS_RULES = [ 'scripts/skosbasics.shapes.ttl', 'scripts/skos-sameas.shapes.ttl', 'scripts/ogc_skos_profile_entailments.ttl', 'scripts/skos_vocprez.shapes.ttl' ]
#COMMON_VALIDATORS = [ "https://w3id.org/profile/vocpub/validator" ]
COMMON_VALIDATORS = [ 'scripts/vocprez.shapes.ttl' ]
#OWL_RULES = [ 'scripts/owl2skos.shapes.ttl' , 'scripts/skos2ftc.shapes.ttl'] + SKOS_RULES
OWL_RULES = [ 'scripts/owl2skos.shapes.ttl' , 'scripts/owl2feature.shapes.ttl'] + SKOS_RULES
#OWL_RULES = [ 'scripts/owl2skos.shapes.ttl' ] + SKOS_RULES

SPEC_RULES = [ 'scripts/spec_as_conceptscheme.shapes.ttl'  ] + SKOS_RULES
PROFILE_RULES = [ 'scripts/prof_as_skos.shapes.ttl'  ] + SKOS_RULES
DOC_RULES =  [ 'scripts/docs_entailments.shapes.ttl'  ] + SKOS_RULES

# , 'scripts/modspec_entailmenthelpers.ttl'
#SPEC_VALIDATORS = [ 'definitions/models/modspec_shacl.ttl']
SPEC_VALIDATORS = [ 'definitions/models/modspec-owl2sh-semi-closed.ttl']
#DOCREG_CLOSURE = [ "definitions/conceptschemes/docs.ttl" ]
SPECMODEL_CLOSURE = [ 'definitions/models/modspec_validations.ttl', 'definitions/conceptschemes/status.ttl' ]
PROFMODEL_CLOSURE = [ 'definitions/conceptschemes/profiles.ttl' , 'definitions/models/prof.ttl'  ]
APPSCHEMA_CLOSURE = [ 'definitions/models/featuretypes.ttl' ]
# 'definitions/models/modspec.ttl',

# SPECMODEL_CLOSURE = [ 'scripts/modspecs_entailmenthelpers.ttl']

SKOS_VALIDATOR = get_closure_graph ( COMMON_VALIDATORS  )
SPEC_VALIDATOR =  get_closure_graph ( SPEC_VALIDATORS  ) + SKOS_VALIDATOR
#DOCREGISTER_GRAPH = get_closure_graph( DOCREG_CLOSURE )
TEST_VALIDATOR = get_closure_graph([ 'scripts/test/test_validator.ttl'])

DOMAIN_CFG = {}

DOMAIN_CFG['definitions/conceptschemes'] =  { 'description': "Set of terms registered with OGC NA not covered by specialised domains" ,
    'glob': '/*.ttl', 'rulelist': SKOS_RULES, 'validator': SKOS_VALIDATOR,
    'extraont': None,
    'uri_root_filter': '/def/'}

DOMAIN_CFG[ 'specification-elements/defs'] =  {
  'description': 'Specification Elements defined according the OGC modular specification and relevant policies' ,
  'glob': '/*.ttl',
  'rulelist': SPEC_RULES,
  'validator': SPEC_VALIDATOR,
  'extraont': ['definitions/models/modspec_validations.ttl',
   'definitions/conceptschemes/status.ttl','definitions/models/doc_relations_model.ttl'],
    'annotations': ['definitions/models/modspec.ttl' , 'definitions/models/policy.ttl' , 'definitions/models/doc_relations_model.ttl'],
  'uri_root_filter': '/spec/'}

DOMAIN_CFG[ 'definitions/docs'] =  {
  'description': 'Document Register' ,
  'glob': '/docs.ttl',
  'rulelist': DOC_RULES,
  'validator': SKOS_VALIDATOR,
  'extraont': ['definitions/conceptschemes/doc-type.ttl'],
  'annotations': [
      'definitions/docs/annotations/docs_upper_collections.ttl',
      'definitions/docs/docs-working-groups.ttl',
  ],
  'uri_root_filter': '/def/'}

DOMAIN_CFG[ 'incubation/binary-array-ld'] =  {
  'glob': '/*.ttl',
  'rulelist': OWL_RULES,
  'validator': SKOS_VALIDATOR,
  'extraont': None,
  'uri_root_filter': '/def/'}

DOMAIN_CFG[ 'scripts/tests'] = {
  'glob': '/*.ttl',
  'rulelist': [],
  'validator': TEST_VALIDATOR,
  'extraont': ['scripts/test/test_closure.ttl'],
  'uri_root_filter': '/test/'}

DOMAIN_CFG[ 'definitions/schema/hy_features/hyf'] =  {
  'glob': '/hyf.ttl',
  'rulelist': OWL_RULES,
  'validator': SKOS_VALIDATOR,
  'extraont': APPSCHEMA_CLOSURE + [ 'definitions/schema/hy_features/hyf/hyf_anno.ttl'],
  'annotations':  APPSCHEMA_CLOSURE + [ 'definitions/schema/hy_features/hyf/hyf_anno.ttl'],
  'uri_root_filter': '/def/'}

DOMAIN_CFG[ '/repos/ogc/cybele-common-semantic-model/profiles/model'] =  [ {
  'glob': '/*_flat.ttl',
  'rulelist': OWL_RULES,
  'validator': SKOS_VALIDATOR,
  'extraont': None,
  'uri_root_filter': '/w3id.org/'},
{
  'glob': '/*_prof.ttl',
  'rulelist': PROFILE_RULES,
  'validator': SKOS_VALIDATOR,
  'extraont': PROFMODEL_CLOSURE,
  'uri_root_filter': '/w3id.org/'}
    ]
DOMAIN_CFG[ '/repos/rob-metalinkage/DEMETER/profiles'] = [ {
  'glob': '/*/*_flat.ttl',
  'rulelist': OWL_RULES,
  'validator': SKOS_VALIDATOR,
  'extraont': None,
  'uri_root_filter': '/w3id.org/'},
{
  'glob': '/*/*_prof.ttl',
  'rulelist': PROFILE_RULES,
  'validator': SKOS_VALIDATOR,
  'extraont': PROFMODEL_CLOSURE,
  'uri_root_filter': '/w3id.org/'}
    ]


DOMAIN_CFG['definitions/profiles'] = [ {
  'glob': '/*.ttl',
  'rulelist':  PROFILE_RULES,
  'validator':SKOS_VALIDATOR,
  'extraont': PROFMODEL_CLOSURE,
    'annotations': ['definitions/conceptschemes/profiles.ttl', 'definitions/models/prof.ttl'],
  'uri_root_filter': '/def/'},
{
  'glob': '/resources/*_owl.ttl',
  'rulelist':  OWL_RULES,
  'validator':SKOS_VALIDATOR,
  'extraont': None,
  'uri_root_filter': None}
]

DOMAIN_CFG['entities'] = {
  'glob': '/*.ttl',
  'rulelist': SKOS_RULES,
  'validator': SKOS_VALIDATOR,
  'extraont': None,
  'uri_root_filter': '/def/'
  }

DEFAULT_RDF_SERVICE = 'http://defs-dev.opengis.net:8080'

def load_vocab(vocab: Path, guri):
    authdetails = None
    try:
        authdetails = (os.environ["DB_USERNAME"], os.environ["DB_PASSWORD"])
        print('Using authentication with user', authdetails[0])
    except:
        print('Not using authentication')
        pass

    r = httpx.delete(
        RDF_SERVICE,
        params={
            'graph': guri
        },
        auth=authdetails
    )

    with open(vocab, "rb") as f:
        content = f.read()

    r = httpx.put(
        RDF_SERVICE,
        params={"graph":  guri },
        headers={"Content-Type": "text/turtle"},
        content=content,
        auth= authdetails
    )
    r.raise_for_status()
    return r.url



def remove_vocabs(vocabs: List[Path], mappings: dict):
    for vocab in vocabs:
        r = httpx.post(
            "http://defs-dev.opengis,net:8080/rdf4j-server/repositories/ogc-na",
            data={"update": "DROP GRAPH <{}>".format(mappings[vocab.name])},
            auth=(os.environ["DB_USERNAME"], os.environ["DB_PASSWORD"])
        )
        assert 200 <= r.status_code <= 300, "Status code was {}".format(r.status_code)
        # remove_from_vocab_index(vocab)


def get_graph_uri_for_vocab(vocab: Path | None, g: Graph = None) -> URIRef:
    """We can get the Graph URI for a vocab using assumption that the ConceptScheme is declared in the graph being processed."""
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
    if not rootpattern :
        # just assume filename is going to be fine
        return( os.path.join(path, 'entailed', filename) + "." + fmt , filename, filename , get_graph_uri_for_vocab(f,g=g) )
    for graphuri in get_graph_uri_for_vocab(f,g=g):
        if canonical_filename:
            print ('Warning - file {} contains multiple concept schemes'.format(f))
        try:
            canonical_filename = graphuri.rsplit(rootpattern)[1]
            conceptscheme = graphuri
            cpaths = os.path.split(canonical_filename)
        except:
            print ('Ignoring concept scheme that does not match domain path {}  : {}'.format(rootpattern,graphuri))
    if not canonical_filename:
        print('Warning - file {} contains no concept schemes matching domain root URI {} - using input filename '.format(f, rootpattern))
        cpaths = ( filename, )
        conceptscheme = None
    return ( os.path.join( path,'entailed',*cpaths) + "." + fmt , filename, canonical_filename , conceptscheme)

FMTS = { 'ttl':'ttl' , 'rdf':'xml', 'jsonld':'json-ld'  }

def make_rdf(f,g=None,rootpath='/def/'):
    loadable_ttl = None
    if not g:
        g = Graph().parse(str(f), format="ttl")
    #g.serialize(destination=f.replace(".ttl",".rdf"), format="xml")
    for fmt in FMTS.keys() :
        newpath, filename, canonical_filename, conceptschemeuri = get_entailedpath(f, g, fmt, rootpattern=rootpath)
        if newpath:
            try:
                Path(Path(newpath).parent).mkdir(parents=True, exist_ok=True)
            except FileExistsError:
                pass
            g.serialize(destination=newpath, format=FMTS[fmt])
            if fmt == 'ttl':
                loadable_ttl = newpath

    if filename != canonical_filename:
        print("New file name {} -> {} for {}".format(filename, canonical_filename, conceptschemeuri))
    return loadable_ttl


def log(param):
   print ( param)


def perform_entailments(rulegraphlist, f, g=None, extra=None, anno=[]):
    """ run skos graph entailments
    @param anno:
    @param rulegraphlist: ordered list of entailment rules to apply in provided order
    @param f:
    @param g:
    @param extra:
    @param annotations:
    @return:
    """
    entailed_extra = extra
    if not g:
        g = Graph().parse(str(f), format="ttl")
    for rules in rulegraphlist:
        shg = Graph().parse(rules, format="ttl")
        if extra:
            entailed_extra = extra
            try:
                validate(entailed_extra, shacl_graph=shg, ont_graph=None,  advanced=True, inplace=True)
            except Exception as e:
                raise Exception("SHACL error entailing baseline for closure in {} : {}".format(rules,str(e)))
        try:
            validate(g, shacl_graph=shg, ont_graph=extra,  advanced=True, inplace=True )
        except Exception as e:
            raise Exception ( "SHACL error in {}: {}".format(rules, str(e)))
    if entailed_extra:
        cleaned = g-entailed_extra
        cleaned.namespace_manager = g.namespace_manager
        return cleaned
    else:
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
        "-d",
        "--domain",
        help="Batch process specific domain",
    )

    parser.add_argument(
        "-i",
        "--initialise",
        help="Initialise Database",
    )

    parser.add_argument(
        "-u",
        "--update",
        action='store_true',
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

    parser.add_argument(
        "-s",
        "--server" ,
        help=f"override server - default = {DEFAULT_RDF_SERVICE}",
    )

    parser.add_argument(
        "-t",
        "--triplerepo",
        default='ogc-na',
        help="Legacy option to override triplestore repo - default = ogc-na",
    )

    args = parser.parse_args()

    RDF_SERVICE = os.environ.get('RDF4JSERVER', DEFAULT_RDF_SERVICE)
    if args.server:
        RDF_SERVICE = args.server

    RDF_SERVICE_PARSED = urlparse(RDF_SERVICE)
    if re.match(r'^defs(-dev)?\.opengis\.net(:80(80)?)?$', RDF_SERVICE_PARSED.netloc) \
            and re.match(f'^/*$', RDF_SERVICE_PARSED.path):
        # Legacy server definition, built from scheme, netloc and args.triplerepo
        RDF_SERVICE = f"{RDF_SERVICE_PARSED.scheme}://{RDF_SERVICE_PARSED.netloc}" \
                      f"/rdf4j-server/repositories/{args.triplerepo}/rdf-graphs/service"

    if args.update:
        print("Using RDF Server for update:", RDF_SERVICE)
    modlist = []
    addedlist = []

    if args.modified:
        print("Modified: " + args.modified)
        modlist = args.modified.split(",")
    if args.added:
        addedlist = args.added.split(",")

    for scopepath in DOMAIN_CFG.keys():
        cfglist = DOMAIN_CFG[scopepath]
        if not isinstance( cfglist,list) :
            cfglist = [cfglist]
        for cfg in cfglist:
            try:
                annotations = cfg['annotations']
            except:
                annotations = []

            if args.domain and args.domain != scopepath:
                continue
            modified = []
            domainlist = [os.path.normpath(i) for i in glob(scopepath+cfg['glob'])]

            if args.batch:
                # update modified list to be everything missing, or everything if -f
                if args.force :
                    modified = domainlist
                else:
                    # fix - this will be broken for globbing pattern
                    modified = list ( set(domainlist) - set(glob(scopepath+ "/entailed" + cfg['glob'])))


            for f in modlist:
                # if the file matches the glob using the scopepath and glob pattern  it's a vocab file
                if f.startswith(scopepath) and f.endswith(".ttl") and os.path.normpath(f) in domainlist:
                    modified.append(Path(f))

            added = []
            for f in addedlist:
                if f.startswith(scopepath) and f.endswith(".ttl") and os.path.normpath(f) in domainlist:
                    p = Path(f)
                    added.append(p)
            extra_ont = None
            if modified + added and 'extraont' in cfg and cfg['extraont'] :
                extra_ont = get_closure_graph(cfg['extraont'])

            for f in modified + added:
                try:
                    newg = perform_entailments(cfg['rulelist'],f,extra=extra_ont, anno=annotations)
                    v = validate(data_graph=newg, ont_graph=extra_ont , inference='rdfs', shacl_graph=cfg['validator'])
                    if True or not v[0]:
                        with open( str(f).replace('.ttl','.txt') , "w" ) as vr:
                            vr.write(v[2])
                    loadable_path = make_rdf(f, g=newg, rootpath=cfg['uri_root_filter'])
                    if args.update:
                        loadlist = [loadable_path]
                        if annotations:
                            loadlist += annotations
                        try:
                            gname = list(get_graph_uri_for_vocab(None, newg))[0]
                        except:
                            gname = "x-urn:{}".format(str(f).replace('\\', ':'))
                        for n,loadable in enumerate(loadlist):
                            try:
                                # need to add annotations to a new context
                                loc = load_vocab( loadable, gname)
                                log("Uploaded {} for {} to   {} ".format(loadable, f, loc))
                            except  Exception as e:
                                log("Failed to upload {} for {} : ( {} )".format(loadable, f, e))
                            if n == 0 :
                                gname = gname+str(n+1)
                            else:
                                gname = gname[:-1] +str(n+1)
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
            print ( "Scope : {}".format(scopepath))
            if modified:
                print("modified:")
                print([str(x) for x in modified])
            if added:
                print("added:")
                print([str(x) for x in added])
            if removed:
                print("removed:")
                print([str(x) for x in removed])

    # rebuild VocPrez' cache
    #r = httpx.get("http://defs-dev.opengis.net/vocprez/cache-reload")
    #assert r.status_code == 200


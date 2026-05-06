from __future__ import annotations

import os
from glob import glob
from pathlib import Path
from typing import List

import httpx
from rdflib import Graph, URIRef
from rdflib.namespace import RDF, SKOS


def get_closure_graph(vlist: List[str]):
    g = Graph()
    for v in vlist:
        if v.startswith("http:") or v.startswith("https:"):
            r = httpx.get(v)
            assert r.status_code == 200
            g += Graph().parse(data=r.text, format="turtle")
        else:
            g += Graph().parse(source=v, format="turtle")
    return g


SKOS_RULES = [
    'scripts/skosbasics.shapes.ttl',
    'scripts/skos-sameas.shapes.ttl',
    'scripts/ogc_skos_profile_entailments.ttl',
    'scripts/skos_vocprez.shapes.ttl',
]
#COMMON_VALIDATORS = [ "https://w3id.org/profile/vocpub/validator" ]
COMMON_VALIDATORS = ['scripts/vocprez.shapes.ttl']
#OWL_RULES = [ 'scripts/owl2skos.shapes.ttl' , 'scripts/skos2ftc.shapes.ttl'] + SKOS_RULES
OWL_RULES = ['scripts/owl2skos.shapes.ttl', 'scripts/owl2feature.shapes.ttl'] + SKOS_RULES
#OWL_RULES = [ 'scripts/owl2skos.shapes.ttl' ] + SKOS_RULES

SPEC_RULES = ['scripts/spec_as_conceptscheme.shapes.ttl'] + SKOS_RULES
PROFILE_RULES = ['scripts/prof_as_skos.shapes.ttl'] + SKOS_RULES
DOC_RULES = ['scripts/docs_entailments.shapes.ttl'] + SKOS_RULES

# , 'scripts/modspec_entailmenthelpers.ttl'
#SPEC_VALIDATORS = [ 'definitions/models/modspec_shacl.ttl']
SPEC_VALIDATORS = ['definitions/models/modspec-owl2sh-semi-closed.ttl']
#DOCREG_CLOSURE = [ "definitions/conceptschemes/docs.ttl" ]
SPECMODEL_CLOSURE = ['definitions/models/modspec_validations.ttl', 'definitions/conceptschemes/status.ttl']
PROFMODEL_CLOSURE = ['definitions/conceptschemes/profiles.ttl', 'definitions/models/prof.ttl']
APPSCHEMA_CLOSURE = ['definitions/models/featuretypes.ttl']
# 'definitions/models/modspec.ttl',

# SPECMODEL_CLOSURE = [ 'scripts/modspecs_entailmenthelpers.ttl']

SKOS_VALIDATOR = get_closure_graph(COMMON_VALIDATORS)
SPEC_VALIDATOR = get_closure_graph(SPEC_VALIDATORS) + SKOS_VALIDATOR
#DOCREGISTER_GRAPH = get_closure_graph( DOCREG_CLOSURE )
TEST_VALIDATOR = get_closure_graph(['scripts/test/test_validator.ttl'])

DOMAIN_CFG = {}

DOMAIN_CFG['definitions/conceptschemes'] = {
    'description': "Set of terms registered with OGC NA not covered by specialised domains",
    'glob': '/*.ttl', 'rulelist': SKOS_RULES, 'validator': SKOS_VALIDATOR,
    'extraont': None,
    'uri_root_filter': '/def/',
}

DOMAIN_CFG['specification-elements/defs'] = {
    'description': 'Specification Elements defined according the OGC modular specification and relevant policies',
    'glob': '/*.ttl',
    'rulelist': SPEC_RULES,
    'validator': SPEC_VALIDATOR,
    'extraont': ['definitions/models/modspec_validations.ttl',
                 'definitions/conceptschemes/status.ttl', 'definitions/models/doc_relations_model.ttl'],
    'annotations': ['definitions/models/modspec.ttl', 'definitions/models/policy.ttl',
                    'definitions/models/doc_relations_model.ttl'],
    'uri_root_filter': '/spec/',
}

DOMAIN_CFG['definitions/docs'] = {
    'description': 'Document Register',
    'glob': '/docs.ttl',
    'rulelist': DOC_RULES,
    'validator': SKOS_VALIDATOR,
    'extraont': ['definitions/conceptschemes/doc-type.ttl'],
    'annotations': [
        'definitions/docs/annotations/docs_upper_collections.ttl',
        'definitions/docs/docs-working-groups.ttl',
    ],
    'uri_root_filter': '/def/',
}

DOMAIN_CFG['incubation/binary-array-ld'] = {
    'glob': '/*.ttl',
    'rulelist': OWL_RULES,
    'validator': SKOS_VALIDATOR,
    'extraont': None,
    'uri_root_filter': '/def/',
}

DOMAIN_CFG['scripts/tests'] = {
    'glob': '/*.ttl',
    'rulelist': [],
    'validator': TEST_VALIDATOR,
    'extraont': ['scripts/test/test_closure.ttl'],
    'uri_root_filter': '/test/',
}

DOMAIN_CFG['definitions/schema/hy_features/hyf'] = {
    'glob': '/hyf.ttl',
    'rulelist': OWL_RULES,
    'validator': SKOS_VALIDATOR,
    'extraont': APPSCHEMA_CLOSURE + ['definitions/schema/hy_features/hyf/hyf_anno.ttl'],
    'annotations': APPSCHEMA_CLOSURE + ['definitions/schema/hy_features/hyf/hyf_anno.ttl'],
    'uri_root_filter': '/def/',
}

DOMAIN_CFG['/repos/ogc/cybele-common-semantic-model/profiles/model'] = [
    {
        'glob': '/*_flat.ttl',
        'rulelist': OWL_RULES,
        'validator': SKOS_VALIDATOR,
        'extraont': None,
        'uri_root_filter': '/w3id.org/',
    },
    {
        'glob': '/*_prof.ttl',
        'rulelist': PROFILE_RULES,
        'validator': SKOS_VALIDATOR,
        'extraont': PROFMODEL_CLOSURE,
        'uri_root_filter': '/w3id.org/',
    },
]

DOMAIN_CFG['/repos/rob-metalinkage/DEMETER/profiles'] = [
    {
        'glob': '/*/*_flat.ttl',
        'rulelist': OWL_RULES,
        'validator': SKOS_VALIDATOR,
        'extraont': None,
        'uri_root_filter': '/w3id.org/',
    },
    {
        'glob': '/*/*_prof.ttl',
        'rulelist': PROFILE_RULES,
        'validator': SKOS_VALIDATOR,
        'extraont': PROFMODEL_CLOSURE,
        'uri_root_filter': '/w3id.org/',
    },
]

DOMAIN_CFG['definitions/profiles'] = [
    {
        'glob': '/*.ttl',
        'rulelist': PROFILE_RULES,
        'validator': SKOS_VALIDATOR,
        'extraont': PROFMODEL_CLOSURE,
        'annotations': ['definitions/conceptschemes/profiles.ttl', 'definitions/models/prof.ttl'],
        'uri_root_filter': '/def/',
    },
    {
        'glob': '/resources/*_owl.ttl',
        'rulelist': OWL_RULES,
        'validator': SKOS_VALIDATOR,
        'extraont': None,
        'uri_root_filter': None,
    },
]

DOMAIN_CFG['entities'] = {
    'glob': '/*.ttl',
    'rulelist': SKOS_RULES,
    'validator': SKOS_VALIDATOR,
    'extraont': None,
    'uri_root_filter': '/def/',
}

DOMAIN_CFG['incubation/geopose'] = {
    'glob': '/*.ttl',
    'rulelist': OWL_RULES,
    'validator': SKOS_VALIDATOR,
    'extraont': None,
    'uri_root_filter': '/ogc/geopose/',
}

FMTS = {'ttl': 'ttl', 'rdf': 'xml', 'jsonld': 'json-ld'}


def log(param):
    print(param)


def get_graph_uri_for_vocab(vocab: Path | None, g: Graph = None) -> URIRef:
    if not g:
        g = Graph().parse(str(vocab), format="ttl")
    for s in g.subjects(predicate=RDF.type, object=SKOS.ConceptScheme):
        yield str(s)


def get_entailedpath(f, g: Graph, fmt, rootpattern='/def/'):
    path, filename = os.path.split(f)
    filename = os.path.splitext(filename)[0]
    canonical_filename = None
    if not rootpattern:
        return (os.path.join(path, 'entailed', filename) + "." + fmt,
                filename, filename, get_graph_uri_for_vocab(f, g=g))
    for graphuri in get_graph_uri_for_vocab(f, g=g):
        if canonical_filename:
            print('Warning - file {} contains multiple concept schemes'.format(f))
        try:
            canonical_filename = graphuri.rsplit(rootpattern)[1]
            conceptscheme = graphuri
            cpaths = os.path.split(canonical_filename)
        except Exception:
            print('Ignoring concept scheme that does not match domain path {}  : {}'.format(rootpattern, graphuri))
    if not canonical_filename:
        print('Warning - file {} contains no concept schemes matching domain root URI {} - using input filename'.format(
            f, rootpattern))
        cpaths = (filename,)
        conceptscheme = None
    return (os.path.join(path, 'entailed', *cpaths) + "." + fmt,
            filename, canonical_filename, conceptscheme)


def make_rdf(f, g=None, rootpath='/def/'):
    loadable_ttl = None
    if not g:
        g = Graph().parse(str(f), format="ttl")
    for fmt in FMTS.keys():
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


def load_vocab(vocab: Path, guri, rdf_service: str):
    authdetails = None
    try:
        authdetails = (os.environ["DB_USERNAME"], os.environ["DB_PASSWORD"])
        print('Using authentication with user', authdetails[0])
    except Exception:
        print('Not using authentication')

    httpx.delete(rdf_service, params={'graph': guri}, auth=authdetails)

    with open(vocab, "rb") as f:
        content = f.read()

    r = httpx.put(
        rdf_service,
        params={"graph": guri},
        headers={"Content-Type": "text/turtle"},
        content=content,
        auth=authdetails,
    )
    r.raise_for_status()
    return r.url


def get_all_vocabs_uris(vocabs) -> dict:
    mappings = {}
    for vocab in vocabs:
        mappings[vocab.name] = get_graph_uri_for_vocab(vocab)
    return mappings


def find_domain_cfg(filepath: str):
    """Return (scopepath, cfg) for the first DOMAIN_CFG entry matching filepath."""
    normalized = os.path.normpath(filepath)
    for scopepath, cfglist in DOMAIN_CFG.items():
        if not isinstance(cfglist, list):
            cfglist = [cfglist]
        for cfg in cfglist:
            domainlist = [os.path.normpath(i) for i in glob(scopepath + cfg['glob'])]
            if normalized in domainlist:
                return scopepath, cfg
    return None, None
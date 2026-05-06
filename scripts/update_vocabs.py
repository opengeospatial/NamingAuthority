from __future__ import annotations

import re
from typing import List
import argparse
from pathlib import Path
from urllib.parse import urlparse
from glob import glob

import httpx
from pyshacl import validate
from rdflib import Graph
import os

from vocab_utils import (
    DOMAIN_CFG, FMTS,
    get_closure_graph, get_graph_uri_for_vocab, get_entailedpath,
    make_rdf, load_vocab, log,
)

DEFAULT_RDF_SERVICE = 'http://defs-dev.opengis.net:8080'


def remove_vocabs(vocabs: List[Path], mappings: dict):
    for vocab in vocabs:
        r = httpx.post(
            "http://defs-dev.opengis,net:8080/rdf4j-server/repositories/ogc-na",
            data={"update": "DROP GRAPH <{}>".format(mappings[vocab.name])},
            auth=(os.environ["DB_USERNAME"], os.environ["DB_PASSWORD"])
        )
        assert 200 <= r.status_code <= 300, "Status code was {}".format(r.status_code)


def perform_entailments(rulegraphlist, f, g=None, extra=None, anno=[]):
    entailed_extra = extra
    if not g:
        g = Graph().parse(str(f), format="ttl")
    for rules in rulegraphlist:
        shg = Graph().parse(rules, format="ttl")
        if extra:
            entailed_extra = extra
            try:
                validate(entailed_extra, shacl_graph=shg, ont_graph=None, advanced=True, inplace=True)
            except Exception as e:
                raise Exception("SHACL error entailing baseline for closure in {} : {}".format(rules, str(e)))
        try:
            validate(g, shacl_graph=shg, ont_graph=extra, advanced=True, inplace=True)
        except Exception as e:
            raise Exception("SHACL error in {}: {}".format(rules, str(e)))
    if entailed_extra:
        cleaned = g - entailed_extra
        cleaned.namespace_manager = g.namespace_manager
        return cleaned
    else:
        return g


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--modified", help="Vocabs to be updated in the DB")
    parser.add_argument("-a", "--added", help="Vocabs to be added to the DB")
    parser.add_argument("-r", "--removed", help="Vocabs to be removed from the DB")
    parser.add_argument("-d", "--domain", help="Batch process specific domain")
    parser.add_argument("-i", "--initialise", help="Initialise Database")
    parser.add_argument("-u", "--update", action='store_true', help="Update Database")
    parser.add_argument("-b", "--batch", action='store_true',
                        help="Batch entail all vocabs ( use -f to force overwrite of existing entailments )")
    parser.add_argument("-f", "--force", action='store_true',
                        help="force overwrite of existing entailments")
    parser.add_argument("-s", "--server",
                        help=f"override server - default = {DEFAULT_RDF_SERVICE}")
    parser.add_argument("-t", "--triplerepo", default='ogc-na',
                        help="Legacy option to override triplestore repo - default = ogc-na")

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
        if not isinstance(cfglist, list):
            cfglist = [cfglist]
        for cfg in cfglist:
            try:
                annotations = cfg['annotations']
            except Exception:
                annotations = []

            if args.domain and args.domain != scopepath:
                continue
            modified = []
            domainlist = [os.path.normpath(i) for i in glob(scopepath + cfg['glob'])]

            if args.batch:
                # update modified list to be everything missing, or everything if -f
                if args.force:
                    modified = domainlist
                else:
                    # fix - this will be broken for globbing pattern
                    modified = list(set(domainlist) - set(glob(scopepath + "/entailed" + cfg['glob'])))

            for f in modlist:
                # if the file matches the glob using the scopepath and glob pattern  it's a vocab file
                if f.startswith(scopepath) and f.endswith(".ttl") and os.path.normpath(f) in domainlist:
                    modified.append(Path(f))

            added = []
            for f in addedlist:
                if f.startswith(scopepath) and f.endswith(".ttl") and os.path.normpath(f) in domainlist:
                    added.append(Path(f))

            extra_ont = None
            if modified + added and 'extraont' in cfg and cfg['extraont']:
                extra_ont = get_closure_graph(cfg['extraont'])

            for f in modified + added:
                try:
                    newg = perform_entailments(cfg['rulelist'], f, extra=extra_ont, anno=annotations)
                    v = validate(data_graph=newg, ont_graph=extra_ont, inference='rdfs', shacl_graph=cfg['validator'])
                    if True or not v[0]:
                        with open(str(f).replace('.ttl', '.txt'), "w") as vr:
                            vr.write(v[2])
                    loadable_path = make_rdf(f, g=newg, rootpath=cfg['uri_root_filter'])
                    if args.update:
                        loadlist = [loadable_path]
                        if annotations:
                            loadlist += annotations
                        try:
                            gname = list(get_graph_uri_for_vocab(None, newg))[0]
                        except Exception:
                            gname = "x-urn:{}".format(str(f).replace('\\', ':'))
                        for n, loadable in enumerate(loadlist):
                            try:
                                # need to add annotations to a new context
                                loc = load_vocab(loadable, gname, RDF_SERVICE)
                                log("Uploaded {} for {} to   {} ".format(loadable, f, loc))
                            except Exception as e:
                                log("Failed to upload {} for {} : ( {} )".format(loadable, f, e))
                            if n == 0:
                                gname = gname + str(n + 1)
                            else:
                                gname = gname[:-1] + str(n + 1)
                except Exception as e:
                    log("Failed to generate {} : ( {}  )".format(f, e))

            removed = []
            if args.removed:
                for f in args.removed.split(","):
                    if f.startswith(scopepath) and f.endswith(".ttl"):
                        removed.append(Path(f))

            print("Scope : {}".format(scopepath))
            if modified:
                print("modified:")
                print([str(x) for x in modified])
            if added:
                print("added:")
                print([str(x) for x in added])
            if removed:
                print("removed:")
                print([str(x) for x in removed])

#unit call of entailment
#example call arguments:
#
# specification-elements/defs/15-111r1.ttl
# scripts/spec_as_conceptscheme.shapes.ttl
# definitions/models/modspec_validations.ttl
# definitions/conceptschemes/status.ttl


import json
from glob import glob
from typing import List
import argparse
from pathlib import Path
from urllib.parse import urlencode, quote_plus


import sys
from pyshacl import validate
from rdflib import Graph, URIRef
from update_vocabs import get_closure_graph

f = sys.argv[1]
rules = sys.argv[2]
ont_g1 = sys.argv[3]
ont_g2 = sys.argv[4]

g = Graph().parse(str(f), format="ttl")
shg = Graph().parse(rules, format="ttl")
extra = get_closure_graph([ont_g1, ont_g2])

try:
    validate(g, shacl_graph=shg, ont_graph=extra, advanced=True, inplace=True)
except Exception as e:
    raise Exception("SHACL error in {}: {}".format(rules, str(e)))
g.serialize(destination=f+'.out', format='ttl')


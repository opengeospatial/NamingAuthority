#!/usr/bin/env python3

import csv
import requests
import json
import os
from pathlib import Path
from rdflib import Graph, URIRef, PROV

GS_URL = os.environ['SWGDOCMATCH_GS_URL']
SWG_FILE = 'entities/bodies.json'

BODIES = 'http://www.opengis.net/def/entities/bodies/'
DOCS = 'http://www.opengis.net/def/docs/'
OUTPUT = Path('definitions/docs/docs-working-groups.ttl')

print("Loading working groups file...")
with open(SWG_FILE, 'rb') as f:
    swgs = {int(s['id']): s for s in json.load(f)}

print("Downloading Google Spreadsheet...")
r = requests.get(GS_URL)
r.raise_for_status()

print("Matching...")
reader = csv.DictReader(r.text.splitlines())
g = Graph()
g.bind('bodies', BODIES)
g.bind('prov', PROV)
g.bind('docs', DOCS)
for row in reader:
    if row['SWGid']:
        try:
            doc_swg = int(row['SWGid'])
            g.add((URIRef(row['URI']), PROV.wasAttributedTo, URIRef(f"{BODIES}{doc_swg}")))
        except ValueError:
            # Not a numeric SWGid
            pass

changed = True
if OUTPUT.exists():
    print("Loading current version for comparison...")
    existing = Graph().parse(OUTPUT)
    changed = len(g ^ existing) > 0

if changed:
    print("Writing output...")
    g.serialize(OUTPUT, format='ttl')
else:
    print("No changes found")

print("All tasks done")

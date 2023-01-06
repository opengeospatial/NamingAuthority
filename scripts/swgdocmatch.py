#!/usr/bin/env python3

import csv
import requests
import json
from rdflib import Graph, URIRef, PROV

GS_URL = 'https://docs.google.com/spreadsheets/d/1zBdwiAmodZttlMwlk9vUgVoJ5oroVpHuce_0rZ8pJp4/export?format=csv'
SWG_FILE = 'incubation/working-groups/working-groups.json'

BODIES = 'http://www.opengis.net/def/entities/bodies/'
DOCS = 'http://www.opengis.net/def/docs/'

with open(SWG_FILE, 'rb') as f:
    swgs = {int(s['id']): s for s in json.load(f)}

r = requests.get(GS_URL)
r.raise_for_status()

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

g.serialize('incubation/working-groups/docs.ttl', format='ttl')

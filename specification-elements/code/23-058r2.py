#!/usr/bin/env python3

#############################################################

# 23-058r2: OGC API - Features - Part 5 / OGC API - Common - Part 3: Schemas
# https://github.com/opengeospatial/ogcapi-features/tree/master/extensions/schemas/standard
# https://www.ogc.org/standards/ogcapi-features/ ==> https://docs.ogc.org/is/23-058r2/23-058r2.html
# https://www.ogc.org/standards/ogcapi-common/ ==>  https://docs.ogc.org/is/23-058r2/23-058r2.html

### Target document URL
specURL = "https://docs.ogc.org/is/23-058r2/23-058r2.html"

### Base Namespace URI (No trailing slash)
baseNSURI = "http://www.opengis.net/spec/ogcapi-common-3/1.0"

DEBUG = True

#############################################################

import re

def isExternalHttp(token):
        return re.search(r'https?://', token) and baseNSURI not in token

def cleanString(intext):
    intext = intext.replace("\"", "")

    if "</" in intext:
        intext = intext[:intext.index("</")]

    # Remove &quote and everything after
    if "&quot" in intext:
        intext = intext[:intext.index("&quot")]

    # Remove trailing punctuation from source URI
    intext = intext.rstrip(".;,")

    if (
        intext.startswith("/req/")
        or intext.startswith("/conf/")
        or intext.startswith("/rec/")
        or intext.startswith("/per/")
        or intext.startswith("/ats/")
    ):
        intext = baseNSURI + intext

    return intext


def addElement(idtoken, token):

    uri = cleanString(token)
#    if DEBUG:
#        print(f"[DEBUG] AddElemt idtoken: {idtoken} token: {token} uri: {uri}")

    # Source URI must be unique; keep first occurrence only
    if uri not in seen_sources:
        seen_sources.add(uri)
        elementList.append((idtoken, uri))


document_number = specURL.rstrip("/").split("/")[-1].replace(".html", "").lower()

# output file
fout = open("../mappings/" + document_number + ".csv", "w")

# input file
fin = open("../specifications/" + document_number + ".html", "r")

elementList = []
seen_sources = set()

idtoken = ""
readingAnnex = 0

fout.write("target,source\n")

for line in fin:
    tokens = line.split()

    for token in tokens:
        if isExternalHttp(token):
            if DEBUG:
                print(f"[DEBUG] SKIP Ext idtoken: {idtoken} token: {token}")
            continue

        if token.startswith("id=\""):
            idtoken = token.replace("id=\"", "")
            idtoken = idtoken[:idtoken.index("\"")]
            if DEBUG:
                print(f"[DEBUG] ______ID idtoken: {idtoken} token: {token}")

        if "id=\"_abstract_test_suite_normative\"" in token:
            readingAnnex = 1

        if readingAnnex == 0:
            if "/req/" in token:
                if "http:" in token:
                    token = token[token.index("http:"):]
                else:
                    token = token[token.index("/req/"):]
                addElement(idtoken, token)

            if "/conf/" in token:
                if "http:" in token:
                    token = token[token.index("http:"):]
                else:
                    token = token[token.index("/conf/"):]
                addElement(idtoken, token)

            if "/rec/" in token:
                token = token[token.index("/rec/"):]
                addElement(idtoken, token)

            if "/per/" in token:
                token = token[token.index("/per/"):]
                addElement(idtoken, token)

        if readingAnnex == 1:
            if "/conf/" in token:
                token = token[token.index("/conf/"):]
                addElement(idtoken, token)

for idtoken, uri in elementList:
    if "example_" in idtoken:
        continue

    # Skip if source containing { or }
    if "{" in uri or "}" in uri:
        continue

    target = specURL + "#" + idtoken
    fout.write(target + "," + uri + "\n")

fin.close()
fout.close()

# vim: set syntax=python

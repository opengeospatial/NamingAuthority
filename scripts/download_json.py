#!/usr/bin/env python3
import json
from urllib import request
import sys
import os

if __name__ == '__main__':

    with open('json_downloads.json') as f:
        files = json.load(f)

    for file in files:
        print('Downloading file {url} to {dest}'.format(**file))

        try:
            with request.urlopen(file['url']) as r:
                if r.status != 200:
                    raise Exception("HTTP response {} - {}".format(r.status, r.reason))
                newcontent = json.loads(r.read())
        except Exception as e:
            print('Exception when parsing file from {}: {}'.format(file['url'], e), file=sys.stderr)
            continue

        overwrite = False
        if os.path.isfile(file['dest']):
            print('Destination file exists - comparing contents')
            try:
                with open(file['dest']) as f:
                    oldcontent = json.load(f)
            except Exception as e:
                print('Exception when opening old JSON file {}: {}'.format(file['dest'], e), file=sys.stderr)
                continue

            if oldcontent != newcontent:
                print('Content is different - updating')
                overwrite = True
            else:
                print('Contents are equal')
        else:
            print('Destination file is new')
            overwrite = True

        if overwrite:
            os.makedirs(os.path.dirname(file['dest']), exist_ok=True)
            try:
                with open(file['dest'], 'w') as f:
                    json.dump(newcontent, f, indent=2)
            except Exception as e:
                print('Exception writing output JSON file {}: {}'.format(file['dest'], e), file=sys.stderr)
                continue

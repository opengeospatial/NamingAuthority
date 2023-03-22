import json
import os.path
import html
import re
from html.parser import HTMLParser
import yaml
import csv
from yaml.representer import SafeRepresenter
try:
    from yaml import CDumper as YamlDumper
except ImportError:
    from yaml import Dumper as YamlDumper


def literal_unicode_representer(dumper, data):
    return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')


class LiteralString(str):
    pass


def change_yaml_style(style, representer):
    def new_representer(dumper, data):
        scalar = representer(dumper, data)
        scalar.style = style
        return scalar
    return new_representer


represent_literal_str = change_yaml_style('|', SafeRepresenter.represent_str)

yaml.add_representer(LiteralString, represent_literal_str)


def to_uri(term: str) -> str:
    uri = re.sub(r'[^A-Za-z0-9-]', ' ', re.sub(r'\s*\(.*\)$', '', term))
    uri = ''.join(w if re.fullmatch(r'[A-Z]+', w) or i == 0 else w.capitalize() for i, w in enumerate(uri.split()))
    return f"http://www.opengis.net/def/glossary/term/{uri}"


class DefParser(HTMLParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = ''
        self._breaking_tag = []

    def handle_starttag(self, tag, attrs) -> None:
        breaking = tag in ('p', 'div')
        self._breaking_tag.append(breaking)
        if breaking:
            self.text += '\n'

    def handle_endtag(self, tag: str) -> None:
        if self._breaking_tag.pop():
            self.text += '\n'

    def handle_data(self, data):
        self.text += re.sub(r'\n\r?', ' ', data)


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.realpath(__file__))
    glossary_fn = os.path.join(script_dir, 'glossary.json')
    with open(glossary_fn) as f:
        data = json.load(f)

    csv_fn = os.path.join(script_dir, 'glossary.csv')
    uris = {}
    with open(csv_fn, newline='') as f:
        reader = csv.reader(f)
        for rownum, row in enumerate(reader):
            if rownum == 0 or not row[1].strip():
                # skip header and empty URI
                continue
            uris[row[0]] = row[1]

    entries = data['GLOSSARY']['INFO']['ENTRIES']['ENTRY']
    output_entries = []
    for entry in entries:
        term = entry['CONCEPT']

        parser = DefParser()
        parser.feed(html.unescape(entry['DEFINITION']))
        definition = parser.text
        definition = re.sub(r' {2,}', ' ', definition)
        definition = re.sub('( *\n\r? *)+', '\n', definition, flags=re.M).strip()
        uri = uris.get(term)

        output_entry = {
            'term': term,
            'definition': LiteralString(definition),
        }
        if uri:
            output_entry['uri'] = uri
        else:
            output_entry['suggestedUri'] = to_uri(term)
        output_entries.append(output_entry)

    output_fn = os.path.join(script_dir, 'glossary-parsed.yaml')
    with open(output_fn, 'w') as f:
        yaml.dump_all(output_entries, f, sort_keys=False, allow_unicode=True, explicit_start=True)


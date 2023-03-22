import json
import os.path
import html
import re
from html.parser import HTMLParser
import yaml
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

class DefParser(HTMLParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = ''

    def handle_starttag(self, tag, attrs) -> None:
        self.text += '\n'

    def handle_endtag(self, tag: str) -> None:
        self.text += '\n'

    def handle_data(self, data):
        self.text += data


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.realpath(__file__))
    glossary_fn = os.path.join(script_dir, 'glossary.json')
    with open(glossary_fn) as f:
        data = json.load(f)

    entries = data['GLOSSARY']['INFO']['ENTRIES']['ENTRY']
    output_entries = []
    for entry in entries:
        term = entry['CONCEPT']

        parser = DefParser()
        parser.feed(html.unescape(entry['DEFINITION']))
        definition = parser.text
        definition = re.sub(r' {2,}', ' ', definition)
        definition = re.sub('( *\n\r? *)+', '\n', definition, flags=re.M).strip()
        output_entries.append({
            'term': term,
            'definition': LiteralString(definition),
        })

    output_fn = os.path.join(script_dir, 'glossary-parsed.yaml')
    with open(output_fn, 'w') as f:
        yaml.dump_all(output_entries, f, sort_keys=False, allow_unicode=True, explicit_start=True)


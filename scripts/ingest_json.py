# from __future__ import print_function
import json
import logging
import argparse
import re
import sys
from collections import deque
from pathlib import Path
from typing import Union, Optional, List, Tuple

import rdflib
from rdflib import Graph
from rdflib.namespace import DC, DCTERMS, SKOS, OWL, RDF, RDFS, XSD, DCAT
from pyld import jsonld
import jq
from os import path, scandir
from jsonpath_ng.ext import parse as jsonpathparse
from wcmatch.glob import globmatch

logger = logging.getLogger(__name__)


class IContextRegistry:
    def get_filenames(self, contextfn: Union[Path, str]) -> List[str]:
        pass

    def get_context(self, filename: Union[Path, str]) -> Optional[str]:
        pass

    def has_context(self, contextfn: Union[Path, str]) -> bool:
        pass

    def has_filename(self, filename: Union[Path, str]) -> bool:
        pass

    def __bool__(self):
        pass


class ContextRegistry(IContextRegistry):
    """
    Support class for context registry operations. A context registry
    is a yamlContextFilename:[listOfFilenameGlobs] mapping contained
    in a dict or a JSON document.
    The context registry has a root directory (implicit or explicit)
    which will be used for glob-matching operations.
    """

    registry: dict
    root_dir: Path

    def __init__(self, source: Union[str, dict], root_dir: Union[Path, str] = None):
        if isinstance(source, str):
            # load from file
            with open(source, 'r') as f:
                entries = json.load(f)
            self.root_dir = Path(root_dir) if root_dir else Path(source).parent
        else:
            # take as is
            entries = source
            self.root_dir = Path(root_dir) if root_dir else Path()

        # Resolve context filename paths
        self.registry = {}
        for ctx, globs in entries.items():
            p = Path(ctx)
            if not p.is_absolute():
                p = self.root_dir / p
            self.registry[p.resolve()] = globs

    def get_filenames(self, contextfn: Union[Path, str]) -> List[str]:
        """
        Tries to find a list of JSON/JSON-LD files for a given YAML context definition filename.
        :param contextfn: YAML context definition filename
        :return: corresponding JSON/JSON-LD filenames, if found
        """
        if not isinstance(contextfn, Path):
            contextfn = Path(contextfn)

        globs = self.registry.get(contextfn.resolve())
        if not globs:
            return []
        return [str(fn) for g in globs for fn in self.root_dir.glob(g)]

    def get_context(self, filename: Union[Path, str]) -> Optional[str]:
        """
        Tries to find the YAML context file for a given JSON file.
        :param filename: the filename of the JSON document
        :return: its corresponding YAML context file, or None
        """

        relativefn = Path(filename).relative_to(self.root_dir)
        for ctx, globs in self.registry.items():
            if globmatch(relativefn, globs):
                return ctx

    def has_context(self, contextfn: Union[Path, str]) -> bool:
        return (contextfn if isinstance(contextfn, Path) else Path(contextfn)).resolve() in self.registry

    def has_filename(self, filename: Union[Path, str]) -> bool:
        return bool(self.get_context(filename))

    def __bool__(self):
        return bool(self.registry)

    def __str__(self):
        return f"ContextRegistry(root_dir={self.root_dir},entries={self.registry})"


class ContextRegistryList(IContextRegistry):
    """
    Support class for aggregating ContextRegistry's.
    """

    def __init__(self, *args: ContextRegistry):
        self.registries: List[ContextRegistry] = list(args)

    def add(self, registry: ContextRegistry):
        self.registries.append(registry)

    def get_filenames(self, contextfn: Union[Path, str]) -> List[str]:
        return [fn for registry in self.registries for fn in registry.get_filenames(contextfn)]

    def get_context(self, filename: Union[Path, str]) -> Optional[str]:
        return next(
            filter(lambda x: x,
                   (registry.get_context(filename) for registry in self.registries)),
            None)

    def has_context(self, contextfn: Union[Path, str]) -> bool:
        return any(r.has_context(contextfn) for r in self.registries)

    def has_filename(self, filename: Union[Path, str]) -> bool:
        return any(r.has_filename(filename) for r in self.registries)

    def __bool__(self):
        return bool(self.registries) and any(bool(r) for r in self.registries)

    def __str__(self):
        return f"ContextRegistryList[{','.join(str(r) for r in self.registries)}]"


def init_graph() -> Graph:
    """
    Creates an empty graph with some standard prefixes.

    :return: an empty RDFLib Graph with some prefixes
    """

    g = rdflib.Graph()
    g.bind("dc", DC)
    g.bind("xsd", XSD)
    g.bind("dct", DCTERMS)
    g.bind("skos", SKOS)
    g.bind("owl", OWL)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    g.bind("dcat", DCAT)
    g.bind("iso", 'http://iso.org/tc211/')
    g.bind("spec", "http://www.opengis.net/def/ont/modspec/")
    g.bind("specrel", "http://www.opengis.net/def/ont/specrel/")
    g.bind("na", "http://www.opengis.net/def/metamodel/ogc-na/")
    g.bind("prov", "http://www.w3.org/ns/prov#")
    return g


def transform_json(data: dict, context: dict) -> dict:
    """
    Transform a JSON document loaded in a dict, and embed JSON-LD context into it.

    WARNING: This function modifies the input dict. If that is not desired, make a copy
    before invoking.

    :param data: the JSON document in dict format
    :param context: YAML context definition
    :return: the transformed and JSON-LD-enriched data
    """

    # Check if pre-transform necessary
    transform = context.get('transform')
    if transform:
        # Allow for transform lists to do sequential transformations
        if isinstance(transform, str):
            transform = (transform,)
        for t in transform:
            data = json.loads(jq.compile(t).input(data).text())

    # Add types
    types = context.get('types', {})
    for loc, typelist in types.items():
        items = jsonpathparse(loc).find(data)
        if isinstance(typelist, str):
            typelist = [typelist]
        for item in items:
            existing = item.value.setdefault('@type', [])
            if isinstance(existing, str):
                item.value['@type'] = [existing] + typelist
            else:
                item.value['@type'].extend(typelist)


    # Add contexts
    context_list = context.get('context', {})
    global_context = None
    for loc, val in context_list.items():
        if not loc or loc in ['.', '$']:
            global_context = val
        else:
            items = jsonpathparse(loc).find(data)
            for item in items:
                item.value['@context'] = val

    if global_context:
        data = {
            '@context': global_context,
            '@graph': data,
        }

    return data


def generate_graph(inputfn: str, contextfn: str, base: Optional[str] = None) -> Tuple[Graph, str]:
    """
    Create a graph from an input JSON document and a YAML context definition file.

    :param inputfn: input filename
    :param contextfn: YAML context definition filename
    :param base: base URI for JSON-LD context
    :return: a tuple with the resulting RDFLib Graph and the JSON-LD enriched file
    """

    g = init_graph()

    jsonld.set_document_loader(jsonld.requests_document_loader(timeout=5000))
    with open(inputfn, 'r') as j:
        inputdata = json.load(j)

    # Load YAML context file
    from yaml import load
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader
    with open(contextfn, 'r') as f:
        context = load(f, Loader=Loader)

    jdocld = transform_json(inputdata, context)

    options = {}
    if base:
        options['base'] = base
    elif context.get('base-uri'):
        options['base'] = context['base-uri']
    elif '@context' in jdocld and jdocld['@context'].get('@base'):
        options['base'] = jdocld['@context']['@base']
    output = json.dumps(jsonld.expand(jdocld, options), indent=2)
    g.parse(data=output, format='json-ld')

    return g, output


def process_file(inputfn: str,
                 jsonldfn: Optional[Union[bool, str]] = False,
                 ttlfn: Optional[Union[bool, str]] = False,
                 contextfn: Optional[str] = None,
                 context_registry: Optional[IContextRegistry] = None,
                 base: Optional[str] = None,
                 skip_on_missing_context: bool = False) -> List[str]:
    """
    Process input file and generate output RDF files.

    :param inputfn: input filename
    :param jsonldfn: output JSON-lD filename (None for automatic).
        If False, no JSON-LD output will be generated
    :param ttlfn: output Turtle filename (None for automatic).
        If False, no Turtle output will be generated.
    :param contextfn: YAML context filename. If None, will be autodetected:
        1. From a file with the same name but yml/yaml extension (test.json -> test.yml)
        2. From a _json-context.yml/_json-context.yaml file in the same directory
    :param context_registry: dict with filename:yamlContextFilename mappings. Will be ignored
        if contextfn is provided
    :param base: base URI for JSON-LD
    :param skip_on_missing_context: whether to silently fail if no context file is found
    :return: List of output files created
    """

    if not path.isfile(inputfn):
        raise IOError(f'Input is not a file ({inputfn})')

    inputbase, inputext = path.splitext(inputfn)

    if not contextfn:
        contextfn = find_context_filename(inputfn, context_registry)

    if not contextfn:
        if skip_on_missing_context:
            logger.warning("No context file provided and one could not be discovered automatically. Skipping...")
            return []
        raise Exception('No context file provided and one could not be discovered automatically')

    g, jsonlddoc = generate_graph(inputfn, contextfn, base)

    createdfiles = []
    # False = do not generate
    # None = auto filename
    # - = stdout
    if ttlfn or ttlfn is None:
        if ttlfn == '-':
            print(g.serialize(format='ttl'))
        else:
            if not ttlfn:
                ttlfn = f'{inputbase}.ttl' if inputext != '.ttl' else f'{inputfn}.ttl'
            g.serialize(destination=ttlfn, format='ttl')
            createdfiles.append(ttlfn)

    # False = do not generate
    # None = auto filename
    # "-" = stdout
    if jsonldfn or jsonldfn is None:
        if jsonldfn == '-':
            print(jsonlddoc)
        else:
            if not jsonldfn:
                jsonldfn = f'{inputbase}.jsonld' if inputext != '.jsonld' else f'{inputfn}.jsonld'
            with open(jsonldfn, 'w') as f:
                f.write(jsonlddoc)
            createdfiles.append(jsonldfn)

    return createdfiles


def find_context_filename(filename, registry: Optional[IContextRegistry]) -> Optional[str]:
    """
    Find the YAML context file for a given filename, with the following precedence:
        1. Search in registry (if provided)
        2. Search file with same base name but with yaml/yml extension.
        3. Find _json-context.yml/yaml file in same directory
    :param filename: the filename for which to find the context
    :param registry: an optional filename:yamlContextFile mapping
    :return: the YAML context definition filename
    """

    # 1. Registry lookup
    if registry:
        yml = registry.get_context(filename)
        if yml:
            return yml

    # 2. Same filename with yml/yaml extension or autodetect in dir
    base, ext = path.splitext(filename)
    dirname = path.dirname(filename)

    for cfn in [
        f'{filename}.yml',
        f'{filename}.yaml',
        f'{base}.yaml',
        f'{base}.yml',
        path.join(dirname, '_json-context.yml'),
        path.join(dirname, '_json-context.yaml'),
    ]:
        if path.isfile(cfn):
            logger.info(f'Autodetected context {cfn} for file {filename}')
            return cfn


def filenames_from_context(contextfn: str, registry: Optional[IContextRegistry]) -> Optional[List[str]]:
    """
    Tries to find a JSON/JSON-LD file from a given YAML context definition filename.
    Priority:
      1. Context file in registry (if registry present)
      2. Context file with same name as JSON doc (e.g. test.yml/test.json)
      3. Context file in directory (_json-context.yml or _json-context.yaml)
    :param contextfn: YAML context definition filename
    :param registry: dict of jsonFile:yamlContextFile mappings
    :return: corresponding JSON/JSON-LD filename, if found
    """

    # 1. Reverse lookup in registry
    if registry:
        found = registry.get_filenames(contextfn)
        if found:
            return found

    # 2. Lookup by matching filename
    basefn = path.splitext(contextfn)[0]
    if re.match(r'.*\.json-?(ld)?$', basefn):
        # If removing extension results in a JSON/JSON-LD
        # filename, try it
        return basefn if not registry.has_filename(basefn) and path.isfile(basefn) else None
    # Otherwise check with appended JSON/JSON-LD extensions
    for e in ('.json', '.jsonld', '.json-ld'):
        jsonfn = basefn + e
        if not registry.has_filename(jsonfn) and path.isfile(jsonfn):
            return jsonfn

    # 3. If directory context file, all .json files in directory
    # NOTE: no .jsonld or .json-ld files, since those could come
    #   from the output of this very script
    # NOTE: excluding those files present in the registry
    dirname, ctxfn = path.split(contextfn)
    if re.match(r'_json-context\.ya?ml', ctxfn):
        with scandir(dirname) as it:
            return [x.path for x in it
                    if (x.is_file() and x.name.endswith('.json')
                        and not registry.has_filename(x))]


def process(inputfiles: str,
            context_registry: Optional[IContextRegistry] = None,
            contextfn: Optional[str] = None,
            jsonldfn: Optional[Union[bool, str]] = False,
            ttlfn: Optional[Union[bool, str]] = False,
            batch: bool = False,
            base: str = None,
            skip_on_missing_context: bool = False):
    result = []
    if batch:
        logger.info("Input files: %s", inputfiles)
        remaining_fn: deque = deque(inputfiles.split(','))
        while remaining_fn:
            fn = remaining_fn.popleft()

            if re.match(r'.*\.ya?ml$', fn):
                # Context file found, try to find corresponding JSON/JSON-LD file(s)
                logger.info('Potential YAML context file found: %s', fn)
                remaining_fn.extend(filenames_from_context(fn, context_registry))
                continue

            if not re.match(r'.*\.json-?(ld)?$', fn):
                logger.debug('File %s does not match, skipping', fn)
                continue
            logger.info('File %s matches, processing', fn)
            try:
                result += process_file(
                    fn,
                    jsonldfn=False if jsonldfn is False else None,
                    ttlfn=False if ttlfn is False else None,
                    contextfn=None,
                    context_registry=context_registry,
                    base=base,
                    skip_on_missing_context=True
                )
            except Exception as e:
                logger.warning("Error processing JSON/JSON-LD file, skipping: %s", str(e))
    else:
        result += process_file(
            inputfiles,
            jsonldfn=jsonldfn if jsonldfn is not None else '-',
            ttlfn=ttlfn if ttlfn is not None else '-',
            contextfn=contextfn,
            context_registry=context_registry,
            base=base,
            skip_on_missing_context=skip_on_missing_context,
        )

    return result


def _process_cmdln():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        help="Source file (instead of service)",
    )

    parser.add_argument(
        '-j',
        '--json-ld',
        action='store_true',
        help="Generate JSON-LD output file",
    )

    parser.add_argument(
        '--json-ld-file',
        help='JSON-LD output filename',
    )

    parser.add_argument(
        '-t',
        '--ttl',
        action='store_true',
        help='Generate TTL output file',
    )

    parser.add_argument(
        "--ttl-file",
        help="TTL output filename",
    )

    parser.add_argument(
        '-c',
        '--context',
        help='YAML context file (instead of autodetection)',
    )

    parser.add_argument(
        '-b',
        '--base-uri',
        help='Base URI for JSON-LD',
    )

    parser.add_argument(
        '-s',
        '--skip-on-missing-context',
        help='Skip files for which a context definition cannot be found (instead of failing)',
    )

    parser.add_argument(
        '--batch',
        help='Batch processing where input file is one or more files separated by commas, context files are '
             'autodiscovered and output file names are always auto generated',
        action='store_true'
    )

    parser.add_argument(
        '--fs',
        help='File separator for formatting list of output files (no output by default)',
    )

    parser.add_argument(
        '-r',
        '--context-registry',
        action='append',
        default=[],
        help='JSON context registry file containing an object of jsonFile:yamlContextFile pairs'
    )

    args = parser.parse_args()

    context_registry = ContextRegistryList(*(ContextRegistry(c) for c in args.context_registry))

    outputfiles = process(args.input,
                          contextfn=args.context,
                          context_registry=context_registry,
                          jsonldfn=args.json_ld_file if args.json_ld else False,
                          ttlfn=args.ttl_file if args.ttl else False,
                          batch=args.batch,
                          base=args.base_uri,
                          skip_on_missing_context=args.skip_on_missing_context)

    if args.fs:
        print(args.fs.join(outputfiles))


if __name__ == '__main__':

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format='%(asctime)s,%(msecs)d %(levelname)-5s [%(filename)s:%(lineno)d] %(message)s',
    )

    _process_cmdln()

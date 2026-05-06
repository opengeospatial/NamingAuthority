from __future__ import annotations

import argparse
import fnmatch
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from glob import glob as fsglob
from pathlib import Path

import yaml
from rdflib import Graph

from vocab_utils import DOMAIN_CFG, find_domain_cfg, get_entailedpath, get_graph_uri_for_vocab, load_vocab, log

REGISTER_FILE = 'production-register.yaml'
TRACKER_FILE = 'production-tracker.json'


def get_blob_hash(filepath: str) -> str | None:
    """Return the git blob hash for a tracked file, or None if untracked."""
    result = subprocess.run(['git', 'ls-files', '-s', filepath], capture_output=True, text=True)
    line = result.stdout.strip()
    if not line:
        return None
    # format: <mode> <hash> <stage>\t<file>
    return line.split()[1]


def get_current_commit() -> str:
    result = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True)
    return result.stdout.strip()


def resolve_register(register_path: str) -> list[dict]:
    """Load register and resolve globs to a deduplicated list of {path, auto} dicts."""
    with open(register_path) as f:
        data = yaml.safe_load(f)

    seen = set()
    entries = []
    for entry in data.get('files', []):
        pattern = entry['path']
        auto = entry.get('auto', False)
        for filepath in fsglob(pattern, recursive=True):
            normalized = os.path.normpath(filepath)
            if normalized not in seen:
                seen.add(normalized)
                entries.append({'path': normalized, 'auto': auto})
    return entries


def apply_filter(entries: list[dict], file_filter: str) -> list[dict]:
    """Intersect entries with comma-separated glob patterns. '*' passes everything through."""
    if file_filter == '*':
        return entries
    patterns = [p.strip() for p in file_filter.split(',')]
    seen = set()
    result = []
    for entry in entries:
        for pattern in patterns:
            if fnmatch.fnmatch(entry['path'], pattern):
                if entry['path'] not in seen:
                    seen.add(entry['path'])
                    result.append(entry)
                break
    return result


def promote(candidates: list[dict], tracker: dict, rdf_service: str) -> dict:
    """Compare hashes, upload changed files, update tracker in place. Returns updated tracker."""
    commit = get_current_commit()
    any_change = False

    for entry in candidates:
        source_path = entry['path']

        _, cfg = find_domain_cfg(source_path)
        if cfg is None:
            log(f"Warning: {source_path} does not match any domain config, skipping")
            continue

        entailed_path, _, _, _ = get_entailedpath(source_path, None, 'ttl',
                                                   rootpattern=cfg['uri_root_filter'])
        if not entailed_path or not Path(entailed_path).exists():
            log(f"ERROR: entailed TTL not found for {source_path} at {entailed_path} — "
                f"run the dev pipeline first")
            sys.exit(1)

        blob_hash = get_blob_hash(entailed_path)
        if blob_hash is None:
            log(f"ERROR: entailed TTL {entailed_path} is not tracked by git — "
                f"run the dev pipeline first")
            sys.exit(1)

        existing_hash = tracker.get(source_path, {}).get('entailed_hash')
        if existing_hash == blob_hash:
            log(f"Up to date: {source_path}")
            continue

        # Upload entailed TTL + domain annotations
        try:
            entailed_g = Graph().parse(entailed_path, format='ttl')
            try:
                gname = list(get_graph_uri_for_vocab(None, entailed_g))[0]
            except (IndexError, StopIteration):
                gname = "x-urn:{}".format(source_path.replace('\\', ':'))

            annotations = cfg.get('annotations') or []
            loadlist = [entailed_path] + annotations
            for n, loadable in enumerate(loadlist):
                # need to add annotations to a new context
                loc = load_vocab(loadable, gname, rdf_service)
                log(f"Uploaded {loadable} for {source_path} to {loc}")
                if n == 0:
                    gname = gname + str(n + 1)
                else:
                    gname = gname[:-1] + str(n + 1)

            tracker[source_path] = {
                'entailed_hash': blob_hash,
                'promoted_at': datetime.now(timezone.utc).isoformat(),
                'commit': commit,
            }
            any_change = True
            log(f"Promoted: {source_path}")
        except Exception as e:
            log(f"ERROR: failed to promote {source_path}: {e}")
            raise

    if not any_change:
        log("Everything up to date, nothing to promote.")

    return tracker


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Promote production-ready entailed TTL files to the production triplestore.'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        'file_filter',
        nargs='?',
        metavar='FILE_FILTER',
        help="Comma-separated glob patterns for source files to consider. Use '*' for all.",
    )
    group.add_argument(
        '--auto-only',
        action='store_true',
        help="Promote only register entries marked auto:true (used by the scheduled workflow).",
    )
    args = parser.parse_args()

    if not args.auto_only and not args.file_filter:
        parser.error("Provide FILE_FILTER or --auto-only")

    RDF_SERVICE = os.environ.get('PROD_RDF_SERVICE_URL')
    if not RDF_SERVICE:
        log("ERROR: PROD_RDF_SERVICE_URL environment variable is not set")
        sys.exit(1)
    log(f"Using RDF service: {RDF_SERVICE}")

    entries = resolve_register(REGISTER_FILE)

    if args.auto_only:
        candidates = [e for e in entries if e['auto']]
        log(f"Auto-only mode: {len(candidates)} candidate(s)")
    else:
        candidates = apply_filter(entries, args.file_filter)
        log(f"Filter '{args.file_filter}': {len(candidates)} candidate(s)")

    if not candidates:
        log("No candidates matched. Exiting.")
        sys.exit(0)

    tracker_path = Path(TRACKER_FILE)
    tracker = json.loads(tracker_path.read_text()) if tracker_path.exists() else {}

    tracker = promote(candidates, tracker, RDF_SERVICE)

    tracker_path.write_text(json.dumps(tracker, indent=2, sort_keys=True) + '\n')

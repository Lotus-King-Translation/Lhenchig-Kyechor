#!/usr/bin/env python3
"""Negative corruption tests against copied evidence, never the canonical files."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
from validate_paired import ROOT, validate


def rewrite(root, path, f):
    p = root / path
    p.write_text(f(p.read_text()))


def repin(root, key, path):
    p = root / 'source/provenance.json'
    obj = json.loads(p.read_text())
    obj[key] = hashlib.sha256((root / path).read_bytes()).hexdigest()
    p.write_text(json.dumps(obj))


def source_mutation(root, old, new):
    rewrite(root, 'paired/source.md', lambda s: s.replace(old, new, 1))
    # Test semantic structure beyond the outer pinned-file checksum.
    repin(root, 'paired_source_sha256', 'paired/source.md')


def run(allow_incomplete=False):
    tests = [
        ('wrong source edition', lambda r: rewrite(r, 'paired/translation.md', lambda s: s.replace('source-edition: provisional-source-v1', 'source-edition: wrong'))),
        ('missing source format', lambda r: source_mutation(r, ' | format: h1', '')),
        ('unsupported source format', lambda r: source_mutation(r, 'format: h1', 'format: unknown')),
        ('format boundary change', lambda r: source_mutation(r, 'format: h1', 'format: verse')),
        ('missing source anchor', lambda r: source_mutation(r, 'source: L0003 L0004', 'source: L0004')),
        ('duplicated source coverage', lambda r: source_mutation(r, 'source: L0003 L0004', 'source: L0003 L0003 L0004')),
        ('unknown source anchor', lambda r: source_mutation(r, 'source: L0001', 'source: L9999')),
        ('source spelling mutation', lambda r: source_mutation(r, 'དང་པོ', 'དང་པར')),
        ('source token marker leakage', lambda r: source_mutation(r, 'དང་པོ', 'དང་␣པོ')),
        ('duplicate translation ID', lambda r: rewrite(r, 'paired/translation.md', lambda s: s.replace('pair: LCK-000002', 'pair: LCK-000001'))),
        ('translation order swap', lambda r: rewrite(r, 'paired/translation.md', lambda s: s.replace('LCK-000001', 'LCK-TEMP').replace('LCK-000002', 'LCK-000001').replace('LCK-TEMP', 'LCK-000002'))),
        ('missing closing translation', lambda r: rewrite(r, 'paired/translation.md', lambda s: s[:s.index('<!-- pair: LCK-000110')].rstrip()+'\n')),
        ('empty translation block', lambda r: rewrite(r, 'paired/translation.md', lambda s: s[:s.index('<!-- pair: LCK-000110')]+ '<!-- pair: LCK-000110 -->\n')),
        ('translation duplicates source format', lambda r: rewrite(r, 'paired/translation.md', lambda s: s.replace('pair: LCK-000001 -->', 'pair: LCK-000001 | format: h1 -->'))),
        ('archive byte corruption', lambda r: rewrite(r, 'source/archive/root/001.txt', lambda s: s+'\n')),
        ('glossary mutation', lambda r: rewrite(r, 'glossary/expanded_tibetan_english_glossary.csv', lambda s: s.replace('Ordinary mind', 'Mind'))),
    ]
    if not allow_incomplete:
        tests += [
            ('unprocessed pair', lambda r: rewrite(r, 'paired/translation.md', lambda s: s.replace('<!-- pair: LCK-000110 -->', '<!-- pair: LCK-000110 -->\n\n[Not yet translated.]'))),
            ('required note removed', lambda r: rewrite(r, 'paired/translation.md', lambda s: __import__('re').sub(r'\[N-[A-Z]\d+\]\(\.\./translations/NOTES\.md#n-[a-z]\d+\)', '', s, count=1))),
            ('broken note reference', lambda r: rewrite(r, 'paired/translation.md', lambda s: s.replace('<!-- pair: LCK-000001 -->', '<!-- pair: LCK-000001 -->\n\n[N-Z999](../translations/NOTES.md#n-z999)'))),
        ]
    results = []
    for name, mutation in tests:
        with tempfile.TemporaryDirectory(prefix='lck-negative-') as td:
            dest = Path(td) / 'repo'
            shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns('.git', '__pycache__'))
            mutation(dest)
            try:
                validate(dest, allow_incomplete=allow_incomplete)
            except (ValueError, KeyError, OSError) as exc:
                results.append({'fixture': name, 'result': 'pass; corruption rejected', 'observed': str(exc)})
            else:
                raise AssertionError('Corruption accepted: ' + name)
    with tempfile.TemporaryDirectory(prefix='lck-unsigned-') as td:
        dest = Path(td) / 'repo'
        shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        (dest / 'translations/signoff.json').unlink(missing_ok=True)
        try:
            validate(dest, allow_incomplete=allow_incomplete, final=True)
        except ValueError as exc:
            assert 'explicit signoff' in str(exc), str(exc)
            results.append({'fixture': 'unsigned final gate', 'result': 'pass; rejected', 'observed': str(exc)})
        else:
            raise AssertionError('Unsigned final validation accepted')
    return {'tests': results, 'passed': len(results), 'failed': 0, 'semantic_tests': 'not these tests; see independent QC reports'}


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--allow-incomplete', action='store_true')
    a=p.parse_args()
    print(json.dumps(run(a.allow_incomplete), indent=2))

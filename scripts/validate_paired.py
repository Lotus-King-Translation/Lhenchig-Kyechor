#!/usr/bin/env python3
"""Validate LCK's documented provisional-source paired-text/2 profile."""
import argparse
import ast
import csv
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAIR = re.compile(r'<!-- pair: (LCK-\d{6})([^\n]*?) -->')
FORMATS = {'h1', 'h2', 'h3', 'prose', 'verse'}
NOTE = re.compile(r'\[(N-[A-Z]\d+)\]\(\.\./translations/NOTES\.md#(n-[a-z]\d+)\)')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(path.read_text())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def parse(text, source_side):
    require(text.startswith('---\n'), 'missing front matter')
    boundary = text.find('\n---\n', 4)
    require(boundary > 0, 'unterminated front matter')
    fm = {}
    for line in text[4:boundary].splitlines():
        key, sep, val = line.partition(':')
        require(sep and key not in fm, 'invalid/duplicate front matter field')
        fm[key] = val.strip()
    matches = list(PAIR.finditer(text))
    require(matches, 'no source/translation pairs')
    require(text[boundary + 5:matches[0].start()].strip() == '', 'unpaired content before first pair')
    require(text.count('<!-- pair:') == len(matches), 'malformed pair marker')
    rows = []
    for i, match in enumerate(matches):
        metadata = {}
        for bit in match.group(2).split('|'):
            if not bit.strip():
                continue
            key, sep, val = bit.strip().partition(':')
            require(sep and key not in metadata, 'invalid/duplicate pair metadata')
            metadata[key] = val.strip()
        if source_side:
            require(set(metadata) == {'source', 'role', 'format'}, 'missing/unexpected source metadata')
            require(metadata['format'] in FORMATS, 'unsupported format')
        else:
            require(not metadata, 'English must inherit source metadata')
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[match.end():end].strip('\n')
        require(body.strip(), 'empty pair ' + match.group(1))
        rows.append({'id': match.group(1), **metadata, 'text': body})
    require(len({r['id'] for r in rows}) == len(rows), 'duplicate pair ID')
    return fm, rows


def parse_po(path):
    rows, entry, field = [], {}, None
    for line in path.read_text().splitlines() + ['']:
        if not line.strip():
            if entry.get('msgid'):
                rows.append(entry)
            entry, field = {}, None
            continue
        m = re.match(r'(msgctxt|msgid|msgstr) (".*")$', line)
        if m:
            field = m[1]
            entry[field] = ast.literal_eval(m[2])
        elif line.startswith('"') and field:
            entry[field] += ast.literal_eval(line)
    return rows


def validate(root=ROOT, allow_incomplete=False, final=False):
    provenance = read_json(root / 'source/provenance.json')
    for row in csv.DictReader((root / 'editions/REGISTER.csv').open()):
        require(sha(root / row['path']) == row['sha256'], 'archive hash mismatch: ' + row['path'])
    require(sha(root / provenance['source_path']) == provenance['source_sha256'], 'source baseline hash mismatch')
    for key, path in [('glossary_sha256', 'glossary/expanded_tibetan_english_glossary.csv'),
                      ('guidance_sha256', 'guidelines/tibetan_translation_standard_v2.md'),
                      ('segmentation_sha256', 'paired/segmentation.json'),
                      ('paired_source_sha256', 'paired/source.md')]:
        require(sha(root / path) == provenance[key], 'pinned input changed: ' + path)
    sfm, sources = parse((root / 'paired/source.md').read_text(), True)
    tfm, targets = parse((root / 'paired/translation.md').read_text(), False)
    require(sfm.get('schema') == tfm.get('schema') == 'paired-text/2', 'wrong schema')
    require(sfm.get('text-id') == tfm.get('text-id') == 'LCK', 'wrong text identity')
    require(sfm.get('edition') == tfm.get('source-edition') == provenance['source_edition'], 'source edition mismatch')
    require(sfm.get('language') == 'bo' and tfm.get('language') == 'en', 'wrong language')
    require(bool(tfm.get('translation-edition')), 'missing translation edition')
    segments = read_json(root / 'paired/segmentation.json')
    expected = [r['id'] for r in segments]
    require([r['id'] for r in sources] == [r['id'] for r in targets] == expected, 'pair symmetry/order/coverage mismatch')
    raw = (root / provenance['source_path']).read_text().splitlines()
    seen = []
    for source, seg in zip(sources, segments):
        anchors = list(range(seg['start_line'], seg['end_line'] + 1))
        require(source['source'].split() == [f'L{n:04}' for n in anchors], 'source anchor mismatch')
        require(source['format'] == seg['format'] and source['role'] == seg['role'], 'source structure mismatch')
        require(source['text'] == '\n'.join(raw[seg['start_line'] - 1:seg['end_line']]), 'source text differs from pinned transcript')
        require(not any(c in source['text'] for c in '␣ '), 'legacy marker leaked into source')
        seen += anchors
    require(seen == list(range(1, len(raw) + 1)), 'source objects lost, duplicated or reordered')
    require(sources[-1]['role'] == 'work_colophon', 'lost closing material')
    bo = parse_po(root / 'source/archive/wip/bo/001.po')
    en = parse_po(root / 'source/archive/wip/en/001.po')
    ref = read_json(root / 'source/reference.json')
    require(len(raw) == len(bo) == len(en) == len(ref) == 589, 'legacy input count mismatch')
    for n, (original, b, e, r) in enumerate(zip(raw, bo, en, ref), 1):
        require(b['msgctxt'] == e['msgctxt'] == r['legacy_context'] and b['msgid'] == e['msgid'], 'PO identity mismatch')
        decoded = e['msgid'].replace(' ', '').replace('␣', '').replace(' ', ' ')
        require(decoded == original.rstrip(' ') if n == 493 else decoded == original, 'token reversal mismatch')
        require(r['tibetan'] == original and r['human_reference'] == e['msgstr'] and r['decoded_po'] == decoded, 'reference projection mismatch')
    incomplete = [r['id'] for r in targets if '[Not yet translated.]' in r['text']]
    require(allow_incomplete or not incomplete, 'unprocessed English pairs')
    note_count = 0
    if not incomplete:
        notes = read_json(root / 'translations/notes.json')
        note_map = {n['id']: n for n in notes}
        require(len(note_map) == len(notes), 'duplicate note ID')
        valid_anchors = {f'L{n:04}' for n in seen}
        required = {'id', 'pairs', 'anchors', 'tibetan', 'category', 'problem', 'treatment', 'uncertainty', 'review_action'}
        for note in notes:
            require(required <= note.keys(), 'incomplete note record ' + note['id'])
            require(set(note['pairs']) <= set(expected) and note['pairs'], 'invalid note pair')
            require(set(note['anchors']) <= valid_anchors and note['anchors'], 'invalid note anchor')
            for key in required - {'pairs', 'anchors'}:
                require(bool(note[key]), 'empty note field ' + key)
        for target in targets:
            links = NOTE.findall(target['text'])
            require(len(re.findall(r'\[N-[A-Z]\d+\]', target['text'])) == len(links), 'malformed note link')
            for ident, anchor in links:
                require(ident in note_map and anchor == ident.lower(), 'broken translation note')
                require(target['id'] in note_map[ident]['pairs'], 'note occurrence missing from note coverage')
        for note in notes:
            for pair in note['pairs']:
                target = targets[expected.index(pair)]
                require(f'[{note["id"]}]' in target['text'], 'required note lost at ' + pair)
        note_count = len(notes)
    if final:
        signoff = root / 'translations/signoff.json'
        require(signoff.exists(), 'final mode requires explicit signoff')
        record = read_json(signoff)
        require(record.get('status') == 'agent-reviewed-provisional-working-release', 'wrong signoff scope')
        require(record.get('human_certification') is False, 'unsubstantiated human certification')
        for path, digest in record['artifact_sha256'].items():
            require(sha(root / path) == digest, 'signed artifact mutated: ' + path)
        require(set(record['reviewed_pairs']) == set(expected), 'independent QC coverage incomplete')
        require(record.get('undisposed_findings') == 0, 'undisposed QC findings')
    return {'schema': 'paired-text/2; LCK provisional profile', 'pairs': len(sources), 'source_lines': len(seen),
            'translated_pairs': len(targets) - len(incomplete), 'unprocessed_pairs': len(incomplete),
            'formats': {f: sum(r['format'] == f for r in sources) for f in sorted(FORMATS)},
            'notes': note_count, 'source_edition': sfm['edition'], 'translation_edition': tfm['translation-edition'],
            'archive_hashes': 'pass', 'input_hashes': 'pass', 'exact_source_reconstruction': 'pass',
            'legacy_reversal': 'pass (L0493 documented trailing-space loss)', 'closing_material': 'retained',
            'final_mode': final, 'semantic_certification': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allow-incomplete', action='store_true')
    parser.add_argument('--final', action='store_true')
    args = parser.parse_args()
    try:
        print(json.dumps(validate(allow_incomplete=args.allow_incomplete, final=args.final), indent=2))
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, f'PAIRED VALIDATION FAILED: {exc}\n')

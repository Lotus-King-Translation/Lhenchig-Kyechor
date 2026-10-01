#!/usr/bin/env python3
"""Build supporting views; never rewrite the canonical source or translation."""
import json
from pathlib import Path
from validate_paired import ROOT, parse, sha, validate


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    result = validate()
    sfm, source = parse((ROOT / 'paired/source.md').read_text(), True)
    tfm, translation = parse((ROOT / 'paired/translation.md').read_text(), False)
    notes = json.loads((ROOT / 'translations/notes.json').read_text())
    usages = json.loads((ROOT / 'translations/usages.json').read_text())
    segments = json.loads((ROOT / 'paired/segmentation.json').read_text())
    hashes = {p: sha(ROOT / p) for p in ['paired/source.md', 'paired/translation.md', 'translations/notes.json', 'translations/usages.json']}
    coverage = []
    bilingual = ['# Lhenchig Kyechor — Tibetan and English', '',
                 'Generated from the canonical paired files by `scripts/build_support.py`. Provisional source; annotated working translation. Verse lineation follows the canonical files. See [notes](../translations/NOTES.md).', '']
    for s, t, seg in zip(source, translation, segments):
        note_ids = [n['id'] for n in notes if s['id'] in n['pairs']]
        coverage.append({'pair': s['id'], 'start_line': seg['start_line'], 'end_line': seg['end_line'],
                         'anchors': s['source'].split(), 'format': s['format'], 'role': s['role'],
                         'status': 'translated; annotated provisional interpretation' if note_ids else 'translated', 'notes': note_ids})
        bilingual += [f'<!-- {s["id"]} -->', f'**{s["id"]} · L{seg["start_line"]:04}–L{seg["end_line"]:04}**', '']
        if s['format'] == 'verse':
            bilingual += ['  \n'.join(s['text'].splitlines()), '', '  \n'.join(t['text'].splitlines()), '']
        elif s['format'].startswith('h'):
            bilingual += ['## ' + s['text'], '', '## ' + t['text'], '']
        else:
            bilingual += [s['text'], '', t['text'], '']
    dump(ROOT / 'paired/coverage.json', {'generated_by': 'scripts/build_support.py', 'inputs': hashes, 'pairs': coverage})
    dump(ROOT / 'paired/manifest.json', {'generated_by': 'scripts/build_support.py', 'source_edition': sfm['edition'],
                                       'translation_edition': tfm['translation-edition'], 'inputs': hashes, 'validation': result})
    (ROOT / 'paired/bilingual.md').write_text('\n'.join(bilingual).rstrip() + '\n')
    lines = ['# Translation and source notes', '', 'Generated from `notes.json`. All locations refer to provisional-source-v1 and its exact archival line anchors. Provisional readings and terminology are not approved glossary changes. No physical witness was consulted.', '']
    for n in notes:
        lines += [f'<a id="{n["id"].lower()}"></a>', f'## {n["id"]}', '',
                  '**Location:** ' + ', '.join(n['pairs']) + '; ' + ', '.join(n['anchors']) + '.', '',
                  '**Exact Tibetan:** ' + n['tibetan'], '',
                  '**Category:** ' + n['category'], '',
                  '**Problem and evidence:** ' + n['problem'], '',
                  '**Working treatment:** ' + n['treatment'], '',
                  '**Uncertainty:** ' + n['uncertainty'], '',
                  '**Review action:** ' + n['review_action'], '']
    (ROOT / 'translations/NOTES.md').write_text('\n'.join(lines).rstrip() + '\n')
    lines = ['# Terminology and usage record', '', 'Generated from `usages.json`. Canonical glossary assignments remain unchanged. A provisional local construction does not become an approved general default.', '']
    for u in usages:
        lines += ['- **' + ', '.join(u['pairs']) + '** — ' + u['tibetan'] + '\n  Canonical entry: ' + u['canonical_entry'] + '; English: ' + u['english'] + '; category: ' + u['category'] + '.\n  ' + u['condition'] + ' Reference: ' + u['note_id'] + '.', '']
    (ROOT / 'translations/USAGE.md').write_text('\n'.join(lines).rstrip() + '\n')
    print(json.dumps({'generated_views': 5, 'pairs': len(coverage), 'notes': len(notes), 'usages': len(usages)}))


if __name__ == '__main__':
    main()

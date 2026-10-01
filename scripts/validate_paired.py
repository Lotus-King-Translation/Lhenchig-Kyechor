#!/usr/bin/env python3
"""Validate the generic paired-text/2 source/translation contract."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paired/source.md"
TRANSLATION = ROOT / "paired/translation.md"
ALLOWED_FORMATS = {"prose", "verse", "h1", "h2", "h3"}
PAIR = re.compile(r"<!-- pair: ([^|>]+?)(.*?) -->")


def front_matter(text):
    if not text.startswith("---\n"):
        raise ValueError("missing front matter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated front matter")
    values = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise ValueError("invalid front matter line: " + line)
        values[key.strip()] = value.strip()
    return values


def pairs(text, source_side):
    rows = []
    seen = set()
    for match in PAIR.finditer(text):
        ident = match.group(1).strip()
        if ident in seen:
            raise ValueError("duplicate pair ID: " + ident)
        seen.add(ident)
        metadata = {}
        for piece in match.group(2).split("|"):
            piece = piece.strip()
            if not piece:
                continue
            key, sep, value = piece.partition(":")
            if not sep:
                raise ValueError("invalid pair metadata for " + ident)
            metadata[key.strip()] = value.strip()
        if source_side:
            missing = {"golden", "role", "format"} - metadata.keys()
            if missing:
                raise ValueError(f"{ident} missing source metadata: {sorted(missing)}")
            if metadata["format"] not in ALLOWED_FORMATS:
                raise ValueError(f"{ident} unsupported format: {metadata['format']}")
        rows.append((ident, metadata))
    return rows


def main():
    source = SOURCE.read_text(encoding="utf-8")
    translation = TRANSLATION.read_text(encoding="utf-8")
    sfm, tfm = front_matter(source), front_matter(translation)
    if sfm.get("schema") != "paired-text/2" or tfm.get("schema") != "paired-text/2":
        raise ValueError("both files must use schema paired-text/2")
    if sfm.get("text-id") != tfm.get("text-id"):
        raise ValueError("text-id mismatch")
    if tfm.get("source-edition") not in {sfm.get("edition"), "unset"}:
        raise ValueError("translation source-edition does not match source edition")
    source_rows = pairs(source, True)
    translation_rows = pairs(translation, False)
    sids = [row[0] for row in source_rows]
    tids = [row[0] for row in translation_rows]
    if sids != tids:
        raise ValueError("source/translation pair IDs or order differ")
    counts = {name: 0 for name in sorted(ALLOWED_FORMATS)}
    for _, metadata in source_rows:
        counts[metadata["format"]] += 1
    print("paired-text/2 valid")
    print("pairs:", len(source_rows))
    print("formats:", " ".join(f"{k}={counts[k]}" for k in sorted(counts)))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        print("PAIRED VALIDATION FAILED:", exc, file=sys.stderr)
        raise SystemExit(1)

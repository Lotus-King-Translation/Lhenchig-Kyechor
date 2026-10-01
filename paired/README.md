# Paired publication

The canonical reusable publication layer is:

- source.md
- translation.md

Both files share the same stable pair IDs in the same order.

Read ../FORMAT.md for the paired-text/2 specification.

Do not treat source anchors as translation segments automatically. Pair segmentation should be a coherent translation unit while retaining provenance back to the fixed golden object IDs.

Every source pair has one required structural field:

`format: prose | verse | h1 | h2 | h3`

The translation inherits that value by shared pair ID. This is the only reader-facing structural field in the paired-text format.

Validate with:

`python3 scripts/validate_paired.py`

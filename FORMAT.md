# Paired-text format

## Version

paired-text/2

## Purpose

The paired-text format is the reusable publication layer between a fixed golden source edition and one translation.

The canonical human-editable content files are:

- paired/source.md
- paired/translation.md

Everything else—JSON projections, bilingual views, token alignment, EPUB/PDF/HTML, search indexes—is generated or supporting material unless a project explicitly says otherwise.

## Core rule: the pair is the identity

Each coherent translation unit has one stable pair ID shared by both files.

Example relationship:

DTG-000001 source ⇄ DTG-000001 translation

Do not create separate source-segment and translation-segment IDs for ordinary cases.

A source pair may contain more than one underlying golden object when the English translation naturally spans them. Internal phrase or token alignment is a separate optional layer.

## Required front matter

source.md must declare at least:

- schema: paired-text/2
- text-id
- edition
- language

translation.md must declare at least:

- schema: paired-text/2
- text-id
- source-edition
- translation-edition
- language

The source-edition value in translation.md must identify the exact golden edition used.

## Pair marker

Use one deterministic HTML comment before each pair.

Recommended source marker:

<!-- pair: TEXT-000001 | golden: U00001 U00002 | role: main_text | format: verse -->

Recommended translation marker:

<!-- pair: TEXT-000001 -->

Projects may replace TEXT with a stable short work code.

The marker syntax must be parseable without rendering Markdown.

### Required format field

Each **source pair** must declare exactly one structural field:

`format: prose | verse | h1 | h2 | h3`

This is the minimal reader-facing structure.

- `prose` — ordinary prose/body text
- `verse` — verse/body text
- `h1` — level-1 heading
- `h2` — level-2 heading
- `h3` — level-3 heading

The source file is authoritative for `format`. The translation inherits it through the shared pair ID; do not duplicate it in `translation.md`.

For Kanava import this maps deterministically:

- `prose` → `type=prose`, `initial_formatting=body`
- `verse` → `type=verse`, `initial_formatting=body`
- `h1` / `h2` / `h3` → `type=prose`, `initial_formatting=h1/h2/h3`

A pair may not cross a format boundary.

## Pair-ID invariants

- Every pair ID occurs exactly once in source.md.
- Every pair ID occurs exactly once in translation.md.
- The pair-ID sequence is identical in both files.
- IDs are stable after a paired-text release.
- IDs are not renumbered because chapter headings or page breaks change.
- If future source segmentation changes materially, create a new paired-text edition and preserve lineage instead of silently reusing old identities.

## Source coverage

Every released golden reading object belongs to exactly one source pair.

No golden object may:

- be omitted
- appear in two pairs
- be silently normalized
- be reordered
- be replaced by translation-oriented wording

The source pair marker records the underlying golden object IDs.

Where a pair groups several objects, use their exact source order.

A validator must reconstruct the source projection deterministically from the pinned golden release.

## Translation coverage

Every source pair has one translation pair with the same pair ID.

The translation may contain:

- ordinary translated prose or verse
- a heading
- a bracketed interpretive supply
- an explicit unresolved marker
- an explicit non-translatable/source-graphic marker

It may not silently disappear because the source is difficult.

A translation pair may be syntactically freer internally than the source, provided the whole pair remains a faithful translation unit and any material uncertainty is annotated.

## Segmentation principle

Pair boundaries should represent coherent translation units rather than blindly mirror electronic source anchors.

Before translation begins, derive `paired/source.md` from the fixed golden release and assign every pair its stable ID, golden provenance, and `format`. Translation then fills the matching IDs in `paired/translation.md`.

Prefer grouping adjacent golden objects when:

- they form one coherent translation unit
- they have the same `format`
- a restored block is translated as one coherent unit

Always split at format changes between `prose`, `verse`, `h1`, `h2`, and `h3`, and at chapter/closing-material boundaries.

Avoid splitting a golden object unless there is a compelling documented reason.

Pair segmentation is editorial structure, not physical manuscript lineation. A grammatical sentence may continue across pair boundaries when structure requires it.

## Roles

Recommended role vocabulary:

- main_text
- source_heading
- chapter_colophon
- work_colophon
- restored_main_text
- source_annotation
- provisional_caption
- ritual_formula
- seal
- unresolved_inscription
- unresolved_source_graphic
- paratext

A project may extend this list, but role meaning must be documented.

Non-main roles still receive pair IDs when they belong to the released reading sequence.

## Notes

Translation notes should use normal Markdown footnotes or stable linked note IDs.

Each note that concerns source editorial history should retain:

- pair ID
- underlying golden object ID(s)
- exact source reading where relevant
- selected treatment
- uncertainty or evidence boundary

Do not duplicate a source annotation as main translation prose merely to keep it visible. Represent it as the correct role and attach the note to the corresponding pair.

## Chapter and section structure

Markdown headings may represent chapters and sections, but pair identity is independent of heading numbers.

The validator should check that all pair IDs remain in source order across headings.

Closing material remains explicitly closing material; do not invent a new chapter merely for convenience.

## Optional fine-grained alignment

Token or phrase alignment is optional and generated.

When used, follow the conceptual model proven useful in Kanava:

- lexical — overt source material corresponds to overt target material
- transliteration — source material is represented by transliteration
- target_grammar — target-language words are required grammatically without separate source lexical content
- source_implicit — source meaning/function has no separate overt target token
- punctuation — punctuation relationship

Many-to-many lexical alignment is allowed.

Do not force word-for-word alignment merely to achieve complete coverage.

A robust token alignment should ensure every non-whitespace token occurrence on each side belongs to exactly one alignment group.

## Validation requirements

A paired-text validator must reject:

- missing `format` on a source pair
- unsupported `format` value
- a pair that crosses a format boundary
- missing pair on either side
- duplicate pair ID
- pair order mismatch
- unknown golden object reference
- omitted golden object
- duplicated golden object coverage
- golden object order mismatch
- source text differing from the pinned golden release
- wrong source edition/version
- lost restored material
- lost closing material
- lost required note/reference
- unrecorded translation mutation when deriving from a fixed translation release

The validator should also report:

- pair count
- prose pair count
- verse pair count
- h1 / h2 / h3 pair counts
- golden objects covered
- restored objects/verses retained
- note count
- unresolved pair count
- closing-material coverage
- exact pinned source and translation versions

## Canonical files versus projections

source.md and translation.md are the canonical paired content.

Recommended generated/supporting outputs may include:

- paired/manifest.json
- paired/coverage.json
- paired/bilingual.md
- paired/alignment.json
- publication HTML/PDF/DOCX/EPUB

Generated files must say what canonical files and release versions produced them.

## Release

A paired-text release must pin:

- golden source release
- translation release
- paired-text schema version
- source.md hash
- translation.md hash

Release validation must prove exact pair symmetry and exact source coverage.

Once tagged, the pair IDs in that release are immutable.

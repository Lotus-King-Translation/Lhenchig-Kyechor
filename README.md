# Tibetan text project template

Organization template for projects that follow one controlled workflow:

1. **Bring the editions together.**
2. **Create a maintained golden Tibetan edition.**
3. **Segment the fixed golden edition into reader-ready pairs with `format: prose|verse|h1|h2|h3`.**
4. **Translate those fixed pairs.**

The repository is intentionally opinionated. Source witnesses, modern transcripts, editorial decisions, the golden reading, and translations remain separate provenance layers. A released golden edition is a maintained reading of an explicitly chosen governing witness; it is not presented as an infallible reconstruction of an original text.

## Start here

Agents and contributors must read [AGENTS.md](AGENTS.md) first.

The active method documents are:

- [Golden edition method](guidelines/golden_edition_method.md)
- [Tibetan–English translation and QC standard](guidelines/tibetan_translation_standard_v2.md)
- [Paired-text format](FORMAT.md)
- [Active glossary](glossary/expanded_tibetan_english_glossary.csv)

The current project state belongs in [PROJECT-STATUS.md](PROJECT-STATUS.md). Phase-specific continuation details belong in the relevant HANDOFF.md; do not rely on chat history as the only record of unfinished work.

## Repository structure

- editions/ — acquired scans, transcripts, and source register
- source/ — immutable imported/source copies
- diplomatic/ — golden-edition work, evidence, releases, and handoff
- translations/ — translation work, evidence, releases, and handoff
- paired/ — canonical paired source/translation files
- guidelines/ — active editorial/translation standards
- glossary/ — active eight-column terminology resource
- scripts/ — project validators/build helpers

Tracked empty subdirectories are included because they recur in every project.

## Completion model

Work is released in bounded, versioned stages. A chapter or section is not “done” because a script ran or a large number of pages were inspected. A release gate requires explicit scope, closed decision queues, preserved uncertainty, reproducible outputs, validation, signoff, a fixed tag, a publication receipt, remote SHA verification, and a clean tree.

Full scan proofreading, exhaustive manuscript collation, eclectic reconstruction, and new witness acquisition are separate research scopes unless a project explicitly adds them to its release contract.

## Paired source and translation

After a golden release is fixed, establish reader-ready source pairs before translation. Each source pair has one `format` value: `prose`, `verse`, `h1`, `h2`, or `h3`. Translate into the matching pair IDs in:

- paired/source.md
- paired/translation.md

Both files use the same stable pair IDs in the same order. See [FORMAT.md](FORMAT.md).

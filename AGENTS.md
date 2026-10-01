# Agent operating contract

This file is the mandatory entry point for every substantial task in repositories created from this template.

## 1. Startup: establish the exact state before editing

At the start of a turn or agent handoff:

1. Read this file.
2. Read PROJECT-STATUS.md.
3. Inspect git status, current branch, local HEAD, remote main, and relevant release tags.
4. If there is interrupted, untracked, or unpublished project work, preserve it on a recovery branch before cleanup, reset, regeneration, or synchronization.
5. Read the phase handoff:
   - edition/golden work: diplomatic/HANDOFF.md
   - translation work: translations/HANDOFF.md
6. Read the governing guideline for the task:
   - golden work: guidelines/golden_edition_method.md
   - translation/QC: guidelines/tibetan_translation_standard_v2.md
   - paired publication: FORMAT.md
7. Read editions/REGISTER.csv and all applicable source/provenance records.
8. Read the current plan, work queue, decisions, coverage, validation, and publication receipts for the exact section being changed.
9. Read DECISIONS.md and identify the latest explicit user-approved decisions. An assistant suggestion, old status paragraph, or majority reading is not automatically an approved decision.
10. Declare the finite task and its completion counts before substantive editing.

Do not begin from memory when the repository contains a newer saved state.

## 2. Three phases and their gates

The normal lifecycle is strictly ordered.

### Phase A — source intake

Bring together scans, transcripts, reprints, web transcriptions, catalog records, and other comparison material. Record provenance and hashes. Classify whether each item is a physical witness, a transcript of a witness, a derivative/reference transcription, a duplicate/reprint, or an unresolved lead.

### Phase B — golden Tibetan edition

Create and release a corrected reading under guidelines/golden_edition_method.md.

Do not begin translation of unreleased text. Translation may use only a fixed golden release unless the user explicitly authorizes a provisional exception.

### Phase C — translation

Before translating a fixed golden release, establish `paired/source.md` for that release with stable pair IDs, exact golden provenance, and one required structural field: `format: prose|verse|h1|h2|h3`.

Translate those fixed source pairs under the active glossary and translation standard into the matching IDs in `paired/translation.md`. Preserve all source-linked uncertainties and notes. The translation inherits `format` from the source pair; do not maintain a competing copy on the English side.

Do not start the next chapter or section while the previous section's required bounded release gate is still open.

## 3. Source authority and provenance

Always distinguish:

- physical scan, manuscript, or printing
- modern electronic transcript of that source
- normalized or reconstructed text
- related website/reference transcription
- source annotation, gloss, or heading
- editorial conjecture
- translation

Never treat filenames, matching wording, or repository location as proof that two files are independent witnesses.

Each acquired item must have a source-register entry and, where possible, an exact SHA-256. Do not overwrite archival originals. Derived files must say what they were derived from.

A hash proves file identity, not that an image crop belongs to the claimed textual anchor. Evidence allocation must be checked separately.

## 4. Golden-edition non-negotiables

The golden edition is a maintained reading of an explicitly selected governing witness. It is not an eclectic reconstruction unless the project explicitly changes scope.

- Freeze a stable source-anchor system before editorial work.
- Never renumber stable source anchors merely because text is restored.
- Preserve exact supplied transcript strings separately from corrected readings.
- No silent Unicode normalization, spelling repair, punctuation repair, arithmetic repair, Sanskrit repair, doctrinal harmonization, or source-layer flattening.
- Separate main text from smaller annotations, variants, headings, captions, seals, graphics, and colophons when the evidence supports that distinction.
- Restored or scan-only material gets its own IDs and provenance.
- Null or empty transcript readings mean absence in that transcript, not proven omission from its physical exemplar.
- Unreadable, missing, uncollated, omitted, conjectured, and uncertain are distinct states.
- A related transcript or website is not promoted into an independent witness without evidence.

For scan evidence, inspect the native image directly. OCR may be used only as a locator or last-resort aid and is not itself evidence for a reading. Preserve exact image provenance and accepted/excluded evidence allocation.

## 5. Avoid the work patterns that cause endless spinning

Before substantive golden-edition work on a chapter or section, freeze a finite release contract containing:

- exact anchor range and boundaries
- exact electronic difference count and readable loci
- related-reference conflict blocks
- a finite set of targeted scan/source checks
- required interventions and restorations already known
- defined deliverable groups
- final validation, signoff, and publication gate

Do not replace this with “keep scanning until confident.”

Electronic collation should locate differences mechanically. Human/editorial effort should then focus on the frozen loci, structural anomalies, missing spans, major differences, headings/layers, and explicitly chosen source checks.

If a historical page hint or exploratory crop is wrong, preserve it as excluded or mislocated evidence. Never promote a convenient crop because its pixels or hash happen to match an image file.

Once all frozen queues are closed, package and release. Exhaustive witness work remains a separate research program unless explicitly included in the contract.

## 6. Editorial decisions

Every nontrivial decision must preserve:

- stable locus or anchor ID
- exact competing strings
- selected treatment
- reason
- evidence paths
- remaining uncertainty
- whether the decision changes main text, source layer, punctuation, or display only

A mechanical alignment result is not an editorial decision.

Do not count an electronic witness as agreement when its relevant span has not been checked or reconstructed.

Where comparison texts are represented by patches or differences, validate reconstruction by at least two paths when practical, for example minimal-difference and whole-locus reconstruction.

## 7. Translation and QC

At the start of translation or QC, read the active combined standard and the full relevant glossary rows, including status and provenance columns.

The golden Tibetan governs what the passage says. The glossary governs established English terminology. Neither can be used to silently override the other.

Translation self-check and independent QC are different activities. Do not label the translator's own review independent QC.

Do not silently activate proposed glossary alternatives. New usages remain proposed until explicitly approved.

Every substantive golden segment must have English or an explicit unresolved or non-translatable marker. Every substantive English addition must be source-supported, glossary-supported, ordinary target-language grammar, or explicitly disclosed.

## 8. Paired-text publication

The reusable canonical publication surface is:

- paired/source.md
- paired/translation.md

Both use identical stable pair IDs and order. The pair, not a word token, is the primary identity. One pair may contain multiple golden source objects when that is the coherent translation unit.

Every source pair must declare exactly one `format`: `prose`, `verse`, `h1`, `h2`, or `h3`. A pair may not cross a format boundary. The English side inherits the value through the shared pair ID.

Every golden reading object must map to exactly one pair. Nothing may overlap or disappear.

Fine-grained token alignment is optional and generated; it is not required to clutter the two canonical files. If implemented, prefer explicit relationship kinds such as lexical, transliteration, target grammar, source implicit, and punctuation rather than pretending all alignment is word-for-word.

See FORMAT.md.

## 9. Status, handoff, and “nothing slips through the cracks”

After every substantive batch update the saved project state, not just chat.

At minimum, the current status and handoff must state:

- exact phase and section or chapter
- governing source edition and release/tag if any
- completed and remaining decision counts
- completed and remaining targeted source checks
- restored and changed anchor counts
- unresolved readings and evidence paths
- deliverable groups completed and remaining
- validation and negative-test state
- whether full scan proofreading was performed
- whether exhaustive witness collation was performed
- next finite task
- whether the next chapter or phase has started

Historical status text must not override the current top-level status.

Do not report accuracy percentages derived from counts.

## 10. Remote preservation

Commit and push every substantive batch before starting the next one.

- Stage files explicitly.
- Use small, meaningful commits.
- Only the coordinating agent publishes or releases.
- Verify the remote branch SHA after every checkpoint.
- If push fails, stop substantive work and preserve locally or recovery-first.
- Do not end a turn with valuable unpublished changes.
- Never commit credentials, secrets, unrelated personal data, caches, or dependency directories.

Use scripts/checkpoint.py for normal staged checkpoints when practical. Each checkpoint report should include fixed completed and remaining counts and the verified remote SHA.

## 11. Release gate

A bounded release is complete only when all required items pass:

1. frozen editorial and source queues closed
2. required reading, apparatus, machine, coverage, and change deliverables built
3. reproducible build passes
4. exact source preservation and reconstruction checks pass
5. relevant links and evidence hashes validate
6. prior fixed releases remain unchanged
7. negative corruption tests reject bad fixtures
8. unsigned final-mode gate rejects before signoff, where supported
9. explicit final review and signoff are recorded
10. final-mode validation passes
11. annotated version tag is pushed
12. remote tag object and peeled commit are verified
13. publication receipt is committed after the fixed tag
14. remote main verification passes
15. working tree is clean

A receipt committed after a release tag must not move the fixed tag.

Always distinguish bounded release complete from all possible witness research complete.

## 12. Generated versus authored files

Document which files are authored inputs and which are generated outputs. Do not hand-edit generated files unless the project explicitly defines them as canonical authored artifacts.

Run read-only validation before regeneration when resuming after interruption.

When a tool, script, or schema is changed, rerun the validation and negative tests that protect the affected outputs.

## 13. Claims and uncertainty

State exactly what was checked.

Do not claim:

- complete scan proofreading if only targeted pages were inspected
- exhaustive collation if witnesses or spans remain outside scope
- successful decipherment when wording remains uncertain
- independent human palaeographic certification for agent inspection
- semantic translation certification from structural validation alone

Preserving an unresolved reading visibly is a successful editorial outcome when the evidence does not support resolution.

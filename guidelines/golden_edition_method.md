# Golden edition method

## Purpose

This method turns a set of acquired editions into one maintained Tibetan reading suitable for translation, while preserving the evidence needed to audit every substantive editorial choice.

“Golden edition” means the project's maintained reading of an explicitly selected governing witness. It does not mean an infallible text, a reconstructed archetype, or a majority-vote eclectic edition unless the project explicitly adopts that different goal.

The method is optimized to finish reliable bounded releases without drifting into endless scan reading or witness acquisition.

## 1. Register sources before editing text

Build editions/REGISTER.csv before collation.

For every item record:

- stable source ID and siglum
- physical witness or modern transcript
- title and provenance
- repository path
- governing, comparison, reference-only, duplicate, or unresolved role
- claimed exemplar, if any
- independence status
- SHA-256 when locally stored
- licensing or attribution constraints
- notes on completeness and chapter mapping

Do not infer witness independence from file names, matching catalog labels, or different download locations.

A web transcription of the governing printing is a useful reference but is not a new independent witness.

## 2. Choose the governing base explicitly

Before producing a golden reading, identify the physical witness that governs the edition.

Keep distinct names for:

- base scan
- base electronic transcript
- comparison transcripts
- other physical witnesses
- reference transcriptions

The base scan governs corrections to the base transcript. Comparison witnesses inform the apparatus and may motivate checks, but they do not override the governing witness because they are smoother, more grammatical, or in the majority.

If the project wants an eclectic critical text instead, write a new method and release contract rather than silently changing this rule.

## 3. Freeze stable source anchors

Create stable source anchors from the supplied electronic base before substantive correction.

Requirements:

- unique IDs
- source order fixed
- exact original strings preserved
- exact character offsets preserved where practical
- no silent Unicode normalization
- restorations and scan-only insertions receive separate IDs
- existing source-anchor IDs are never renumbered merely because something is inserted

Source anchors are electronic locators, not claims about physical manuscript lineation.

## 4. Establish chapter or section boundaries

Before collation, fix the bounded section under review.

Record:

- first and last anchor
- exact source offsets
- corresponding scan page/image range where known
- corresponding ranges in each electronic comparison source
- opening and closing headings or colophons
- uncertainty in the boundary itself

Do not begin the next section until the current section's release gate is closed.

## 5. Freeze a finite release contract

This is the step that prevents endless spinning.

Before substantive editorial review, produce a plan containing:

- exact anchor count
- exact electronic differences
- readable difference loci
- related-reference conflict blocks
- finite targeted scan/source checks
- known interventions or suspected missing spans
- deliverable groups
- validation requirements
- final signoff/tag/receipt gate

The plan must include fixed completed/remaining counts.

A bounded release may explicitly leave broader witness collation, decorative sign decipherment, full punctuation proofing, or untargeted scan review outside scope.

Do not substitute “read until satisfied” for a finite plan.

## 6. Mechanical electronic collation first

Use exact electronic comparison to find where attention is needed.

Recommended properties:

- exact source slices
- monotonic alignment
- no Unicode normalization
- exact difference IDs
- readable whole-locus records
- minimal patch records where useful
- additions, omissions, and transpositions represented explicitly

When comparison texts can be represented as transformations of the base, verify that each comparison text reconstructs exactly from the base plus the apparatus.

Prefer two independent reconstruction paths where practical, such as:

- minimal-difference reconstruction
- whole-locus reconstruction

Mechanical agreement is not proof that a physical witness agrees. It only says the supplied electronic strings agree.

## 7. Target scan review instead of broad wandering review

Freeze a finite list of scan checks selected from:

- large or semantically important differences
- suspected missing verses
- broken or implausible base-transcript strings
- headings or colophons embedded in main text
- likely small-print annotations or variants
- chapter boundaries
- punctuation/sign questions that affect text allocation
- loci where comparison witnesses strongly disagree
- structurally important numerals or lists

Inspect native source images directly.

OCR may help locate material, but OCR output is not evidence for a reading.

For every accepted image/crop record:

- source image/page
- original image hash
- exact crop coordinates if cropped
- target anchor/locus
- why the crop is associated with that locus

Exploratory or mislocated crops remain preserved but explicitly excluded from accepted evidence.

A matching file hash proves image identity, not anchor association.

## 8. Separate textual layers

One of the most important recurring tasks is distinguishing:

- main root text
- source heading
- small gloss
- reported alternative
- correction note
- colophon
- seal
- caption
- unresolved graphic
- ritual formula
- modern editorial insertion

Do not flatten all visible source material into one running root-text string.

When a base e-text interleaves a smaller note inside a main verse, preserve the original e-text string in the apparatus and select the scan-supported main line separately.

If the exact smaller-note wording or substitution scope remains uncertain, preserve that uncertainty.

## 9. Editorial dispositions

Every frozen locus must end in an explicit disposition.

Typical dispositions:

- retain base
- adopt scan-supported correction
- restore scan-attested main text
- separate source annotation from main text
- classify heading or colophon
- retain with explicit uncertainty
- defer outside bounded scope

Each decision records:

- stable ID
- exact base string
- exact comparison strings
- selected reading or role
- rationale
- evidence
- remaining uncertainty
- whether original anchor text changes

Never silently choose a comparison witness because its grammar is better.

Do not repair arithmetic, Sanskrit, odd syntax, or doctrinal content unless the governing source evidence supports the repair.

## 10. Restorations

A restoration enters the golden main reading only when the governing source supports it.

Requirements:

- separate restoration ID
- placement after/before stable anchors
- exact source image evidence
- exact Tibetan transcription
- reason for treating it as main text
- display/punctuation policy
- remaining uncertainty

Comparison transcripts may corroborate a restoration but do not replace governing-scan evidence.

## 11. Keep uncertainty first-class

Use distinct states for:

- unreadable glyph
- uncertain punctuation
- uncertain word division
- source note with uncertain scope
- missing scan leaf
- supplied transcript omission
- genuine witness omission
- uncollated witness span
- conjecture
- unresolved graphic

Do not turn any of these into “agreement.”

Do not invent wording for a graphic or compressed sign group merely to make the edition look complete.

## 12. Required bounded release outputs

A section release should normally include:

- readable golden text
- machine-readable reading sequence
- comparative apparatus
- related-reference comparison where used
- source-review/evidence records
- changes from supplied base transcript
- coverage and retained uncertainty
- build manifest
- final validation
- final editorial review

Project-specific names may differ, but the information may not disappear.

## 13. Validation

Validation should prove structural and provenance claims, not invent an “accuracy percentage.”

At minimum validate:

- all original anchors preserved and ordered
- every frozen comparison decision represented
- restorations placed exactly once
- source annotations layered correctly
- exact source strings retained
- electronic comparison reconstruction
- accepted evidence hashes
- local links
- prior fixed releases unchanged
- build reproducibility
- explicit false flags for work not performed, such as full scan proofreading or exhaustive witness collation

Add negative tests that deliberately corrupt anchors, roles, restoration placement, evidence links, or coverage flags and ensure the validator rejects them.

Where supported, final-mode validation should reject an unsigned candidate before signoff.

## 14. Release and publication

A release is not complete at the commit.

Required sequence:

1. close the finite decision/source-check queues
2. build candidate
3. validate candidate
4. run negative tests
5. record final editorial review
6. record source-bound signoff
7. run final-mode validation
8. commit release content
9. create annotated version tag
10. push tag
11. verify remote tag object and peeled commit
12. write publication receipt on main
13. verify remote main
14. verify clean tree

The publication-receipt commit is allowed to be later than the fixed release tag. It must not move the tag.

## 15. Chapter-by-chapter progression

For long works, release one bounded section at a time.

The next section begins only after the previous section has:

- closed decision counts
- closed targeted source checks
- complete deliverables
- passed tests
- final signoff
- fixed tag
- publication receipt
- clean remote verification

This creates a monotonic sequence of trustworthy releases and prevents later work from destabilizing earlier chapters.

## 16. What this method deliberately avoids

Do not let bounded publication be blocked indefinitely by:

- acquiring every conceivable witness
- reading every scan page without a frozen question
- trying to resolve every decorative sign
- redoing already completed lexical passes
- treating historical “exhaustive” plans as current release requirements
- collapsing transcript and physical-witness evidence
- trying to reconstruct an unattested ideal original
- starting later chapters while earlier release queues remain open

Those may all be legitimate later research projects. They are not automatically prerequisites for a useful, auditable golden v1.

## 17. Status language

Use precise claims such as:

- “bounded golden v1 complete”
- “targeted base-scan checks complete”
- “electronic A/B/S collation complete”
- “full base-scan proofreading not performed”
- “exhaustive witness collation not performed”

Do not convert counts into an accuracy percentage.

A visibly unresolved reading is better than an unsupported confident correction.

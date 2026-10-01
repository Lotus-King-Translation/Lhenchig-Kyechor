# Independent translation QC

All 110 pairs / 589 source lines were read against the new English under standard v2.0 by an agent other than the translator of that partition. This is independent agent review, not independent human certification.

| Scope | Translator | Independent reviewer | Report | Dispositions | Applied-fix verification |
| --- | --- | --- | --- | --- | --- |
| A: pairs1–39 /lines1–191 | source_audit | translate_c | [A](review-A.json) | [A](disposition-A.json) | [A](verification-A.json) |
| B: pairs40–74 /lines192–392 | translate_b | source_audit | [B](review-B.json) | [B](disposition-B.json) | [B](verification-B.json) |
| C: pairs75–110 /lines393–589 | translate_c | translate_b | [C](review-C.json) | [C](disposition-C.json) | [C](verification-C.json) |

Eight English wording changes were accepted: five in B, two in A, and one explicitly bracketed conjectural interpretation in C. Five new source/usage notes address documentation gaps. Existing source questions remain visible; dispositions do not authenticate a corrected Tibetan reading. Root also attached seven missing reference-note links and corrected one exact quotation’s unattested headword-final tsheg.

Input names `work/translation-X.json` in reports refer to the unchanged published snapshots at `../drafts/partition-X.json`. Their byte hashes preserve the reviewed draft. Verification files compare the final affected text and publish per-pair hashes; whole-file hashes in a verification describe its moment in the coordinated workflow, since other partitions were subsequently updated. The final signoff pins the combined artifacts.

The [30 guideline fixtures](regression-fixtures.json) include actual-draft checks and explicitly synthetic boundary exercises. Twenty-nine exercises passed at their declared scope; R26 was not tested because the original disrupted song was unavailable. R02/R04 passed synthetic boundaries only; their historical source applications were not tested. These are limited artifact checks, not performance estimates. The [23 corruption tests](../validation/release-negative-tests.json) separately protect source, glossary, pairing, notes and final-signoff requirements.

Physical-witness proofreading, exhaustive collation and final human scholarly approval were not performed.

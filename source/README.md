# Source and reference

`archive/` contains unchanged legacy files pinned to commit 396428b4d94b446448db9460185c554e696c181a. `archive/root/001.txt` governs this provisional translation. No golden edition or physical witness has been established. The source colophon calls its compiler the wanderer Dor Gyal; Phagmodrupa is the legacy repository attribution, not a historical identification independently verified here.

The legacy script inserts ASCII spaces as token boundaries, uses U+2423 `␣` inside affixed particles, and replaces original spaces with U+1680 ` `. Decode by deleting ASCII spaces and U+2423, then replacing U+1680 with ordinary spaces. This recovers 588 lines byte-for-byte as Unicode strings and all 589 modulo the trailing ASCII space at L0493, removed by the legacy script’s strip operation. The raw root file avoids any lossy reversal. `001_v2.txt` differs from it only by a final newline.

Repeated vowel marks, missing tshegs and suspicious spellings already occur in the raw transcript: they are not token markers and are not silently repaired. Notes disclose interpretive readings. `reference.json` maps all 589 PO contexts and human English entries to exact source lines by context ID (a mechanical association, not a claim of semantic alignment); none is blank, which establishes reference presence, not translation quality. The old English remains reference only.

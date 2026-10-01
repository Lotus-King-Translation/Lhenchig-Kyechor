# Project-owner decisions

## D001 — Direct translation, 2026-10-01
The user explicitly instructed: “skip the golden edition phase, and go straight to translating.” The complete supplied work is one bounded translation batch, with parallel drafting partitions rather than separate chapter releases. Use a fixed provisional transcript; do not represent it as a golden edition.

## D002 — Source and reference roles, 2026-10-01
The user instructed us to remove the legacy Tibetan formatting and produce the template’s paired source and translation. The rough human English is optional reference, not governing English. The current template standard and unchanged glossary govern translation. Mechanical recovery does not authorize silent spelling repairs.

## Implementation decisions
- Repository name: Lhenchig-Kyechor, the source title in the existing organization’s spelling and hyphenated title convention; the legacy Phagmo-Lhenchig-Kyechor remains intact.
- Governing input: exact archived root/001.txt at the supplied branch commit, the pre-tokenization source used by the legacy scripts.
- Stable line anchors L0001–L0589. Pair code LCK; coherent verse units retain original line order.
- The paired marker uses `source:` for provisional line anchors, replacing the misleading `golden:` label. This scoped schema adaptation is documented in FORMAT.md and validated.
- Uncertain readings remain in Tibetan unchanged and receive source-linked translation notes. Final human approval is not implied by an agent-reviewed working release.

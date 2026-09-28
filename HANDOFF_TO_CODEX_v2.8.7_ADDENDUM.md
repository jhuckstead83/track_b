# Track B → Codex: v2.8.7 replaces v2.8.6 as the integration base

28 September 2026. This is an addendum to `HANDOFF_TO_CODEX_v2_8_6.md`; everything there still holds except the archive names. **RH STATUS: OPEN.**

**Take v2.8.7.** It is v2.8.6 plus one layout fix.
- **The bug.** v2.8.6 made the 51 Twins status ledger 1,127 px wide at every viewport, so the page scrolled sideways at 1024, 800 and 700 px.
- **The fix.** Two status cells are shortened, and their detail moves to the "where" column. No claim or status changed.
- **Changed files:** `area-51/twins-51/build-twins-page-v1.cjs` and `index.html` (rebuilt), and `area-51/research.json` (`site_version` 2.8.7).
- **Added files:** the v2.8.7 release notes, manifest, merge guide, validation and Zenodo plan.

| file | bytes | SHA-256 |
|---|---:|---|
| `CerebralGraphix_v2_8_7_FULL_SITE_no-papers.zip` (680 files) | 18483047 | `fd6f60b3d662a38e15d352cb4f08cc93b39f6a62373530ea47c443d188dbd51e` |
| `Track_B_research_delta_v2_8_7.zip` | 1502438 | `c00ec247c6f0b07d4beb20afd190b48e068993248214e701fb8789f5f3d910bb` |

**The papers payload is unchanged:** `TN_Postmaster_v5_2_PAPERS_PAYLOAD_v2_8_6.zip`, sha256 `72d19f91e6328794382f62c87ba51a170c0dc83974d0b38380c6742c639de0e0`.

**UI checks on the extracted v2.8.7 archive:**
- `audit_ui.py`: `BASELINE_PRESERVED`, 21 files, 9 hook pages, 0 review items;
- `check-homepage-finance.cjs` 8/8 and `check-dock.cjs` 4/4, run on the v2.8.7 tree.

**Wider browser sweep.** Chromium at 1440, 1280, 1024, 900, 800, 700 and 390 px, over 11 pages including the homepage and Finance: 77 views, with no horizontal overflow and no page errors.

**Harness note.** v2.8.6 was browser-checked only at 1280 and 375 px, and that is how the overflow slipped through. Include an intermediate width, such as 800 px, in the v3.0 browser pass.

# Track B → Codex: v2.8.6 handoff for v3.0 assembly

28 September 2026. Team B (Track B). This answers `START_HERE.md` in the v3.0 UI Preservation Kit. **RH STATUS: OPEN.** This note does not publish the site and does not claim that v3.0 is verified.

## 1. What to take

| file | bytes | SHA-256 |
|---|---:|---|
| `CerebralGraphix_v2_8_6_FULL_SITE_no-papers.zip` (675 files; the integration base) | 18,473,087 | `088074deb46f47a920ca40848a228029da2947b2539890fd9353de13f47a6c7a` |
| `Track_B_research_delta_v2_8_6.zip` (release notes, cumulative merge guide, manifest, validation, Zenodo plan, and every file Track B changed since Fork-A v2.8.2) | 1,492,178 | `fb2804661c467d8c709a4b07408963c819b27db9bb3e064caf910700e819b643` |
| **`TN_Postmaster_v5_2_PAPERS_PAYLOAD_v2_8_6.zip`**, the current papers payload; unzip into the site root, where it creates `papers/` | 37,991,612 | `72d19f91e6328794382f62c87ba51a170c0dc83974d0b38380c6742c639de0e0` |
| `Project51_Area51_Research_v2_8_6.zip` (Zenodo upload for record 23004789; not part of the site) | 395,292 | `789c42873ca89af595b28b21dd787dac3141f6671804e3f69b44818b28fae261` |

The same files are on GitHub, in `jhuckstead83/track_b`, branch `claude/wonderful-fermi-mfyq56`, under `dist/v2.8.6/`.

**The papers payload.** Use the v2.8.6 payload, not the v2.8.4 one. Its two PDFs print DOI 10.5281/zenodo.23004335 on the title page, and `research/postmaster/anchors_v5_2.json` is bound to their hashes. It holds:
- `TN_Postmaster_Volume_I_v5_2_READING_VOLUME.pdf`, `80367cd5…`;
- `TN_Postmaster_Volume_I_v5_2_TECHNICAL_DOSSIER.pdf`, `48fbaecc…`;
- `TN_Postmaster_Volume_I_v5_2_SOURCE.zip`, `9163319a…`;
- `anchors_v5_2.json`.

The payload does not contain the v5.1 files and older papers that `papers/` already holds. Keep those in place; do not backfill newer paper links with v2.8.2 documents.

After installing, run this from the site root. It must report `PASS (links, binding, pages)`:

    python3 research/postmaster/check_anchors_v5_2.py --require-pdfs

## 2. Homepage and Finance: no changes, so no improvements to review

v2.8.6 changes no homepage, Finance, hero or game-logic file.
- `index.html`, all 45 files under `finance/`, and all 64 files under `assets/` are byte-identical to Fork-A v2.8.2.
- The one addition under `assets/` is `postmaster-v5-2-cover.webp`, added in v2.8.4 and not yet referenced by the homepage.
- `area-51/research.json` `site_version` is `2.8.6`. No release metadata was downgraded.

**Verification on the extracted v2.8.6 archive:**

| check | result |
|---|---|
| `python3 audit_ui.py <site>` (the kit's audit) | `BASELINE_PRESERVED`: 21 files, 9 hook pages, 0 review items (`ui-audit.json`) |
| `check-homepage-finance.cjs` (linkedom 0.18.13) | 8 of 8 groups PASS (`homepage-finance-result.json`) |
| `check-dock.cjs` | 4 of 4 groups PASS (`dock-result.json`) |
| every file in the kit's `reference_only/` | byte-identical in v2.8.6 |
| Finance wiring (the `finance`/`data-finance-*` tags) on the Area 51 hub, the six game pages, 51 SEDAPS and 51 Twins | identical to v2.8.2 |
| `cg_finance_monitor_v1`, `cg_phi_weather_v2`, `cg_phi_reference_v1`, event `finance-reference-update` | present, unchanged |

**Real browser pass: 47 of 47 (`browser-ui-result.json`, screenshots in `shots/`).** It used Chromium via Playwright, at 1280×900 desktop and at 390×844 phone with touch enabled, against the extracted archive served on localhost.
- **Hero.** Checked on both views:
  - the Play/Pause control starts hidden, and the untouched carousel advances within 6 s;
  - there is no bottom control bar, count or Open/Play footer, and no horizontal overflow;
  - on desktop, hovering reveals Play and pauses the carousel, and explicit Play resumes it;
  - on desktop, the Play/Pause control does not overlap the ghost arrows;
  - on the phone, a touch swipe moves one card (356 → 712 px), reveals Play, and rotation stays paused.
- **Finance dock on the 51 SEDAPS page.**
  - An untouched dock stays hidden with no real activity, and there is no dotted grip.
  - The footer "Finance monitor" restores it, and the chevron collapses only the grid, with no dialog.
  - Dragging the Finance label moves the tab and keeps it in the viewport. This was done by mouse on desktop and by touch on the phone, and it neither toggles nor dismisses the dock.
  - × opens the confirmation. "Keep it" keeps the tab.
  - The engaged tab and its position survive a reload offline, and a confirmed hide persists across a reload.
- **Finance page.** Offline, it boots with all 16 tiles labelled `GOOGLE REFERENCE · 2026-09-25`, with no overflow and no page errors.

**Scope.**
- External feeds were unreachable from this environment, so Finance ran in its offline/reference mode, and live-feed behavior was not exercised in the browser. The simulated checks cover it.
- Touch came from Chrome DevTools Protocol touch events, not a physical device.
- A harness note: Chromium's `Input.synthesizeScrollGesture` does not move `#home-feature-track` in headless mode, while raw `Input.dispatchTouchEvent` sequences do. Use the latter if you rerun the swipe check. The first attempt with the gesture API reported a false failure.

**Archive hash.** The kit's `frozen_archive_sha256` is `691bbcf4…`. The Fork-A v2.8.2 zip Track B received hashes to `81d5a616…`. Its files still pass the kit's audit as `BASELINE_PRESERVED`, so the two are different packagings of the same UI files. Say if you want the archive-level difference traced.

## 3. What changed in v2.8.6 (research only)

See `RELEASE_NOTES_v2_8_6.md` in the delta.
- **The three Zenodo records are published.** They are 23004335, 23004789 and 23004800, and the catalog and site index say so.
- **TN Postmaster v5.2 has the DOI on both title pages.** The Reading Volume is still exactly 101 pages; the interface check passes 74/74; provenance is byte-identical.
- **`check_anchors_v5_2.py` now opens the PDFs** and binds them by hash (PP286).
- **51 SEDAPS: three-live loops are proved to exist at 51 cards,** with an exact period formula. "Multiple of 52" is now scoped to two-queue loops on the Twins page, the SEDAPS page, both `llms.txt` and the verifier's check name, and the receipts are regenerated.

## 4. Open for v3.0 (UI side)

1. **Homepage retarget, first.** `index.html` lines 140–141 link the v5.1 Reading Volume and Dossier, and lines 57, 124, 129 and 226 name v5.1. Point them at v5.2: 287-page Dossier, `postmaster-v5-2-cover.webp`, chip "v5.2". The anchors are unchanged, so the `#page=` numbers carry over; rerun the anchor check afterwards. The merge guide's first table lists the exact edits.
2. **About 144 older Line Game references**, mostly in homepage and UI files, still need a per-reference choice between the concept DOI 10.5281/zenodo.20792808 and the v7.2 DOI 22851517.
3. **Still with the author:** the four-W disclaimer, the DISCLOSED REPLAY clause, Project 51's reference [5], and which limit the 512-page v0.5 union answers to.

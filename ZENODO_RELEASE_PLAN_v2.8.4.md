# Zenodo plan for v2.8.4: records, files, cross-links, placeholders

This plan supersedes `ZENODO_RELEASE_PLAN_v2_8_3.md` and `ZENODO_RELEASE_PLAN_v2_8_0.md`, which are kept as released. What changed: record 1 now deposits the built PDFs in its first version. **No DOI in this release was invented.**
- Every link still waiting for a DOI carries `data-doi-pending="…"` in the page source. Search for that attribute, paste the DOI you mint next to it, and the site is cross-linked.
- The DOIs already cited are:
  - the TN Postmaster concept DOI 10.5281/zenodo.21968915, and v5.1 = 10.5281/zenodo.22844194;
  - The Line Game v7.2 = 10.5281/zenodo.22851517 and v7.5 = 10.5281/zenodo.22943070 (concept 10.5281/zenodo.20792808);
  - Project 51 v0.4, with Telescope 51 v0.7 and the Formula 51 concise method, = 10.5281/zenodo.22985771 (concept 10.5281/zenodo.22862811).
- The last three come from the Blue Team's DataCite check (PP270) and the record archives you supplied. Zenodo was not reachable from this session, so open each landing page once before the upload.

## Records to mint

| # | Record | Mint as | Upload | Placeholder id |
|---|---|---|---|---|
| 1 | TN Postmaster Volume I v5.2 | new version under concept 10.5281/zenodo.21968915 | the three files of the v2.8.4 papers payload: `TN_Postmaster_Volume_I_v5_2_READING_VOLUME.pdf` (101 pp), `TN_Postmaster_Volume_I_v5_2_TECHNICAL_DOSSIER.pdf` (287 pp) and `TN_Postmaster_Volume_I_v5_2_SOURCE.zip`, whose `qa/BUILD_BINDING.json` binds both PDFs by SHA-256 | `tn-postmaster-v5-2` |
| 2 | 51 SEDAPS v0.4.1 research update | new version of the 51 SEDAPS record, or a new record if the v0.1 note has none | the files below | `sedaps-51-v0-4-1` (was `sedaps-51-v0-4`) |
| 3 | 51 Twins v1: exact still plates and twin calibration | new record | a zip of `area-51/twins-51/` | `twins-51-v1` |
| 4 | Formula 51: uniqueness by deduction | new version of the Formula 51 Concise Method record, or a new record | `research/project-51/formula51/` without `__pycache__/` | `formula51-deduction` |
| 5 | Cerebral Graphix site v2.8.4 (optional) | new version of the site record, if you keep one | the full site zip | none |

**Files for record 2**, all in `area-51/sedaps-51/`:
- `RESEARCH_UPDATE_v0_4_1.md` (new results and the §1.1 proof) and `RESEARCH_UPDATE_v0_4.md` (corrected);
- `past10-certificates-v0-4-1.json`, `verify-past10-v0-4-1.cjs`, `VERIFY_v0_4_1.json`;
- `count-histories-v0-4-1.cjs`, `HISTORY_COUNTS_v0_4_1.json` (exact history counts);
- `independent/` (Python replay, census programs, receipts);
- `sedaps-lemma-v0-4.js` (scope clause in the header), `sedaps-v0-4.js`, `verify-sedaps-v0-4.cjs`, `VERIFY_v0_4.json`, `dstart4-certificates-v0-4.json`;
- the inherited `sedaps-core-v0-2.js` and `reachable-certificate-v0-3.json`.

## Cross-links (Zenodo "related identifiers")

- **1 → 3:** isSupplementedBy. **3 → 1:** isSupplementTo. The plates and the calibration report draw on Dossier §§69A–69B.
- **2 → 3:** isSupplementedBy. **3 → 2:** references. Plates II–IV draw on SEDAPS v0.4.1.
- **2 → Spivey, *Cycles in War*, INTEGERS 10 (2010) #G02:** references. It is the source of the alternation theorem behind the period formula.
- **3 → Project 51 v0.4 (10.5281/zenodo.22985771):** references, for plate V.
- **3 → Volume I: Exact Geometry and Symbolic Foundations** (your existing DOI): references. The trapped tip is used only as a drawing device.
- **4 → Project 51 v0.4 (10.5281/zenodo.22985771) and Line Game v7.5 (10.5281/zenodo.22943070):** references.
- **1 → arXiv:2608.13637 and arXiv:2609.02882:** references. These are reference entries [121] and [66].
- **1 → TN Postmaster Research Volume I v0.5 (10.5281/zenodo.21968858):** isNewVersionOf is already implied by the concept; no extra link is needed.

## Pasting the DOIs into the site

1. **Postmaster page.** In `research/postmaster/index.html`, the v5.2 source link carries `data-doi-pending="tn-postmaster-v5-2"`. Add the DOI next to it. The page's reading links already point at the v5.2 PDFs (v2.8.4).
2. **SEDAPS page.** In `area-51/sedaps-51/index.html`, the link to the current research update carries `sedaps-51-v0-4-1`.
3. **51 Twins page.** The page is generated. Edit the "Cite" line in `area-51/twins-51/build-twins-page-v1.cjs` (`twins-51-v1`), then run `node area-51/twins-51/build-twins-page-v1.cjs --write`. Editing `index.html` by hand makes the build check report it as stale.
4. **Project 51 page.** In `research/project-51/index.html`, the deduction link carries `formula51-deduction`.
5. **Manifest.** Refresh the hashes of any file you edit in `MANIFEST_v2_8_4.json`, or regenerate it.

## Before record 1: the v5.2 PDFs are built

The PDFs in the v2.8.4 papers payload were built on 28 September with pandoc 3.1.3 and TeX Live 2023: Reading Volume 101 pages, Technical Dossier 287 pages, no undefined references, no missing characters, and no overfull box over 30 pt. In the same environment the v5.1 Reader rebuilds to its recorded 101 pages. `qa/check_v52_interface.py` passes 74/74 with the build receipts. To rebuild them independently, put the v2.8.4 source zip in My Drive and run this Colab cell. It uses pandoc 3.1.3, the version the v5.0 build used. `build_baseline_v51.py` rebuilds v5.1 in the same environment, so the page count is compared like for like:

```python
from google.colab import drive; drive.mount('/content/drive')
!unzip -q -o "/content/drive/MyDrive/TN_Postmaster_Volume_I_v5_2_SOURCE.zip" -d /content
%cd /content/TN_Postmaster_Volume_I_v5_2
!wget -q https://github.com/jgm/pandoc/releases/download/3.1.3/pandoc-3.1.3-1-amd64.deb && dpkg -i pandoc-3.1.3-1-amd64.deb > /dev/null
!apt-get -qq update && apt-get -qq install -y texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra texlive-lang-english lmodern > /dev/null
!pip -q install pymupdf
!python qa/build_release.py both
!python qa/build_baseline_v51.py reading
!python qa/check_v52_interface.py
```

Once the build receipts exist, `check_v52_interface.py` enforces the Reader's 101-page ceiling. The Blue Team has asked whether that ceiling should be 99; that decision is yours and is unchanged here. The Track B edits add a few source lines to the Reader, so read its page count from the build receipt.

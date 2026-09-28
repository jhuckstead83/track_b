# TN Postmaster Volume I -- v5.2 (source package)

This package holds the two companion volumes as editable Markdown masters:

- `src/TN_Postmaster_Volume_I_v5_2_READING_VOLUME.md`
- `src/TN_Postmaster_Volume_I_v5_2_TECHNICAL_DOSSIER.md`

**No PDFs are included.** This delivery was assembled without a pandoc/TeX toolchain, so the
build receipts are produced by running the build below. Figures are unchanged from v5.0.

## What changed

v5.2 adds a calibration and restores two proved firewalls. It advances no RH status.

**Technical Dossier, new §§69A–69C.**
- **§69A.** The Davenport–Heilbronn function shares the reflection F(s) = F(1 − s) of completed
  zeta, but its Gamma factor is Γ((s+1)/2), with conductor 5, and it has no Euler product. Its
  zero census runs to height 640. Every rung computed through W₁₆₅₈₈ is positive, and the first
  failure is W₁₆₅₈₉(7140.066) < 0. Both values are computed on a finite zero list. At 250
  digits, at three tested centres, its Löwner (Dobsch) matrices are positive semidefinite
  through N = 100, and the first tested size that fails is N = 105 (sizes step by 5). Read pivot by
  pivot, the exact first failing sizes are N* = 105, 106 and 107 at the three centres. A table
  gives the first failing rung for each of its 16 off-line zeros.
- **§69B.** It adds the parity lemma (TW.1) and the local Gaussian form (TW.2), both proved.
  It also adds the detection law (TW.3), k* ≈ 1.3·t²/(aδ), as evidence only: it is calibrated
  on 15 twin zeros and on 90 off-line pairs planted among Platt's zeta zeros.
- **§69C.** It restores two theorems proved in the v0.3 edition that were never retired but
  had dropped out after v0.4: orientation annihilation, and compact Euler-ray instability.
- **Other edits.** The abstract, §67, §69, §159 and the summary are updated to match. Entries
  121–124 are added to the references, and [66] is corrected.

**Reading Volume.**
- The live pair (R.2) is now ranked by reach, with the twin result stated in that paragraph.
- Three status-key rows and two NO-GO rows (§R25) are added, and [66] is corrected.
- The v5.1 and v5.0 version notes move to `provenance/`.
- The Reader is held to its 101-page ceiling. The twin's tables and displays live only in the
  Dossier; because tags are global, the Reader cites (TW.1) and (TW.3) there.

The full change list, with the open points for the author, is in
`editorial/V52_PUBLICATION_DELTA.md`.

The volumes do not depend on any companion entropy paper.

## Team B corrections (27 September 2026, same edition)

These edits sharpen wording. No number, tag, status mark or reference changed.
- **Gamma factor.** The twin shares the reflection of ξ, not its Gamma factor. The abstract, §§67,
  69, 69A, the summary, the Reader's abstract, (R.2) paragraph, §R25 row and closing are updated.
- **Finite prefix.** "No finite rung prefix decides RH" and "cannot tell ξ from the twin" are
  replaced. The corrected claim: a long finite prefix does not by itself rule out off-line zeros
  that lie higher, or nearer the line, than the prefix can see.
- **Löwner sizes.** The Löwner table reports first *tested* failing sizes. Positivity is scoped to
  the three tested centres, since Dobsch–Donoghue needs every centre. The exact first failing
  sizes, N* = 105, 106 and 107, come from `provenance/v5_2/evidence/team_b_replay/lowner_nstar.py`
  (receipts `nstar_*.json`; a rerun at 320 digits with another contour agrees).
- **Rung precision.** The rung computations are scoped to the finite zero list, and an
  independent 60- and 100-digit replay reproduces the 40-digit values
  (`provenance/v5_2/evidence/team_b_replay/`).

`qa/check_v52_interface.py` still passes 67/67 with the checker unchanged. The Reader grew by
about three source lines; re-measure the 101-page ceiling at build time.

## Verification scope

- **`qa/check_v52_interface.py`** uses the standard library only and writes
  `qa/V52_INTERFACE_RECEIPT.json`. It runs 67 checks before a build; once the build receipts
  exist, it adds page-count and log checks. The 67 cover:
  - preservation of v5.1's equation tags, status tags, status rows and reference numbering;
  - the new tags and their status markers;
  - exact rational algebra for the fold, (TW.1) and (TW.2);
  - the internal consistency of the twin tables (c(n) by Dirichlet inversion, the δ and
    ratio columns, the median, |q₀|, θ_max, the sector bound);
  - agreement between the printed numbers and the recorded runs in `provenance/v5_2/evidence/`;
  - build hygiene (no new glyphs, no `|` inside table math).
- **`qa/make_source_delta.py`** writes the two source diffs, `qa/SOURCE_DELTA.json` and the
  evidence checksums.
- **Evidence.** The twin computations are in `provenance/v5_2/evidence/`, with a map from
  each printed number to its file. They were not rerun for this package. The 40-digit and
  250-digit values come from the Colab runs transcribed in `evidence/colab/COLAB_OUTPUTS.txt`.
- **Inherited certificates.** The v5.0 interval certificates were **not rerun**. They remain
  inherited evidence in `provenance/v5_0/qa/`.

## Build

The build needs Python 3, PyMuPDF, Pandoc (3.x recommended; v5.0 and v5.1 used 3.1.x) and
TeX Live with the packages named in the preambles. From this folder:

```sh
python qa/build_release.py both        # PDFs to output/pdf/, receipts to qa/BUILD_*.json
python qa/build_baseline_v51.py        # optional: v5.1 Reader page count in the same environment
python qa/check_v52_interface.py       # re-run after building to add the page and log checks
```

The interface check enforces the 101-page Reader ceiling once `qa/BUILD_READING.json` exists.
Page counts depend on the toolchain, so compare against `qa/BASELINE_V51.json` when building
with anything other than pandoc 3.1 and TeX Live 2023–2025.

## Provenance

- `provenance/v5_1/` holds the v5.1 masters, preambles, receipts, README and checksums.
- `provenance/v5_0/` and `provenance/v50/` are unchanged.
- `qa/restore_v50.py` restores a separate v5.0 tree.

## Publication status

This is an assembled v5.2 source package. It has not been built into PDFs here, uploaded to
Zenodo, or assigned a deposit DOI. The concept DOI printed in the work identifies the
existing version series.

# TN Postmaster Volume I -- v5.1

Two complete, independently readable companion volumes:

- `output/pdf/TN_Postmaster_Volume_I_v5_1_READING_VOLUME.pdf` (101 pages)
- `output/pdf/TN_Postmaster_Volume_I_v5_1_TECHNICAL_DOSSIER.pdf` (281 pages, including the three inherited facsimile pages)

The editable masters are in `src/`. Figures are retained from v5.0 without modification. The generated TeX is also supplied; build from the Markdown masters rather than editing generated TeX.

## What changed

Both volumes now have self-contained abstracts and summaries. The Reading Volume's contract following (9.8), and Dossier Section 32, specify reflection-pair indexing, multiplicity, and what the fold preserves. The one new equation label is (IF.1). R10C's statement of positivity and monotonicity of an individual kernel is now explicitly restricted to positive real q. The v5.0 theorem/status ledger, equation labels, and research frontier are retained.

The volumes do not depend on *Surprise Is Not Meaning*. The entropy paper imports only the fold convention and first-Li identity; no entropy conclusion is evidence for a TN positivity result.

## Verification scope

`qa/V51_INTERFACE_RECEIPT.json` records 19 focused algebraic, preservation and document-build checks. `qa/BUILD_READING.json` and `qa/BUILD_DOSSIER.json` record the rebuilt PDFs, source hashes, stable references and clean typesetting logs. The two source diffs and `SOURCE_DELTA.json` show the editorial delta explicitly.

The large v5.0 interval certificates were **not rerun** for this editorial release. Their original programs, receipts and metadata remain in `provenance/v5_0/qa/`. They are inherited evidence, not a newly claimed certificate. All such build claims in the new front matter are dated to v5.0.

## Build

Requirements: Python 3, SymPy, PyMuPDF, Pandoc, and a TeX Live installation with the packages named in the supplied preambles. Fonts are standard TeX installation dependencies; no font files are bundled.

From this folder:

```sh
python qa/build_release.py both
python qa/check_v51_interface.py
```

The build requires no network access. `tmp/` is regenerated and is not part of the source of record. The three-page historical facsimile is appended by the build to the Dossier.

## Inherited v5.0 source

For compact storage, unchanged figures are shared. `provenance/v5_0/` contains the remaining original v5.0 source tree. To restore a fully separate original tree, run:

```sh
python qa/restore_v50.py /path/to/a/new/TN_v5_0_SOURCE
```

The script rejects an existing destination. It is for restoring provenance, not for revising v5.1. The original source checksum file is retained within that restored tree.

## Publication status

This delivery is an assembled v5.1 manuscript/source package. It has not been uploaded to Zenodo or assigned a new deposit DOI here. The concept DOI printed in the work identifies the existing version series, not a claim that this revision is already publicly deposited.

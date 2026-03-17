# Last Error Check

Date: 2026-03-17

## Completed checks
- Generated publication figures from `paper/make_publication_figures.py`
- Compiled `paper/Constants_Analysis.tex` successfully with `pdflatex`
- Executed `python track_b/run_quarry.py` successfully from repository root
- Verified CSV outputs were written:
  - `quarry_output/master_atlas_ledger.csv`
  - `quarry_output/filtered_top50.csv`
- Verified featured case cards were generated under:
  - `quarry_output/featured_case_cards/`

## Final patch applied
A runtime warning was observed when exact/trivial identities with `abs_error = 0` or `best_q <= 1`
entered the ranking and case-card pipeline. These were not meaningful transient geometries.

The following filter was added to `track_b/run_quarry.py`:
- drop exact / trivial pairs before ranking and case-card generation

This removed the warning path and produced a clean filtered leaderboard.

## Notes
- The repository package includes the uploaded deep-research packaging report files under `docs/`.
- The manuscript package is ready for Overleaf upload.
- Please review display-name metadata in `CITATION.cff` before public Zenodo release if you want a full-name variant rather than the current minimal form.

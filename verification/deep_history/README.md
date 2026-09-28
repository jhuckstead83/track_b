# Deep-history checks

Team B, 27–28 September 2026. **RH STATUS: OPEN.**

| File | What it checks |
| --- | --- |
| `v05_synthesis_checks.py`, `V05_SYNTHESIS_CHECKS.json` | The synthesis layer of TN Postmaster Research Volume I v0.5 (10.5281/zenodo.21968858). Its load-bearing identities replay 13 of 13, and so does the constant-Jacobian counterexample it records. The defects found are cosmetic: two `qquad` typos, one `-log U`, and a mis-titled Rowland–Wu citation. |
| `V50_CERTIFICATE_REEXECUTION.json` | The inherited v5.0 source-rung certificates W₂–W₆, re-executed from `provenance/v5_0` of the v5.2 source (see below). |

Details of the v5.0 re-execution:
- `qa/replay_math.py` ran all 16 steps with exit code 0.
- Its regenerated receipts equal the shipped ones apart from timing fields.
- The second parameter set was also run: Arb at 384 bits, degree 22, step 1/128; Decimal at 100 digits, degree 24. Its receipts and the cross-backend check equal the shipped `*_second` receipts, apart from timing fields.

These checks re-execute existing certificates. They add no Widder rung: W₇ via F^(14) remains OPEN.

Run the v0.5 checks with:

    python3 verification/deep_history/v05_synthesis_checks.py

Run the v5.0 replay from an unpacked copy of `papers/TN_Postmaster_Volume_I_v5_2_SOURCE/provenance/v5_0/` with:

    python3 qa/replay_math.py

It needs `python-flint` 0.9.0 and SymPy.

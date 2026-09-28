# 51 SEDAPS v0.4.1 — independent replays

Team B, 27 September 2026. These programs are separate from the shipped JavaScript. They restate the
rule from its text and read only the certificate JSON files in the parent folder. RH STATUS: OPEN.

| File | What it checks | Run |
| --- | --- | --- |
| `sedaps_independent.py` | v0.3 certificate; all 20 four-for-four deals; 01/11 mod-3 clock at every turn; 10 at every elapsed turn (reached exactly at 24, 27, 30, 33); forward fates; the 2,000-deal remnant | `python3 sedaps_independent.py` (about 25 s) |
| `census2.c` | complete state census, 3-queue rule (all states, or `live3`) or 2-queue War | `gcc -O3 -o census2 census2.c && ./census2 9 3` |
| `census_alt.c` | the same, recording winner alternation and α on every loop (2-queue mode) | `./census_alt 11 2` |
| `census_deals.c` | never-ending alternate deals; reproduces OEIS A400411 | `./census_deals 11 2 deals` |
| `live3_packet.c`, `live3_loops.c` | every packet-form state of n cards, played until a queue empties; `live3_loops.c` also catalogues the three-live loops, and with a fourth argument `cong` keeps only sizes congruent mod 3, the states an equal deal can reach (v0.4.1 §2); receipt `LIVE3_LOOPS_RECEIPT.json` | `gcc -O3 -o live3_loops live3_loops.c && ./live3_loops 11` (about 10 s); n = 12 in four shards: `./live3_loops 12 s 4` for s = 0…3, a few minutes each |
| `war_period_sigma.py` | brute-force alternation for n ≤ 9 and the period 2·ord(σ) for every α | `python3 war_period_sigma.py` |
| `CENSUS_RECEIPT.json` | the census results for n ≤ 11 (3 queues) and n ≤ 12 (2 queues) | — |
| `sedaps_independent_receipt.json` | the replay receipt | — |

Memory: the 3-queue census at n = 11 needs about 0.8 GB (two bits per state, 3.11 × 10⁹ states);
the 2-queue census at n = 12 about 1.3 GB.

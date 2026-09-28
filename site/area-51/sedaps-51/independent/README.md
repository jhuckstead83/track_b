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
| `live3_struct.c` | `live3_loops.c` plus a structural classification of every loop found: largest queue, win gaps, whether the winner always plays a packet head, one head per turn | `./live3_struct 12 s 4` for s = 0…3 |
| `live3_sync.c` | every whole-packet state, with the global maximum in queue 0: a complete search for the loops an equal deal could reach (v0.4.1 §2) | `./live3_sync 12`; n = 15 in shards, hours each |
| `live3_rigid12.c` | every rigid-shape state at n = 12 for each of the 55 head sets containing 11, played while the head wins; its totals equal the census, so every loop at 12 cards is rigid; receipt `live3_rigid12_receipt.json` | `cc -O2 -fopenmp -o live3_rigid12 live3_rigid12.c && ./live3_rigid12` (about 30 s on 4 cores) |
| `live3_construct.py` | top-headed states for n = 12 to 51, played until they return, with the four invariants and the undo step checked every turn; receipt `live3_construct_receipt.json` | `python3 live3_construct.py` (a few seconds) |
| `live3_construct_check.cjs` | replays the 15- and 51-card witnesses with the site's engine `sedaps-core-v0-2.js` | `node live3_construct_check.cjs` |
| `live3_rigid_period.py` | the rigid-loop period formula against the order of σ and against play, for every shape at every n from 12 to 51; complete spectra; receipt `live3_rigid_period_receipt.json` | `python3 live3_rigid_period.py` (about 10 s) |
| `live3_probe51.py` | 3,000 synchronised states and 3,000 deals at 51 cards (status C); receipt `live3_probe51_receipt.json` | `python3 live3_probe51.py` (under a minute) |
| `war_period_sigma.py` | brute-force alternation for n ≤ 9 and the period 2·ord(σ) for every α | `python3 war_period_sigma.py` |
| `CENSUS_RECEIPT.json` | the census results for n ≤ 11 (3 queues) and n ≤ 12 (2 queues) | — |
| `sedaps_independent_receipt.json` | the replay receipt | — |

Memory: the 3-queue census at n = 11 needs about 0.8 GB (two bits per state, 3.11 × 10⁹ states);
the 2-queue census at n = 12 about 1.3 GB.

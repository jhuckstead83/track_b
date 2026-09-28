# Forge 51 — two sides, one observation, and recoverable history

Research return v0.2 · 26 September 2026, America/New_York

**Primary project:** Forge 51, a Python/Colab research notebook. **Website sidecar:** 51 Sedaps. Literal string reversal of `SPADES 51` is `15 SEDAPS`; reversing a block does not change its cardinality of 51. Neither title is connected to the historical count of 15 terminating runs.

**RH STATUS: OPEN**

## What merits attention

1. **51 Sedaps has a sharp, small history cost.** Under the published ordinary three-player capture rule, every current state has at most four one-turn predecessors. Four actually occur in the legal 51-card state space. Consequently an endpoint and **two bits per played move** suffice to reconstruct a trajectory, when the transition convention and move count are known. This is a new derivation relative to the inspected handoff, notebook, and v7.2 card rule; no claim of literature-wide novelty is made.
2. **TFG growth needs a declared embedding.** Keeping physical cells fixed and reflecting do not commute. Keeping the signed triangular address fixed does commute with reflection, using a different embedding on each side. This makes the existing warning about rectangle-dependent coordinates an explicit commuting-map result.
3. **The approved rounded-q pilot fails immediately and correctly.** One on-seam and one off-seam point have exactly the same declared rounded observation. The exact rational control separates them. This anticipated failure is a calibration result, not independent surprise.

Your instruction, “you can’t have a boundary without two sides,” is implemented here by naming the signed sides before applying a quotient. For fixed positive t, let δ=β−1/2. The negative and positive sides are δ<0 and δ>0; the seam is δ=0. The map δ↦δ² merges the two sides but preserves whether δ=0. In the quotient, that seam is an endpoint. We therefore ask two separate targets: **side** and **seam membership**. Neither target substitutes for the other.

## Research board

| Object | Exact facts | Fuzzy/open interface | Cheapest decisive experiment |
|---|---|---|---|
| TFG chambers and rectangle | ρ(r,c)=T_(r−1)+c is invertible; signed rectangle coordinates have two triangular sheets | Which coordinates stay fixed under N→N+1? | Compare physical and signed-address embeddings against reflection. Completed on 140 cells, with an all-n algebraic proof below. |
| Normalized four-step zero relation | For an index set M, W₄(M)=⋃_(j=1)^4(M+j) is a directed horizon | The exact y_n normalization, event definition, overlap handling and historical training windows are missing | Recover the frozen preprocessing first; then one forward-only packet test with its baseline and null fixed before reveal. Not run. |
| Q_E3.5 | No mathematical phase boundary has been established by this handoff | Definition, fitted threshold, transition band, or artifact? | Recover the original threshold provenance and formula. No scan or threshold tuning is authorized by this report. |
| Forge 51 | Commitments, pure player interface, deterministic caps and separate ledgers are implemented | A useful source-owned target and its analytic transport remain open | The frozen rounded-q firewall pilot. Completed; counterexample on first block. |
| 51 Sedaps | Mirror conjugacy; predecessor bound ≤4; explicit four-way 51-card witness | Reachability of that witness from 17–17–17 starts; optional changes to the capture rule | Exact predecessor enumeration and reference-rule replay. Completed; no recurrence search. |
| Folded q and scalar W | q=s(1−s); Im q=−2tδ; W forgets the sign of δ. Exact height information can recover distance from the seam in the stated domain | Exact recoverability versus finite-precision resolution; whether the observation is independently available | Preserve the signed coordinate, test known fibers, and apply the paper's exact sensitivity formula. No zero data used. |
| Source-side prime/Gamma lane | Finite two-sheet extension and swap are exact; common-weight magnitude balance is coefficient-independent | Completion, tails, coupled source positivity and a map to the actual zero set | First test arithmetic specificity against changed common weights. Existing balance identity already survives that null, so it cannot establish prime-specific forcing. Gamma-minus-prime transport remains untested here. |

W₄ (directed horizon), R₄ (merge radius), M₄ (residue partition), and χ₄ (Dirichlet character) remain different typed objects. No cyclic residue interpretation has been inferred from four forward offsets.

## Exact delta A: four possible pasts, at most two bits per move

### Domain and source rule

A state X=(H₀,H₁,H₂) consists of three labeled ordered queues partitioning a fixed set of distinct cards. The published strength address is q=4(v−1)+s; 2♣, q=7, is excluded. The greatest exposed address wins. Every nonempty queue removes its first card. The winner appends its own exposed card first, then the other exposed cards in clockwise player order.

Let F be this **played-turn** map on states with at least two nonempty queues. A terminal state's artificial self-loop is excluded from predecessor counting. For mirror calibration only, extend F by fixing terminal states. Optional forgiveness/escrow is a different transition and is outside this result.

### Proposition

For every state X, |Pre_F(X)|≤4. This bound is attained for 51 active cards.

**Proof.** Let B be the current nonempty-player set, b=|B|. A possible previous live-player set A must contain B, have size 2 or 3, and have a winner w∈B. For fixed (A,w), the last |A| cards of H_w must be the returned pot. Their order uniquely identifies the card drawn by each player. Remove this suffix and prepend the identified draws to those players' queues. This gives at most one predecessor; reject it unless the first card in the pot is greatest and forward replay returns X.

The numbers of candidate pairs (A,w) are:

| Current live players b | Possible preceding live sets | Candidate predecessors at most |
|---|---|---:|
| 3 | A=B | 3 |
| 2 | A=B or all three | 4 |
| 1 | Either of the two two-player sets containing B, or all three | 3 |

Thus there are at most four. This is a counting proof for arbitrary card count under the stated rule, independent of the finite enumeration. □

### A sharp six-card witness, lifted to all 51

Use addresses 0,1,2,3,4,5, whose ordinary faces are A♠, A♥, A♦, A♣, 2♠, 2♥. All four rows below map in one turn to the same endpoint:

**Endpoint:** `((5,3,1), (4,2,0), ())`.

| Predecessor H₀ | Predecessor H₁ | Predecessor H₂ | Winner | Previous live players |
|---|---|---|---:|---|
| (0,5,3,1) | (2,4) | () | 1 | {0,1} |
| (0,5,3,1) | (4) | (2) | 1 | {0,1,2} |
| (3,5) | (1,4,2,0) | () | 0 | {0,1} |
| (5) | (3,4,2,0) | (1) | 0 | {0,1,2} |

For the actual deck, let U be the increasing list of the other 45 active strength addresses. Replace the endpoint by `(U‖(5,3,1), (4,2,0), ())`, where ‖ denotes concatenation. The four predecessors become:

1. `((0)‖U‖(5,3,1), (2,4), ())`;
2. `((0)‖U‖(5,3,1), (4), (2))`;
3. `((3)‖U‖(5), (1,4,2,0), ())`;
4. `((5)‖U, (3,4,2,0), (1))`.

All four were independently replayed through the archived `war.py` implementation with a one-turn cap. No higher cards in U are exposed during these turns. The common endpoint has hand sizes (48,3,0).

**Scope:** These are legal states. Reachability of this particular endpoint from an initial 17–17–17 deal has not been proved. The upper bound remains valid on any reachable subset; sharpness on that restricted subset is open.

### Recovering the past

Order the valid predecessors lexicographically using the declared card addresses and player order. Store the actual predecessor's index, 0–3, using two bits. Given the endpoint, decode that index and recover the previous state. Repeat backward for the known move count. The fixed rule, endpoint, ordering convention, and log length are shared information; they are not included in the two-bit-per-move figure. Recovering a pre-shuffle deck additionally requires the shuffle convention/record.

Two bits are also necessary in the worst case for a fixed-length one-move code when all four legal predecessors are admissible. The full archived event log is sufficient but contains more information than one-step inversion requires.

Current state plus winner is insufficient in the witness: each winner has two compatible live masks. Current state plus previous live mask is also insufficient: each mask has two compatible winners. **Current state plus both winner and previous live mask is sufficient**, although the sorted predecessor index packs the needed distinction into at most two bits.

### Mirror is not inverse

For the explicit full-state mirror

R(H₀,H₁,H₂)=(rev H₂, rev H₁, rev H₀),

the queue separators and player labels are transported as part of the convention. With F^R=RFR, the equality RF=F^R R is algebraic. It does not imply RF=FR and does not construct F⁻¹. The four-way collision forbids a single-valued state-only inverse on this domain. The extra branch log restores backward recoverability on the image of the augmented transition.

This suggests a finite sidecar mechanic: present a shared endpoint, expose one history bit at a time, and ask which predecessors remain possible. It directly implements observer-relative history ambiguity without inventing a scalar measure of meaning.

## Exact delta B: which growth commutes with the mirror?

Use R_n=[n]×[n+1], u=j−i−1/2, and the physical reflection

S_n(i,j)=(n+1−i,n+2−j).

The physical inclusion E_n(i,j)=(i,j) satisfies

**S_(n+1) E_n(i,j)=E_n S_n(i,j)+(1,1).**

Consequently the physical extension/reflection diagram fails at every cell. This is an exact coordinate defect, not sampling noise.

Now preserve the signed triangular address (ε,r,c), where ε=sign(u), c=|u|+1/2, and r=i on the negative sheet or r=n+1−i on the positive sheet. Its induced embedding is

- E*_n(i,j)=(i,j) for u<0;
- E*_n(i,j)=(i+1,j+1) for u>0.

Direct substitution on the two sides gives **S_(n+1) E*_n=E*_n S_n** and preserves (ε,r,c) exactly. Both embeddings preserve the signed seam coordinate u. They differ in which cell/address is identified across sizes.

The audit checked n=1,2,11, totaling 140 cells: 140 physical commutator defects; 140 passing signed-address checks. The algebra above proves the claims for all n. Neither embedding is automatically the one a later analytic map must use.

## The two resolved tension points

These were the two selected structural questions, with both sides defined before evaluation. Their exact outcomes now move to the calibration pool.

| Seat | State space / map | Target | Null or countermodel | Frozen bound and stop | Outcome |
|---|---|---|---|---|---|
| F51-L0-002-SEDAPS-PREDECESSORS | Three ordered queues; published F; explicit R | Is the past uniquely recoverable? Does the full mirror commute after conjugation? | Distinct legal predecessors with one endpoint; unconjugated mirror | 20,160 six-card states, 60 seconds; first invariant failure stops; four 51-card one-step reference checks | Unique state-only past fails; degree ≤4 with sharp witness; conjugated mirror passes |
| TFG embedding control, inside L0 | R_n with E_n or E*_n and S_n | Is extension reflection-compatible while the declared address is preserved? | Physical inclusion versus signed-address inclusion | Exactly 140 disclosed cells, n∈{1,2,11}; first exact discrepancy against the derived identity stops | Physical diagram fails by (1,1); adapted diagram commutes |

No third empirical tension point is promoted while y_n and Q_E3.5 remain unspecified.

## Folded q: source-derived facts and the precision implication

The recovered v0.1 notebook already marks the t²=1/12 threshold. The v7.2 paper §6 proves recovery from (t,W) for known t≥1 on its strip domain; §7 equation (16) gives the exact fixed-height sensitivity. These are **existing results**, not fresh discoveries.

Writing δ=β−1/2 and A=t²+1/4 gives q_r=A−δ², q_i=−2tδ and

\[
1-\frac{W(\beta,t)}{W(1/2,t)}
=\frac{\delta^2(3t^2-1/4+\delta^2)}{(A-\delta^2)^2+4t^2\delta^2}.
\]

At t²≥1/12 this vanishes exactly when δ=0; below the threshold a second seam-weight solution has δ²=1/4−3t². W is even in δ, so it never identifies the side at a fixed positive height. Adding sign(Im q) would distinguish the sides, but that coordinate must be independently available; manufacturing it from an unknown β would disclose the target.

For fixed nonzero δ and t→∞, the relative deficit is asymptotic to **3δ²/t²**, while the absolute weight deficit is asymptotic to **6δ²/t⁴**. Thus greater height improves neither finite-precision resolution nor information ownership. This is an algebraic consequence of the existing formula, not a new zero experiment.

For instance, the synthetic choice δ=1/4 and t=10¹² has relative deficit approximately 1.875×10⁻²⁵. A binary64 W computation cannot generally resolve that relative change. If β itself has already been rounded onto 1/2, later high-precision arithmetic cannot restore it. Exact rational or interval inputs must precede the arithmetic. A stable formula for a known δ is a diagnostic; it is not a source-owned way of learning an unknown δ.

## Frozen pilot ledger: F51-L1-001-ROUNDED-Q

The original contract was implemented without retuning. Python 3.12.14, x86_64 Linux, NumPy 2.3.5 and pandas 2.2.3 matched its environment. Original handoff and notebook hashes matched. The additional recovered Colab-run notebook has identical source across all 29 cells and no recorded error outputs; that is evidence about the old notebook, not a live Colab test of this release.

**Player:** only canonicalized binary64 q rounded to 12 decimal places. Fixed p=0.95 for zero observed imaginary part, else p=0.05. **Dealer:** rational β,t,q, target label, pair identity, seed and ordering metadata. Predictor has no globals/closure accessing those fields. This is auditable procedural separation, not cryptographic isolation.

**Board:** j=1,…,17; t=(2j−1)/2; k∈{20,40,46}; matched β=1/2 and β=1/2+(−1)^(j+k)2^(−k). Seed 510052; 102 observations and predictions committed before first label reveal. Control: exact rational q. Baseline: p=1/2. Target: exact β=1/2, on synthetic points only. Complete original contract and machine-readable manifests are in the bundle.

The first shuffled block was (j,k)=(2,46), t=3/2:

| State | Exact Im q | Rounded observation | Exact label |
|---|---|---|---:|
| β=1/2 | 0 | (2.5,0.0) | 1 |
| β=1/2+2⁻⁴⁶ | −3/2⁴⁶ | (2.5,0.0) | 0 |

The off-seam real component is exactly 5/2−2⁻⁹². Both the exact reflection and conjugation controls passed. The run stopped after this complete block, as frozen.

### Exact-check ledger

| Check | Result |
|---|---|
| Original input hashes and canonical cell sources | PASS |
| Public 25-trial two-sheet controls; 76 card constructions, cutoff ≤201 | PASS; max balance residual 1.7763568394002505×10⁻¹⁵; swap and extension residuals zero |
| Support/complement; successor gate | PASS; 148 exact successor cases |
| TFG inverses and two-sheet fibers | PASS; 140 cells |
| Both published rational W collisions; public manifest | PASS |
| Revealed rational q controls | PASS |
| Observation/prediction commitments | PASS |

### Surprise scoreboard — kept separate

| Item | Value |
|---|---:|
| Committed predictions | 102 |
| Scored outcomes | 2 |
| Unscored outcomes | 100 |
| Player mean log loss | 2.1979643381655687 bits |
| Baseline mean log loss | 1 bit |
| Total bits gained over baseline | −2.3959286763311374 |
| p=0.95 bin | 2 observations; positive frequency 1/2 |
| p=0.05 bin | Empty |

Independent research surprise: **N/A**. This intentionally targets a known rounding mechanism. Scores describe only the stopped synthetic prefix; no significance claim or extrapolation is made.

### Structural-survival scoreboard

| Dimension | Status |
|---|---|
| Public finite-card extension | PASS |
| Revealed reflection/conjugation | PASS |
| TFG address preservation and immutable record commitments | PASS |
| Exact-q positive control | PASS on revealed states |
| Rounded-q target fibers | COUNTEREXAMPLE |
| Source-to-zero transport | NOT TESTED |
| Zero-location data leakage | No zero dataset; fixed pure predictor sees only K |

**Classification:** COUNTEREXAMPLE to exact target recovery from the declared rounded observation. **Recommendation:** REPAIR. Exact/interval observation handling belongs in a new contract; it was not patched into this run.

**What changed:** failure gates, commitments, a serialized collision, the predecessor theorem and the explicit TFG embedding distinction. **What did not change:** original source notebooks, RH, the missing analytic transport, and the untested historical zero-gap claims. **RH STATUS: OPEN.**

### Compute and provenance

The original pilot took approximately 0.30 seconds of computation. It used 1 of 51 allowed blocks, 106 of 306 allowed rounded-q evaluations, 106 of 306 exact-q evaluations, and 102 fixed predictions. The exact six-card audit took approximately 0.69 seconds: 20,160 states, 18,000 played transitions, and all predecessor lists checked against exhaustive enumeration. Its degree histogram was {0:8160, 1:7200, 2:3660, 3:1080, 4:60}. These are finite state counts, not probabilities for the 51-card game.

| Commitment | SHA-256 |
|---|---|
| Frozen contract | b80572890deb75444b2e6392e7c277aab9362cfd2ffaba1d23db64d2c6072843 |
| Dealer manifest | 874351e61920f8ae524c090d7c2205eb61cf044387bdc6c3d0c8722fff083a60 |
| Player observations | 3f8f8f7c957c20279882d8510f2236fbed96b4bc2b252673670636deaab8d533 |
| Player predictions | 60db297d3cdf4c740eba8a0383369b25c5effbbdc368df8dc0482da41b8f6456 |
| Archived war.py | 92b4e9866a6791704e76050132225cd74c0ee184d81d14bc815d7a8835c827c8 |

## Notebook and next input

`Forge_51_v0_2.ipynb` is self-contained: the original inputs, fixed contract, reference results, exact lab and runner are embedded. Run all cells in a standard Colab Python runtime. It replays disclosed results; it does not open another holdout. Replay permits a different Python/package version only if binary64, original hashes, commitments, stop location and outcomes match. A mismatch stops with IMPLEMENTATION FAILURE. The original strict-environment runner remains unchanged. No package installer, network data fetch, root search or full-height dispatcher is included.

The notebook includes the two scoreboards, exact side/seam table, predecessor replay, and a manifest checklist for a future zero-data seat. It has been executed locally from its code cells; a live fresh Colab run of this release remains for the user.

The next missing input is specific: **What is the exact formula for the historical normalized y_n, and where did the 3.5 threshold come from?** A source notebook cell or frozen run configuration is preferable to reconstructing it from a plot. Include whether the normalization uses future neighbors and which windows selected the threshold. That determines what can enter the player view and which data can still serve as a holdout.

Full-height zero computation remains with the user in Colab. No high-height run was launched here. No empirical threshold, new seed, next scale or source-to-zero theorem has been invented.

**Overall recommendation: READY FOR USER DECISION** on the next defined seat; the completed rounded-q seat separately recommends REPAIR.

**RH STATUS: OPEN**

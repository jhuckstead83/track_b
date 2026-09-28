# Formula 51: 51 is unique by deduction, and a more legible table exists

Team B, 27 September 2026. The input is *Formula 51, Concise Method* (26 September 2026), run unchanged for every radix N through its own `derive51.py`. That file ships in this folder and is identical to the Project 51 v0.3 fixture. The decoder scores are Project 51's:
- the (weight class, polar address) fibres;
- the largest injective factorial sector for (class, polar, color).

Run `python f51_band.py` in this folder to regenerate `f51_band.json` byte for byte. It covers every N from 1 to 11,172. `python f51_independent.py f51_band.json` recomputes all of it without `derive51.py` or `unicodedata` (see §6). RH STATUS: OPEN.

## 1. The band claim holds (CHECKED)

Exactly the radices **1177 ≤ N ≤ 1764** give 51 visible components: 588 values, contiguous. N = 1438 reproduces Project 51 exactly:
- class sizes 2, 1, 9, 1, 9, 11, 18;
- **8** compatible arrangements (3 collision pairs);
- injective (class, polar, color) sector **45!**.

## 2. A better example exists in the band (COMPUTED)

The decoder scores vary across the band.

| compatible arrangements (class + polar) | 4 | 8 | 12 | 16 | 24 | … | 11520 |
|---|---|---|---|---|---|---|---|
| number of radices | 24 | 48 | 66 | 12 | 70 | … | 6 |

| injective (class, polar, color) sector | 23! | 36! | 41! | 45! | **51!** |
|---|---|---|---|---|---|
| number of radices | 414 | 16 | 70 | 80 | **8** |

**N = 1353, 1354, 1355 and 1356** beat 1438 on both scores. Class + polar leaves only **4** arrangements, and (class, polar, color) is **fully injective**: all 51 cards are identified, a 51! sector. N = 1349–1352 also reach full injectivity, with 8 arrangements.

The trade-off: these radices have ⌊N/28⌋ = 48 complete leading/vowel contexts, not 51. They lose the self-description of §3.

## 3. 51 is forced by self-description (PROVED)

Call a radix **self-describing** when its number of visible components equals its number of complete leading/vowel contexts. Hangul has 21 vowels and 28 trailing slots, counting "none". Two quantities must be kept apart:

- **K(N)**, the number of visible components. For N ≥ 588 all 21 vowels and all 27 trailing consonants occur, so K = L + 48, with L = ⌈N/588⌉ leading consonants. Then **K = 51 ⇔ L = 3 ⇔ N ∈ [1177, 1764]**, the 588-radix band of §1.
- **c(N) = ⌊N/28⌋**, the number of complete leading/vowel contexts. Then **c = 51 ⇔ N ∈ [1428, 1455]**.

Self-description is K = c. The proof has two cases.

**Case N ≥ 588.**
1. From 588(L − 1) < N ≤ 588L we get 21(L − 1) ≤ c ≤ 21L.
2. Put c = L + 48 into this bracket. That gives 20L ≥ 48 and 20L ≤ 69, so **L = 3**.
3. Then K = 51, so c = 51, so N ∈ [1428, 1455].
4. Conversely, each N in [1428, 1455] has L = 3, because 1176 < N ≤ 1764. So K = 51 = c.

**Case N < 588.** Then K ≥ 1 + ⌈N/28⌉, which exceeds c = ⌊N/28⌋, so there is no solution.

The self-describing radices are therefore exactly **N = 1428…1455**: the band K = 51 intersected with c = 51. **51 is the unique self-describing alphabet size of the Hangul syllable block.** The exhaustive search over all 11,172 radices agrees.

*Correction (27 September).* The first version of this proof wrote the condition as c − ⌈c/21⌉ = 48. That silently used ⌈N/588⌉ = ⌈⌊N/28⌋/21⌉, which is false exactly when N ≡ 1, …, 27 (mod 588): 486 radices in [588, 11172], or 513 in [1, 11172]. The bracket above avoids the step. The conclusion was unaffected.

Three repairs were made independently and agree: Team B (above), Blue Team PP272, and the Fork-A research pass (site v2.8.1). Fork-A bounds c directly: 28c ≤ N ≤ 28c + 27 and 588(c − 49) < N ≤ 588(c − 48) give 28224 ≤ 560c < 28839, so c = 51.

## 4. Inside the self-describing window, 1438 is co-optimal, then unique

| N | r = N mod 28 | class sizes | arrangements | (class, polar, color) sector |
|---|---|---|---|---|
| 1433–1436 | 5–8 | …, 4–7, 11, 23–20 | 16 | 45! |
| **1437** | 9 | 2,1,9,1,8,11,19 | **8** | **45!** |
| **1438** | 10 | 2,1,**9**,1,**9**,11,18 | **8** | **45!** |
| **1439** | 11 | 2,1,9,1,10,11,17 | **8** | **45!** |
| **1440** | 12 | 2,1,9,1,11,11,16 | **8** | **45!** |
| 1441–1443 | 13–15 | … | 8 | 23! |
| all others | | | 12–192 | 23!–36! |

- **Decoder optimum (COMPUTED).** Within the window, only **1437–1440** are optimal on both decoder scores.
- **Balanced partial classes (PROVED).** Inside the window, the vowel class V₀…V₈ always has 9 members, because 1176 = 42·28 makes the L₂ block 252 + r long. The trailing class T₁…T_{r−1} has r − 1 members. The two are equal only at r = 10, that is, **N = 1438**. It is the unique self-describing radix with two nine-member partial-context classes.
  - In one line: over the window, balanced ⇔ ⌊(N − 1176)/28⌋ = (N mod 28) − 1 (PP274).
  - The seven-class picture needs r ≥ 2. At the two lowest radices the class count drops: N = 1428 (r = 0) has 5 classes, 2, 1, 9, 12, 27; N = 1429 (r = 1) has 6, 2, 1, 9, 1, 11, 27. A table over all 28 self-describing radices that assumes seven classes is wrong on those two rows.

**Deduction chain.** Self-describing ⇒ 51 components and N ∈ [1428, 1455]. Decoder-optimal ⇒ N ∈ [1437, 1440]. Balanced partial classes ⇒ N = 1438.

## 5. Reading

- **1438 was not chosen.** It is the original count of tabulated zeros. The chain shows that this data-given radix lands inside the four-radix optimum of the 28 self-describing radices, and that the balance condition picks it out exactly. That is a characterization, not evidence about zeros. The method record's fence, "the repeated count is not evidence about ordinate values", stands.
- **A property of 1438 is not a reason for 1438** (PP274). Among the 28 self-describing radices, exactly four minimise the arrangement count while maximising the safe sector, and exactly one of those, N = 1438, has ⌊(N − 1176)/28⌋ = (N mod 28) − 1. This is a property of 1438 established in September 2026, not a record of how the radix was selected. The provenance question of the method record is unchanged: why Hangul was chosen, and whether other radices were explored, remain undocumented.
- **For the games' table.** If a fully legible table is ever wanted, N = 1353–1356 gives one in which class + polar + color identifies every card, at the cost of self-description. Changing the alphabet would change every game built on it. That is a design decision, not a correction.
- **The deck's 52 − 1 = 51 is a separate fact.** The deck side is a physical choice; Hangul supplies 51 by self-description.
- **The deployed table matches the derivation.** The symbol file and `area-51/prospect-51/data.js` agree with it on every card, symbol, class, polar address and color (0 mismatches, checked against the v2.6.1 site).

## 6. Independent replay and two further results (27 Sep; released in v2.8.3)

`f51_independent.py` rebuilds every radix from explicit Hangul arithmetic: L = ⌊d/588⌋, V = ⌊(d mod 588)/28⌋, T = d mod 28. Each weight class is an exact product of conditional ratios. It does not import `derive51.py` and does not use `unicodedata`. Its receipt is `f51_independent_receipt.json`.

| Check | Result |
| --- | --- |
| Component counts, N = 1 … 11,172 | the band [1177, 1764] (588 radices); self-describing radices exactly [1428, 1455] |
| The 588 band tables (class sizes, arrangements, collision pairs, sector, contexts, lowest class) | all equal `f51_band.json`, 0 mismatches |
| Repaired §3 bracket | holds for every N ≥ 588; the old ceiling step fails at 486 of them |
| Window optimum and balance | 1437–1440 decoder-optimal; balanced partial classes only at 1438 |

Two results proposed by the Blue Team (PP270), now replayed independently as their requested second return. PP274 grades both A-CAT:

- **Where the trailing class is lightest.**
  - The edge inequalities hold exactly: 28⁵¹ < 21⁵⁶ < 28⁵², and 1218⁴² < 42⁴²·28⁴³ < 1219⁴³.
  - The lowest-weight class is a visible trailing class for exactly **257 radices, [1219, 1455] ∪ [1745, 1764]**.
  - At N = 1438 the binding margin is 56·log₂21 − 51·log₂28 = 0.794675, a factor 21⁵⁶/28⁵¹ ≈ 1.7347.
- **The polar fibres (Project 51).**
  - The fibre of t/s is {js(js − 1)/2 + jt : j ≥ 1}. On 51 identities that gives 30 labels and 50,164,531,200 lifts.
  - The largest fibre is the triangular numbers {1, 3, 6, 10, 15, 21, 28, 36, 45}.
  - The weight classes cut it into the three pairs {6, 10}, {15, 21}, {36, 45}, so J = (W, P) has exactly 8 lifts.
  - The sharp sectors follow from the single rule k_max = 51 − μ_f: they are 15, 23 and 45.

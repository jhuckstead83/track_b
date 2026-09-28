# Where the source went, and the twin test on the principal route

Team B, 27 September 2026. The sources are:
- `TN_Postmaster_v0_5_Source_and_Audit (3).zip`, containing v0.1–v0.5, the Master Volume v0.6 PDF and the nested v0.3 and v0.4 packages;
- the Master Volume companion audits;
- the manuscripts for v0.6, v0.7, v1.0–v1.6, v2.9, v3.0 and v5.1.

`RH STATUS: OPEN`. No ledger was edited and no status was promoted.

---

## 1. Short answer

**The source was not lost at inception.** The inception had the right diagnosis, the right target and the right firewalls:

- **Master Volume companion audit (10 Aug).** It split Li's coefficients as λ_n = A_n (archimedean, positive) − P_n (prime sum, "the entire difficulty"). It then ruled: *"Every coordinate in the volume is on the side that cannot close this … it would have to say something new about the prime side."*
- **Postmaster v0.1–v0.3 (14–16 Aug)** sharpened that into three proved statements and one target:
  - **Orientation annihilation** (v0.3, eq. `orientation-annihilation`): *"a conjugation-symmetric linear zero functional … erases the orientation bit. Absolute value, a half-plane projection, or equivalent phase information must be added."*
  - **Compact Euler-ray instability** (v0.3, Theorem `compact-instability`): no map continuous in a finite-order C^k topology recovers the defect from compact Euler-accessible data, uniformly over the real-symmetric Cartwright class. Its boundary box keeps *"a zeta-specific arithmetic identity using the complete prime/Gamma data"* as the one open door.
  - **Parity blindness** (v0.1, firewall #6): reflection-even observables respond as α²u², losing the first-order sign.
  - **The target** (v0.1): an orientation-preserving arithmetic Hardy projection of the upper folded divisor, built from prime, Gamma and theta data.

**What was lost, and when.**

- **v0.4, 16 Aug (PP18–PP27).** The work pivoted to heat, complete-monotonicity and Stieltjes/Hankel criteria on the safe axis. These are exactly the conjugation-symmetric real-axis tests that v0.3 had just proved blind to orientation. From v0.4 through v5.1, the orientation-annihilation, compact-ray and parity firewalls have **zero mentions**. They were never retired; they were simply not carried forward. The v0.4 memo keeps only the weaker line "finite batteries are nonforcing".
- **v1.0, 21 Aug.** The Widder rung ladder became the organizing frontier. W₂ and W₃ were "proved by source-side directed-interval" certificates; v1.2 put "Source Rungs" in the title. A month of work then climbed W₂ → W₆ (v3.0 reached F^(8); v5.1 reached W₆), with W₇ ⇝ F^(14) as the live next step.
- **In the process, the word "source" changed meaning.** At inception it meant *zeta-specific arithmetic that must supply the orientation bit*. By v5.1 it means *the safe-axis Gamma-plus-prime formula (9.5), evaluated without zero data*. A function without an Euler product has a source in the second sense too. The twin has one, and it passes the same rungs.

**What remained, in v5.1:**

- **The prime channel P(x) = (1/R)·Σ Λ(n) n^(−s_x)** inside the principal route L_Γ − L_P ⪰ 0 (§R16). It is RH-equivalent and uses Λ ≥ 0, but every finite section of it is parity-blind (§3).
- **The exact-divisor route (§§155H–155J).** It uses Möbius arithmetic and lives in the one-sided Hardy space of Re s > ½. This is the one v5.1 route that kept the inception's orientation property. It gets its own subsection below.
- **The §155G Euler-side countermodel.** It has positive prime-power weights, a PNT envelope, a meromorphic Euler product and an exact prime prefix, yet interior poles. It lacks the functional equation.

**Why the exact-divisor route keeps orientation.** A zero ρ with Re ρ > ½ blocks the Nyman–Beurling/Báez-Duarte approximation through point evaluation. The classical reproducing-kernel bound gives a squared distance of at least (2Re ρ − 1)/|ρ|². That is first order in the displacement: one-sided, not parity-blind. Its finite approximants converge only like 1/log N, so it is no cheap finite test either.

## 2. Timeline

| date | version | what the prime side was doing | orientation / compact-ray / parity firewalls | organizing frontier |
|---|---|---|---|---|
| 10 Aug | Master Volume audit | named as the whole difficulty (P_n in λ_n = A_n − P_n) | the prime-side diagnosis, graded ARGUED (structural) | Li / Stieltjes positivity of the μ_k |
| 14 Aug | Postmaster v0.1 | "prime-power Gram matrices are PSD over a positive prime-power measure" | 6 firewalls, including #5 compact-ray and #6 parity | arithmetic Hardy projection (first order) |
| 16 Aug | v0.3 | same | proved: orientation annihilation, compact Euler-ray instability | same |
| 16 Aug | v0.4 (PP18–27) | square-supported Ψ_□; prime–Gamma heat owner | **none carried** | terminal complete monotonicity (safe axis) |
| 16–20 Aug | v0.5–v0.7 | Wilson gate, Weil form, Löwner split | none | Weil / Löwner |
| 21 Aug | v1.0 | "source" = safe-axis formula (9.5) | none | **Widder rungs**; W₂, W₃ certified |
| 9 Sep | v3.0 | same | none | rungs through F^(8) |
| 19 Sep | v5.1 | P(x) in L_Γ − L_P; §155G countermodel; §155H divisors | none | **W₇ ⇝ F^(14)** and L_Γ − L_P ⪰ 0 |

The counts come from marker searches over each manuscript (orientation/Hardy, compact-ray/Cartwright/parity, Widder, Löwner, Weil, von Mangoldt, Euler product, "source"). The table is a reading of those counts plus the quoted passages.

## 3. The twin test on the principal route

**The route.** From §R16, S_ξ(x) = 1/x + G(x) − P(x), and the Löwner matrices of h = x·S must be PSD on every finite node set.

**The twin satisfies the same identity.** It has its own Gamma channel, and its "prime channel" uses the coefficients c(n) of −f′/f:

| n | 2 | 3 | 4 | 6 | 9 | 11 | 12 | 13 | 14 | 19 | 21 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| twin c(n) | +0.197 | **−0.312** | **−1.442** | **+1.936** | **−2.286** | +2.398 | **−0.763** | **−0.729** | **−2.852** | **−2.944** | **+3.290** |
| ζ: Λ(n) | 0.693 | 1.099 | 0.693 | 0 | 1.099 | 2.398 | 0 | 2.565 | 0 | 2.944 | 0 |

The twin's weights are negative at primes and prime powers, and nonzero at composites. Because the twin has off-line zeros, Löwner's theorem guarantees it fails the all-node statement somewhere. So that statement *discriminates in principle*.

**Parity lemma** (PROVED; this is v0.1 firewall #6 and v0.3's orientation annihilation, made exact). Take any real test on real nodes: rungs, Li, Hankel, Löwner or energies. For an off-line folded pair q = q_r ± iη it sees F(q_r + iη) + F(q_r − iη) = 2F(q_r) − η²F″(q_r) + O(η⁴). The first-order term cancels identically, so every finite real test responds at order η² ∝ θ².

**Measured** (COMPUTED):

- **Rungs.** The first failure is at k* = 16,589, and k*·θ² ≈ 0.86, exactly the parity scaling.
- **Löwner / Dobsch, N nodes** (by Dobsch–Donoghue, equivalent to the local N×N Taylor-coefficient matrix at each centre):
  - The twin's matrices are **PSD for every N ≤ 64** at every tested centre.
  - They are indistinguishable from an on-line control (the off-line pair moved onto the line) to a relative 5×10⁻⁶ ≈ θ²/10 at small N.
  - The smallest eigenvalue drops to 10⁻¹⁵ by N ≈ 65. The drop steepens past N ≈ 43, the number of on-line zeros below the off-line one. That fits the picture that a finite certificate must first "annihilate" those zeros, but it doesn't prove it.
  - The exact first failing N is beyond double precision. Colab section D computes it from the exact source formula at 250 digits.

**Resolved at 250 digits** (Colab section D, 27 Sep; COMPUTED). The Taylor coefficients of h came from the twin's exact source formula, so every zero is included. Inertia was read off by symmetric elimination:

| centre x₀ | PSD through | first negative pivot | pivot size |
|---|---|---|---|
| 7124.38 (0.97·\|q₀\|) | N = 100 | **N = 105** | 1.0×10⁻¹⁴¹ |
| 7344.72 (\|q₀\|) | N = 105 | N = 110 | 1.3×10⁻¹⁴⁹ |
| 7565.07 (1.03·\|q₀\|) | N = 105 | N = 110 | 1.2×10⁻¹⁴⁸ |

The deciding pivots are 70–80 orders of magnitude above working precision (about 10⁻²²⁰ after coefficient scaling), so the sign is genuine. Only multiples of 5 were tested, so N* lies in 101–105 at the best centre.

- **The comparison that matters.** An N-node test uses Taylor coefficients up to order 2N − 1, about 210 here. The first failing rung, k* = 16,589, uses derivatives up to order 2k − 1 ≈ 33,000. So the principal route's finite sections detect the twin's first off-line zero with about **160× fewer derivatives** than the rung ladder. Finite certificates on the principal route really do carry information the rungs lack.
- **The price.** The deciding eigenvalue is about 10⁻¹⁴¹ of the matrix scale. A certificate of the same size for ζ would need arithmetic well beyond 150 digits, and it must resolve roughly 2.4× as many nodes as there are zeros below the target height (N* ≈ 105 against 43 zeros below the twin's off-line zero at 85.7).
- **Consistency with the parity lemma.** The off-line contribution is still second order in the displacement, and the Löwner test is still parity-blind in that sense. It succeeds sooner only because an optimal quadratic form concentrates that second-order signal far more efficiently than any single fixed rung.

**Reading.** Finite certificates don't discriminate cheaply on either route. What discriminates lives in the all-order or all-node quantifier. The only argument type not ruled out is one that couples the functional equation with the integers' Euler product.

## 4. Two countermodels bracket the problem

| countermodel | has | lacks | where |
|---|---|---|---|
| Davenport–Heilbronn twin | functional equation, Gamma factor, Dirichlet series, finite order | Euler product (c(n) signed, composite-supported) | Team B (this folder); PP199 qualitatively |
| §155G prime-supported model | positive prime-power weights, PNT envelope, meromorphic Euler product, exact prime prefix | the functional equation | v5.1 Dossier §155G |

Neither half is enough. An RH-strength argument must use both halves jointly. The principal route is "cancellation-first", in v5.1's own words, and so has the right shape. The exact-divisor route and the inception's arithmetic Hardy projection are the two routes that are also first-order in the displacement.

## 5. Proposals for the author (report only; nothing promoted)

1. **Restore two proved rows to the §R25 NO-GO ledger:** v0.3's orientation annihilation and its compact Euler-ray instability theorem. Both were proved and never retired.
2. **Add the twin next to §155G** as the functional-equation-side countermodel, with one sentence and the numbers k* = 16,589, K_sector = 218 and no Löwner failure for N ≤ 64 at double precision.
3. **Re-rank W₇.** Keep (R.4) as EQUIV. Move the W₂–W₇ source certificates from "live frontier" to "finite prefix; parity-blind; the twin passes them".
4. **Put the first-order routes back in front:**
   - The exact-divisor residual (§§155H–J) is one-sided and uses Möbius arithmetic.
   - The inception's one-sided defect L_ξ(c) = Σ_{Im q>0} log|(q+ic)/(q−ic)| changes by 2cη/(|q|² + c²) per upper node, linear in η. v0.1's "next theorem" (an arithmetic Hardy projection) is exactly the missing bridge from source-side data to that first-order object.
5. **Run Colab section D** to pin the twin's first failing Löwner size.

## Files

`dh_twin/lowner.py` (twin and ζ resolvents from the source formula; ζ reproduces λ₁ = 0.02309570896612) · `dobsch.cjs`, `dobsch_compare.cjs`, `dobsch_twin_scan_log.txt` · `lowner_search.py` (first attempt; its ~10⁻¹¹ "negatives" were divided-difference noise and are superseded) · `TEAM_B_long_runs.ipynb` section D.

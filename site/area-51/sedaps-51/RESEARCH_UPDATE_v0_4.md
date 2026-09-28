# 51 SEDAPS v0.4 research update

27 September 2026. Team B pass on the Forge 51 v0.3 release. *Corrected in v0.4.1 (27–28 September): §1 now carries the turn-count qualifier, §2 states the lemma's scope, and §4 cites the known War theorem. New results are in [RESEARCH_UPDATE_v0_4_1.md](RESEARCH_UPDATE_v0_4_1.md).* Exact three-queue card model, with the rule unchanged in `sedaps-core-v0-2.js`. **RH STATUS: OPEN.** There is no zero-data test and no RH inference.

Status labels:
- **PROVED** means a short argument, given below.
- **CERT** means explicit states or deals replayed with the shipped rule alone.
- **COMPUTED** means an exhaustive search that relies on a proved lemma.
- **EVID** means a sampled regularity. It is not a theorem.

## 1. At turn 85, the present has exactly one past from a fair deal

v0.3 certified branch 00, excluded 11 by its prefix floor of 33, and left 01 and 10 open. Both are now closed.

| Bits | Previous sizes | Live | Verdict | Reason | Status |
| --- | --- | --- | --- | --- | --- |
| 00 | 36, 15, 0 | 2 | reachable | the recorded 17–17–17 deal (seed 510053) | CERT |
| 01 | 36, 14, 1 | 3 | excluded | mod-3 clock: the three lengths lie in three different classes mod 3, so no turn works | PROVED |
| 10 | 34, 17, 0 | 2 | excluded at turn 84 | its deepest backward history reaches turn 66; none reaches 65. Fair deals do reach it at turns 24, 27, 30 and 33 (v0.4.1, CERT) | COMPUTED |
| 11 | 33, 17, 1 | 3 | excluded | mod-3 clock at every turn (and the v0.3 prefix floor of 33) | PROVED |

Given the equal start **and the known elapsed turn count 85**, this present therefore determines its immediate past with no extra history bits. This does not establish uniqueness if the elapsed turn count is unknown: then 00 and 10 both come from fair deals, and the leading bit alone recovers the past (v0.4.1). The v0.4 game applies this: "Apply 17-card start + turn 85" now leaves one past.

**The mod-3 clock (PROVED).**
1. A queue that is empty never receives cards again, because only the winner of a turn receives cards.
2. So if all three queues are live at turn s, they were live at every earlier turn.
3. On every such turn each player gives up one card and the winner appends three.
4. Each length therefore changes by −1 or +2, and n_i(s) ≡ 17 − s (mod 3).
5. At s = 84 that residue is 2. Branch 01 has lengths 36, 14, 1 and branch 11 has 33, 17, 1, so both are impossible. Their three lengths are not even congruent to one another, so they are impossible at every turn.

**Branch 10 (COMPUTED).**
- The time-aware shape lemma of §2 prunes the backward search from 10. The search is complete: it expanded 336 states, and no backward history gets below turn 66. This settles turn 84 only; the lemma is turn-indexed. v0.4.1 searches every elapsed turn: fair deals reach 10 at turns 24, 27, 30 and 33 and at no other turn.
- The search's predecessor routine agrees with the shipped `predecessors`.
- The lemma accepted all 384,722 (state, turn) pairs with at least two live queues reached in 300 seeded games. That is an implementation check; the lemma itself is proved.

## 2. The time-aware shape lemma (PROVED)

From a 17–17–17 deal, after s turns:

- **Three queues live.** Each queue is a front of p cards followed by 3-card packets, each packet led by its largest card. Here p = 17 − s while s < 17, and p ≡ 17 − s (mod 3) with p ≤ 2 afterwards. Removing a front card shortens the front or starts on the next packet. Appending a won packet adds a 3-card packet led by the winning card.
- **Two queues live.** Here s ≥ 17. Each live queue is at most 2 front cards, then 3-card packets, then 2-card packets, each led by its largest card.
- **Elimination congruence.** While three are live, n_i(s) = 17 + 3w_i − s, so the first elimination happens at e = 17 + 3w_k. That means e ≡ 2 (mod 3) and e ≥ 17.
- **Scope** (corrected in v0.4.1, after PP275). The lemma speaks only about states with at least two live queues. A terminal state, in which one queue holds all 51 cards, fails the test by construction yet is reachable. The backward search never tests one, because every legal predecessor has at least two live queues. The full necessity proof is in v0.4.1 §1.1.

`sedaps-lemma-v0-4.js` implements the lemma and the backward search. It runs in the browser and in `verify-sedaps-v0-4.cjs`.

## 3. Four is the true maximum among reached states (CERT)

v0.3 left open whether the four-predecessor maximum is attained inside the equal-deal reachable class. It is attained. Five presents (turns 32, 35, 41, 50 and 53) have all four legal pasts reached from four different 17–17–17 deals. `dstart4-certificates-v0-4.json` lists each deal, and the verifier replays every one with the shipped rule.

Supporting samples (COMPUTED, 27 Sep):
- 2,518 of 3,000 seeded deals reach a present with four legal pasts. The earliest is at turn 17 and the median at turn 72.
- Among the 400 earliest such presents at turns ≡ 2 (mod 3), the number of pasts reachable from a fair deal is 1, 2, 3 or 4 in 137, 240, 18 and 5 cases.

## 4. The periodic remnant (EVID)

A game has finitely many states, so a game that never ends must repeat.

- **Seeded deals.** Of 2,000 seeded 17–17–17 deals, 348 end, with a median end at turn 97. The other 1,652 fall into a loop. Every loop has two live queues, and each queue wins exactly half the turns of the loop.
- **Loop lengths.** Only 12 lengths occur: 312, 520, 624, 780, 1,196, 1,716, 2,184, 2,964, 3,276, 3,536, 3,744 and 4,004. Their gcd is **52 = 51 + 1**.
- **The turn-85 present** enters a loop at turn 356 with period 3,744 = 52 × 72.
- **The four-for-four presents** loop with periods 780, 4,004, 4,004 and 3,276. The fifth, at turn 50, ends at turn 70.
- **Deck sizes** (300 seeded deals each, cards numbered by strength):

| n cards | 7 | 9 | 11 | 13 | 15 | 17 | 21 | 27 | 33 | 39 | 45 | 51 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gcd of loop lengths | 8 | 10 | 12 | 14 | 16 | 18 | 22 | 28 | 34 | 40 | 46 | 52 |

- **Even decks.** At n = 6, 8, 12, 24, 30 and 48, no deal looped. At n = 10, 14 deals looped, all with period 60, which is not a multiple of 11. At n = 20, one deal looped, with period 672 = 21 × 32.

**Update (v0.4.1).** This is known mathematics for loops with two live queues. With two queues left, the rule is War with the winning card placed first. For an odd deck, Spivey (*Cycles in War*, INTEGERS 10, 2010, Thm 6) shows that its cycles alternate winners. Alternation forces the period 2·lcm(α/2, (n+1)/2, (n−1−α)/2), where α is even, and that is always a multiple of n + 1 (proof in v0.4.1 §2). Complete censuses of every state for n ≤ 11 confirm it: every loop has two live queues, and the only lengths are 6, 8, {20, 30} and {12, 24} for n = 5, 7, 9 and 11. **Open:** a loop in which all three queues stay live (none exists for n ≤ 11).

Compare Volume I's trapped tip: the silver cascade leaves an exact rational void, 1/28 of the cone. The two results share a shape (a long process leaves a clean remnant) but not the mathematics.

## 5. Files

| File | What it is |
| --- | --- |
| `sedaps-lemma-v0-4.js` | shape lemma, mod-3 clock, backward search, start verdicts (browser and Node) |
| `sedaps-v0-4.js` | game script; v0.3 files are unchanged and retained |
| `dstart4-certificates-v0-4.json` | five four-for-four presents with their four deals |
| `verify-sedaps-v0-4.cjs` | replays everything above; `--decks` adds the deck-size sweep; writes `VERIFY_v0_4.json` |
| `/area-51/twins-51/` | the 51 Twins exhibit: plates II–IV draw these results |

Open:
- a loop with three live queues at odd n (none for n ≤ 11, but they exist at n = 12; the n + 1 divisibility of two-live loops is settled in v0.4.1);
- the four-player rules;
- the count |H_t(x)| of complete histories ending at a present, a Colab candidate.

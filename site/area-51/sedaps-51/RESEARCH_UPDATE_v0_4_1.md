# 51 SEDAPS v0.4.1 research update

27–28 September 2026. Team B (Track B), continuing the v0.4 pass. The rule is unchanged (`sedaps-core-v0-2.js`). **RH STATUS: OPEN.** There is no zero-data test and no RH inference.

Status labels are those of v0.4: **PROVED** (short argument given), **CERT** (explicit states or deals replayed with the shipped rule), **COMPUTED** (exhaustive search, relying on a proved lemma), **EVID** (sampled regularity).

This update answers the two open items raised in PP271 (Blue Team, 27 Sep), which was written against the v0.3 files. PP271's mod-3 clock and its elimination corollary are the v0.4 §1 clock and §2 congruence. The two derivations are independent and agree.

## 1. The turn count is part of the filter

v0.4 searched past 10 at turn 84 only. Its shape lemma is turn-indexed, so a verdict at one turn says nothing about another. Here every elapsed turn is searched.

| Bits | Sizes | Reached from a 17–17–17 deal at elapsed turn s | Status |
| --- | --- | --- | --- |
| 00 | 36, 15, 0 | s = 84 (the recorded deal, seed 510053) | CERT |
| 01 | 36, 14, 1 | never: three live queues in three residue classes mod 3 | PROVED |
| 10 | 34, 17, 0 | **exactly s = 24, 27, 30 and 33** | CERT for those four turns; COMPUTED for the rest |
| 11 | 33, 17, 1 | never: three residue classes (and the prefix floor 33 > 17) | PROVED |

- **Certificates.** `past10-certificates-v0-4-1.json` holds one 17–17–17 deal for each of the four turns, with SHA-256 digests of the deal, of past 10 and of the present. The verifier replays each deal with the shipped rule alone. The first turn is large as a set: 24,310 = C(17, 8) distinct deals reach past 10 at turn 24.
- **Exclusion at every other turn.** A complete backward search under the proved shape lemma runs from every turn s = 17 … 84. Two-live states need s ≥ 17. No search except the four above reaches a deal.
- **Closure.** At turns t ≥ 17, the lemma depends on t only through t mod 3. From s = 82, 83 and 84 no search checks a state below turn 17: the deepest surviving state is at turn 18 or later, and its predecessors are checked one turn lower. So each search from s + 3 is the same tree shifted by three turns, and the verdict is 3-periodic for every later turn.
  - The 3-periodicity is the mod-3 clock: beyond the threshold t ≥ 17, the lemma reads t only through the all-live residue (17 − t) mod 3. So the closure is a proof by finite search plus induction, not merely a property of one run.
  - **The clock and the search do different jobs** (PP272 §1). The clock alone cannot exclude turn 84 for past 10, since 24, 27, 30, 33 and 84 are all ≡ 0 (mod 3); only the turn-indexed search excludes it. Conversely, the clock closes 01 and 11 at every turn with no search at all.
- **Two implementations agree.** The shipped `SedapsLemma.explore` (`verify-past10-v0-4-1.cjs`) and an independent Python restatement (`independent/sedaps_independent.py`) give the same four turns.
- **Blue Team returns.** PP274 replayed the four certificates. PP275 ported the search to Python separately and reproduced the turn-84 exclusion with identical figures: 336 states expanded, lowest turn 66, not capped. Both halves now have an independent second return, and the Blue Team grades the zero-bit reading A-CAT (certified).

**Consequences for the turn-85 present.**
- *Turn count known:* exactly one past comes from a fair deal, so **zero history bits** are needed. This is the v0.4 claim, now with its qualifier.
- *Turn count unknown:* 00 and 10 both come from fair deals, so |Pre(x) ∩ R| = 2. They differ in the leading bit, so **one bit recovers the past**. PP271 asked for this `= 2` to be frozen as a certificate; it now is.
- The same present is also reached from fair deals at turns 25, 28, 31 and 34, through past 10.

This is the R versus R_t distinction PP271 asked for. The game knows its own turn count, so it may use the stronger, turn-indexed filter R_t. PP272 corrected PP271's one-bit reading to zero bits once the certificate existed, and PP274–PP275 supplied the second returns.

### 1.1 Why the search is a proof (PROVED)

**Theorem.** Let y have at least two live queues. If `explore(y, s)` finds no 17–17–17 deal and is not capped, then no 17–17–17 deal reaches y at elapsed turn s.

The hypothesis on y cannot be dropped: a terminal state is reachable, yet fails the test at once, so `explore` would report it excluded. For example, seed 5 of the v0.4 generator ends at turn 117 with sizes 0, 0, 51, and `explore` on that state returns no deal. PP276 found the same case with its own generator. The hypothesis holds in every use here. `startVerdicts` and `verify-past10-v0-4-1.cjs` call `explore` only on legal predecessors, and every predecessor has at least two live queues: each queue in the turn's live set A gets its pot card back, and |A| ≥ 2. (Checked: 135,578 predecessors emitted along 300 seeded games, none with fewer than two live queues; PP276 found 0 of 2,478.)

The proof rests on two facts.

**(a) The predecessor list is complete.** Suppose x has at least two live queues and its turn produces y. The turn's live set A contains every live queue of y and has at least two members. The winner w is live in y. The last |A| cards of y[w] are the pot, the winning card first, and that card is the largest in the pot. `preds(y)` runs through every such (A, w) and rebuilds x uniquely: each player in A takes its pot card back to its front, and w also loses the pot from its tail. Conversely, every x it rebuilds does produce y, because the rebuilt fronts are exactly the pot cards and the largest of them sits in w. So `preds(y)` is exactly the set of legal predecessors. It agrees with the shipped `SedapsCore.predecessors`.

**(b) The shape test is necessary on states with at least two live queues.** Let x be reached from a 17–17–17 deal after s turns, with at least two live queues.
1. *Once empty, always empty.* Only live queues play, and only the winner, which is live, receives cards. So the number of live queues never rises. A queue live at turn s was live at every earlier turn and played one card on each of the s turns.
2. *Pot size equals the live count.* Each pot holds the cards played on that turn: 3 while three queues are live, 2 afterwards. It is appended with the winning card, the largest, first.
3. So a queue live at turn s consists of its 17 dealt cards followed by the pots it won, in order, with the first s cards removed.
   - *All three live.* Every pot so far has 3 cards. If s < 17, the queue is its last 17 − s dealt cards, then whole 3-packets. If s ≥ 17, the dealt cards are gone and s − 17 packet cards have been played. What remains is the last p = (17 − s) mod 3 cards of one packet, then whole 3-packets. This is the first branch of `shapeOK`.
   - *Exactly two live.* The first queue to empty held one card at the turn before, while three were live. By the first branch that turn t satisfies p(t) = 1, so t ≥ 16 and the elimination turn is at least 17. (The sharper congruence of v0.4 §2, e = 17 + 3w ≡ 2 (mod 3), derived independently in PP271 §4, is not needed here.) Hence s ≥ 17 and the dealt cards are gone. The queue's pots are a run of 3-packets followed by a run of 2-packets. Removing the first s − 17 of those cards leaves at most 2 cards of one packet, then whole 3-packets, then whole 2-packets, each led by its largest card. This is the second branch of `shapeOK`.

*Proof of the theorem.* Suppose some deal reached y at turn s. Its history x₀, …, x_s = y is a chain of legal predecessors. Each x_j with j < s has at least two live queues because it has a successor, and x_s = y has at least two by hypothesis. So by (b) every state in the chain passes the test at its own turn. By (a) the search meets every one of them; its memo on (turn, state) only skips subtrees already explored. So the search finds the deal. An uncapped search that finds none proves that no deal reaches y at turn s. ∎

**Scope correction (PP275).** The v0.4 lemma header said "a state failing the test at turn s is unreachable at turn s". That is false for terminal states: one queue holding all 51 cards is reachable and fails the test by construction. The search never tests such a state, since it has no successor and so is never a predecessor. The header now carries the scope "at least two live queues"; the code is unchanged. The v0.4 verifier's own sweep was already restricted to states with at least two live queues.

Replay of the scope (COMPUTED, `verify-past10-v0-4-1.cjs` check 5, v0.4 deal generator). Over 2,000 seeded deals played to their end, or to turn 6,000:
- all 9,949,705 (state, turn) pairs with two or three live queues pass;
- exactly 348 pairs fail, and they are the terminal states of the 348 deals that end.

PP275's independent sweep found the same pattern: 58 failures in 102,900 pairs, every one terminal. The two counts are the same finding at different budgets: in both, every failure is a terminal state and nothing else fails. (The v0.4 verifier's 384,722 pairs over 300 deals differ from a 300-deal run of this sweep only by counting turns t < 1,500 rather than t ≤ 1,500: one pair for each of the 253 deals that reach the cap. PP276 reconciles all three counts.)

PP276 also replayed every predecessor that `preds` emits over 13,830 reachable states: 5,355 emitted, none spurious, none missing and none extra against the shipped routine. So dropping the replay check in (a) costs nothing, as the argument says.

### 1.2 Exact history counts (PROVED formula, COMPUTED counts)

Fork-A asked for the exact number of equal-deal histories at the turn-32 present (its work packet A); its own search stopped at a 250,000-state cap. Forward play is deterministic, so a history is fixed by its deal, and the backward histories of a present form a tree. The count is the number of 17–17–17 deals whose play reaches the present at that turn.

**Proposition (PROVED).** Let z be a state at turn t ≤ 16 that passes the shape test with all three queues live. Then each queue is its last 17 − t dealt cards followed by a, b and c whole 3-packets, with a + b + c = t, and exactly

  **t! / (a! b! c!)**

17–17–17 deals reach z at turn t. In particular every such z is reachable: below turn 17 the shape test is sufficient as well as necessary.

*Proof.* The card count gives 3(17 − t) + 3(a + b + c) = 51, so a + b + c = t. Take a legal predecessor that passes the test at turn t − 1. Its turn had all three queues live, so its winner w lost its pot, the last three cards of z[w]. If w has no packet, those are dealt cards, and removing them leaves w with 15 − t cards, fewer than the 18 − t the test needs at turn t − 1. So w has a packet and the pot is its last packet. Conversely, for each queue w with a packet, returning that packet's cards to the fronts (the winner's card to w, the others in seat order) gives a legal predecessor that passes the test. Its winning card is the packet's head, which is its largest card. So the predecessors correspond exactly to the queues with a packet, and each one lowers that queue's count by one. The number N(a, b, c) of deals below z therefore satisfies

  N(a, b, c) = N(a − 1, b, c) + N(a, b − 1, c) + N(a, b, c − 1),

dropping any term with a negative count, with N(0, 0, 0) = 1: at turn 0 every queue holds its 17 dealt cards. The multinomial coefficient satisfies the same recursion and the same start. ∎

Above turn 17 the tree is searched with the shape test, which §1.1 shows skips no history. Each three-live state it meets at turn 16 or below is then counted by the formula. `count-histories-v0-4-1.cjs` does this and writes `HISTORY_COUNTS_v0_4_1.json`.

| Present | Deals reaching it | 00 | 01 | 10 | 11 |
| --- | ---: | ---: | ---: | ---: | ---: |
| turn 32 | **484,731,472** | 77,014,080 | 179,358,976 | 24,504,480 | 203,853,936 |
| turn 35 | 266,342,128 | 54,493,296 | 175,092,112 | 18,378,360 | 18,378,360 |
| turn 41 | 4,376,374,600 | 2,633,897,448 | 1,671,141,888 | 71,062,992 | 272,272 |
| turn 50 | 77,430,403,880 | 3,035,825,388 | 33,385,199,692 | 5,471,721,320 | 35,537,657,480 |
| turn 53 | 264,906,968,790 | 32,672,640 | 66,411,520 | 13,051,046,778 | 251,756,837,852 |
| turn 85 | 69,150,842,132 | all of them | 0 | 0 | 0 |

For past 10 of the turn-85 present, the deals at turns 24, 27, 30 and 33 number 24,310 = C(17, 8), 97,240, 1,361,360 and 8,751,600.

- The four pasts of each four-for-four present sum to the present's count. Every past is reached by at least one deal, as the v0.4 certificates show.
- A deal-by-deal enumeration, with no formula, reproduces five of these counts exactly (`--brute`): past 10 of the turn-85 present at turns 24–33, and all 24,504,480 deals behind past 10 of the turn-32 present.
- "Four certified pasts" and "hundreds of millions of histories" are both true of the turn-32 present. The first counts one-step predecessors, the second counts complete histories.

## 2. Loops: the period theorem for two live queues

With the third queue empty, the rule is two-player War: the higher card wins, and the winner puts its own card on the bottom and then the loser's. Spivey studies exactly this game (M. Z. Spivey, *Cycles in War*, INTEGERS 10, 2010, #G02). For an odd deck his Theorem 6 characterizes the cycles. In them the players win alternately, and each pile alternates between cards that never lose and cards that always lose. That summary is taken from OEIS A400411 and its companion code; the paper itself could not be opened from this environment.

**Proposition (PROVED).** Take a loop with two live queues holding all n cards, n odd, whose winners alternate. Let α be A's length just before its winning turns. Then α is even, and the loop length is

  **L = 2 · lcm(α/2, (n+1)/2, (n−1−α)/2)**, always a multiple of n + 1.

*Proof.* Let A win the even turns and B the odd ones. Lengths then alternate between (α, n−α) and (α+1, β), where β = n−α−1. Over two turns every card moves to a new position by the same map σ, whatever the card values are. Write A[i] and B[j] for positions, with 0 at the front, at even times:

- A[i] goes to A[i−2] for i ≥ 2;
- A[0] goes to A[α−2], and A[1] goes to B[β];
- B[j] goes to B[j−2] for j ≥ 2;
- B[0] goes to A[α−1], and B[1] goes to B[β−1].

*If α is even,* then β is even too, and σ splits into three cycles:
- the even A positions, a cycle of length α/2;
- the odd A positions together with the even B positions, a cycle of length α/2 + β/2 + 1 = (n+1)/2;
- the odd B positions, a cycle of length β/2.

The cards are distinct and fill all n positions, so the state recurs after 2k turns exactly when σᵏ is the identity. That gives the formula. Cards in the first and third cycles are always played by the turn's winner; cards in the middle cycle always lose.

*If α is odd,* σ is a single n-cycle. The top card then reaches B[0] at an even turn, where B must lose, which is impossible. ∎

**The 51-card game.** Put a = α/2 for 1 ≤ a ≤ 24. Then L = 2·lcm(a, 26, 25 − a).
- L(α) = L(n − 1 − α) identically, since the first and third lcm arguments swap. So a ≤ 12 suffices.
- L therefore takes **exactly 12 values**, the predictions of the proved formula.
- They coincide with the 12 lengths observed among the 2,000 seeded deals, with none missing and none extra:

| α | a = α/2 (or 25 − a) | L = 2·lcm(a, 26, 25 − a) | loops among 2,000 seeded deals |
| --- | --- | ---: | ---: |
| 2 or 48 | 1 | 624 | 4 |
| 4 or 46 | 2 | 1,196 | 10 |
| 6 or 44 | 3 | 1,716 | 54 |
| 8 or 42 | 4 | 2,184 | 73 |
| 10 or 40 | 5 | 520 | 121 |
| 12 or 38 | 6 | 2,964 | 127 |
| 14 or 36 | 7 | 3,276 | 166 |
| 16 or 34 | 8 | 3,536 | 181 |
| 18 or 32 | 9 | 3,744 | 245 |
| 20 or 30 | 10 | 780 | 202 |
| 22 or 28 | 11 | 4,004 | 231 |
| 24 or 26 | 12 | 312 | 238 |

- The twelve lengths are 52 × 6, 10, 12, 15, 23, 33, 42, 57, 63, 68, 72 and 77. These multipliers have gcd 1, so the observed gcd 52 is exact, not merely a common factor (PP276).
- The turn-85 present's period 3,744 is a = 9.
- The four-for-four presents' periods 780, 4,004 and 3,276 are a = 10, 11 and 7.

**Complete censuses (COMPUTED).** `independent/census2.c` stores two bits per state and checks every state, not just deals.

| n | states (3-queue rule) | loops | loop lengths | loops with 3 live queues |
| --- | ---: | ---: | --- | ---: |
| 5 | 2,520 | 12 | 6 | 0 |
| 7 | 181,440 | 312 | 8 | 0 |
| 9 | 19,958,400 | 2,016 | 20, 30 | 0 |
| 11 | 3,113,510,400 | 333,552 | 12, 24 | 0 |
| 3, 4, 6, 8 | all | 0 | — | — |
| 10 | 239,500,800 | 288 | 60 | 0 |

- **Two-queue War.** No cycles at n = 12 (5.27 × 10⁹ states).
- **Alternation and the formula.** Every two-queue loop for n ≤ 11 alternates winners, has even α, and matches the formula exactly.
- **Cross-check.** The same program counts the never-ending alternate deals of two-player War as 30, 2,304, 218,680, 395,940 and 28,223,770 for n = 5, 7, 9, 10 and 11. This is OEIS A400411.
- **Even decks.** The absence of loops at 3, 4, 6, 8 and 12 fits the published pattern: cycles are constructed for every n that is not 2ᵏ or 3·2ᵏ.

**What stays open.** With two live queues, the period theorem settles the n + 1 divisibility. For the three-queue rule as a whole it would follow from one more fact: that no loop keeps all three queues live. **That fact is false in general.** It holds for every n ≤ 11, over the whole state graph, and fails at n = 12 (CERT):

  A = 6 0 1, B = 2 10 7 3, C = 4 8 11 5 9 (front card first)

returns to itself after 9 turns.
- The winners rotate A, B, C, A, B, C, A, B, C.
- The queue lengths cycle (3, 4, 5) → (5, 3, 4) → (4, 5, 3).
- 9 is not a multiple of 13. But 12 is even, and the n + 1 pattern was only ever claimed for odd decks.

**Fair deals do not reach these loops (PROVED + COMPUTED).**
- On a three-live turn the sizes change by (+2, −1, −1). Since +2 ≡ −1 (mod 3), all three sizes move together mod 3, so whether they are pairwise congruent is invariant along any trajectory. This is the mod-3 clock of v0.4 §1, for an equal deal of any size 3m.
- An equal deal has congruent sizes, so every three-live state it reaches has them too, and so does every loop it could enter.
- Every three-live loop at n = 12 has pairwise incongruent sizes: (3, 4, 5) up to rotation for length 9, and (3, 5, 4) for length 60. So no 4–4–4 deal reaches one.
- Two exhaustive checks agree:
  - `live3_loops.c 12 0 1 cong` plays every packet-form state with congruent sizes, and all 514,483,200 of them lose a queue within 20 turns;
  - PP282 walks every congruent-size three-live state at n = 12 (3.03 × 10⁹ after its one-third reduction), with no shape assumption, and all of them lose a queue within 25 turns.

So the ledger carries **two claims**, and n = 12 separates them. "No three-live loop in the state graph" is false at 12. "No three-live loop reachable from an equal deal" holds through n = 12 and is OPEN at 51, where none was seen in 2,000 seeded deals (EVID). PP282 found the same loops independently: its witness, a 3-turn transient into a period-9 loop, belongs to the length-9 family above.

A census of 1.8 × 10⁹ states (PP281, n = 11) predicted no loop at the next size and was wrong. That is a small, checkable example of the firewall: a finite search, however large, is not an all-n theorem.

**Packet form on a loop (PROVED).** Call a three-live state *packet form* when each queue is the tail of one packet (0, 1 or 2 cards) followed by whole 3-card packets, each led by its largest card.

1. *Every state on a three-live loop is in packet form.*
   - Let the loop have length L, and fix a state x on it. Over L turns each queue plays one card per turn, so queue i plays its first L cards in order and receives cards only at its tail.
   - If L were smaller than |xᵢ|, then after L turns the queue would begin with its card xᵢ[L]. Since the state is x again, that card would equal xᵢ[0], one card in two positions, which is impossible because the cards are distinct.
   - So L ≥ |xᵢ| for every queue, and within one period every card present at x is played. After the period, queue i holds only cards appended during it. Those were appended as 3-packets, each led by its largest card, and the pops have removed a prefix. What is left is the tail of one packet followed by whole packets.
   - That state is x, so x is in packet form. This holds on the whole state graph, with no reachability assumption.
2. *A turn that leaves all three queues live maps packet form to packet form.* Playing a front card shortens the partial tail, or turns a whole packet into a 2-card tail. The winner appends a new packet led by its largest card.

So a three-live loop exists if and only if some packet-form state never loses a queue. `independent/live3_packet.c` enumerates every packet-form state of n cards and plays each one until a queue empties:

| n | packet-form states | three-live loops | most turns before a queue empties |
| --- | ---: | ---: | ---: |
| 3–7 | 6; 72; 480; 2,880; 21,840 | 0 | 1, 1, 2, 3, 4 |
| 8 | 174,720 | 0 | 8 |
| 9 | 1,344,000 | 0 | 8 |
| 10 | 12,096,000 | 0 | 11 |
| 11 | 119,750,400 | 0 | 15 |
| 12 | 1,153,152,000 | **1,145,664**: 1,036,800 of length 9 and 108,864 of length 60 | 20 |
| 13 | 12,454,041,600 | 0 | 26 |

The next odd size, n = 13, again has no three-live loop anywhere in the state graph: all 12,454,041,600 packet-form states lose a queue within 26 turns. So loops keeping three queues live occur at 12 cards, but not at 13 or at 11 or fewer.

At n = 12, the 15,863,040 packet-form states that lie on loops are exactly 9 × 1,036,800 + 60 × 108,864, so the loop count balances. Each loop is counted once, at its lexicographically smallest state. The program classifies every state as losing a queue, lying on a loop, or entering one, using Brent's cycle detection (`independent/live3_loops.c`).
- **Independent returns.** PP281 ran an unrestricted census of every three-live state with the global maximum in queue 0. That is an exact one-third reduction by seat rotation, and it uses no shape assumption. It covers n ≤ 11 (1,796,256,000 states at n = 11), finds no loop, and gives worst exit times 2, 4, 5, 10, 11, 15 and 19 for n = 5–11. It also reproduces the packet-form counts above for n ≤ 8 from its own shape predicate. The complete census of `census2.c` (every state, three queues, n ≤ 11) is a third method.
- PP281 §3 read the lemma as needing reachability from a fair deal. The distinct-card argument in step 1 shows it does not: the census result holds on the whole state graph.
- A census that finds nothing constrains nothing beyond its range, and n = 12 shows why that matters: the pattern of n ≤ 11 does not continue. For odd n ≥ 13, and at 51, three-live loops are OPEN.


Three exact facts narrow any three-live loop. None of them is a proof that such a loop cannot exist.

1. **Balanced winners** (PP273). On a three-live turn each length changes by −1, +2 for the winner. Closing a loop of length L forces each queue to win exactly L/3 turns, so 3 | L. PROVED.
2. **Queue maxima never lose** (Team B; this strengthens PP273's "the top card never changes queue").
   - A queue receives cards only on turns it wins. Every card in that pot is below the winning card, which was already in the queue. So a queue's maximum card can never increase, and it drops only when that card loses.
   - On a loop the maximum is periodic and non-increasing, hence constant. So **in every loop, each live queue's maximum card wins whenever it is played**. PROVED.
   - In a three-live loop, the three queue maxima are therefore never played on the same turn. In two-queue War this is the "cards that never lose" half of Spivey's description.
3. **Fair-deal loops** (PP273, via the clock). A three-live loop reachable from a 17–17–17 deal has three lengths congruent mod 3. Its queues are then packet-synchronised: all three play packet heads on the same turns. PROVED; this cuts the candidates by about two thirds.

"No three-live loop exists" and "no three-live loop is reachable from a fair deal" are different claims; the second is the one the game needs.

## 3. Independent replays

| Check | Result |
| --- | --- |
| v0.3 certificate, seed 510053, 85 turns | replays |
| 20 deals of the five four-for-four presents | all replay; the stated four predecessors are the full legal set |
| forward fates | turn 85: loop from turn 356, period 3,744; turn 32: period 780 |
| remnant, 2,000 seeded deals (same generator, ported) | 348 end, 1,652 loop, gcd 52, same 12 lengths and counts |
| turn-indexed scan of past 10 | deals at 24, 27, 30, 33 only |

## 4. Files

| File | What it is |
| --- | --- |
| `past10-certificates-v0-4-1.json` | four 17–17–17 deals reaching past 10, with SHA-256 digests |
| `verify-past10-v0-4-1.cjs` | shipped-rule replay, full turn scan and the lemma-scope sweep (§1.1); writes `VERIFY_v0_4_1.json` |
| `count-histories-v0-4-1.cjs`, `HISTORY_COUNTS_v0_4_1.json` | exact history counts (§1.2) |
| `independent/` | Python replay, census programs, receipts (see its README) |

## 5. Status ledger

| Claim | Status |
| --- | --- |
| 01 and 11 unreachable from every equal deal, at every turn | PROVED |
| Past 10 reached from equal deals exactly at turns 24, 27, 30, 33 | CERT (the four turns) + COMPUTED (exclusion elsewhere); second returns PP274, PP275 |
| Turn-85 present: one fair past given the turn count; two without it; one bit suffices | CERT + COMPUTED; Blue Team A-CAT |
| The shape test is necessary on states with at least two live queues; the backward search is complete for such a start state | PROVED (§1.1); audited in PP276 |
| "A state failing the test is unreachable", for terminal states | false as first written; scope corrected |
| Below turn 17, a three-live state passing the shape test is reached by exactly t!/(a! b! c!) deals | PROVED (§1.2) |
| Exact history counts of the six certified presents (turn 32: 484,731,472) | COMPUTED (§1.2) |
| Alternating two-queue loops have L = 2·lcm(α/2, (n+1)/2, (n−1−α)/2), a multiple of n + 1 | PROVED |
| Odd-deck War cycles alternate winners | published (Spivey 2010, Thm 6); COMPUTED for n ≤ 11 |
| In every loop each live queue's maximum card never loses; three-live loops have balanced winners | PROVED |
| Every state on a three-live loop is in packet form; packet form is preserved while three queues live | PROVED (§2) |
| No loop in the state graph keeps three queues live | COMPUTED for n ≤ 11 (two methods; PP281 second seat) and for n = 13; **false at n = 12** (CERT: 1,145,664 loops, of lengths 9 and 60; PP282 witness); OPEN for n ≥ 14 |
| Pairwise congruence of the three sizes mod 3 is invariant while three are live | PROVED |
| No three-live loop is reachable from an equal deal | COMPUTED through n = 12 (two methods); OPEN at 51 |
| Four-player rules; the count \|H_t(x)\| | OPEN |

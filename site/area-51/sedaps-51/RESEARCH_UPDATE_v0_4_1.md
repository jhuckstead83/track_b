# 51 SEDAPS v0.4.1 research update

27–28 September 2026 (§2 extended 28 September for v2.8.6). Team B (Track B), continuing the v0.4 pass. The rule is unchanged (`sedaps-core-v0-2.js`). **RH STATUS: OPEN.** There is no zero-data test and no RH inference.

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

## 2. Loops: period theorems for two live queues and for rigid three-live loops

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

- These are laws of two-queue loops. Loops that keep three queues live follow their own formula (below), and at 51 cards 23 of their 29 rigid periods are not multiples of 52.
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

**What stays open.** With two live queues, the period theorem settles the n + 1 divisibility. For the three-queue rule as a whole it would follow from one more fact: that no loop keeps all three queues live. **That fact is false in general.** It holds for every n ≤ 11, over the whole state graph, and fails at n = 12 (CERT) and at every multiple of 3 above it, 51 included (PROVED, construction below). The first failure:

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

So the ledger carries **two claims**, and n = 12 separates them. "No three-live loop in the state graph" is false at 12, and at every multiple of 3 from there up, 51 included. "No three-live loop reachable from an equal deal" holds at 9, 12 and 15 cards (complete searches) and is OPEN at 51, where none was seen in 2,000 seeded deals (EVID). PP282 found the same loops independently: its witness, a 3-turn transient into a period-9 loop, belongs to the length-9 family above.

A census of 1.8 × 10⁹ states (PP281, n = 11) predicted no loop at the next size and was wrong. That is a small, checkable example of the firewall: a finite search, however large, is not an all-n theorem. A second example: every loop the 2,000 seeded deals reach has a length divisible by 52. That is true of everything those samples can reach, which are two-queue loops, where it is proved. It is false of three-live loops at 51 cards, and 3 of the first 19 three-live periods found happened to be multiples of 52 anyway (PP287). A pattern confirmed by sampling is a fact about the sample.

**Packet form on a loop (PROVED).** Call a three-live state *packet form* when each queue is the tail of one packet (0, 1 or 2 cards) followed by whole 3-card packets, each led by its largest card.

1. *Lemma: a loop is never shorter than its queues, so every state on a three-live loop is in packet form.* (PP283 grades this A, withdrawing PP281 §3.)
   - Let the loop have length L, and fix a state x on it. Over L turns each queue plays one card per turn, so queue i plays its first L cards in order and receives cards only at its tail.
   - If L were smaller than |xᵢ|, then after L turns the queue would begin with its card xᵢ[L]. Since the state is x again, that card would equal xᵢ[0], one card in two positions, which is impossible because the cards are distinct.
   - So L ≥ |xᵢ| for every queue, and within one period every card present at x is played. After the period, queue i holds only cards appended during it. Those were appended as 3-packets, each led by its largest card, and the pops have removed a prefix. What is left is the tail of one packet followed by whole packets.
   - That state is x, so x is in packet form. This holds on the whole state graph, with no reachability assumption.
2. *A turn that leaves all three queues live maps packet form to packet form.* Playing a front card shortens the partial tail, or turns a whole packet into a 2-card tail. The winner appends a new packet led by its largest card.

So a three-live loop exists if and only if some packet-form state never loses a queue. The lemma is what makes a packet-form census a complete search for loops. `independent/live3_packet.c` enumerates every packet-form state of n cards and plays each one until a queue empties:

| n | packet-form states | three-live loops | most turns before a queue empties |
| --- | ---: | ---: | ---: |
| 3–7 | 6; 72; 480; 2,880; 21,840 | 0 | 1, 1, 2, 3, 4 |
| 8 | 174,720 | 0 | 8 |
| 9 | 1,344,000 | 0 | 8 |
| 10 | 12,096,000 | 0 | 11 |
| 11 | 119,750,400 | 0 | 15 |
| 12 | 1,153,152,000 | **1,145,664**: 1,036,800 of length 9 and 108,864 of length 60 | 20 |
| 13 | 12,454,041,600 | 0 | 26 |

The census at n = 13 is also complete: all 12,454,041,600 packet-form states lose a queue within 26 turns, so no loop of any kind keeps three queues live at 13 cards.

**The structure of the loops, and why equal deals cannot reach them.**

*Phase lemma.* In packet form, a queue plays a packet head exactly when its size is divisible by 3. On a three-live turn every size changes by −1 (mod 3), so the pattern of residues only shifts. The sizes are pairwise congruent exactly when all three queues play heads on the same turns ("synchronised"), and pairwise distinct exactly when one queue plays a head on each turn.

Call a loop *rigid* when the winning card is always a packet head.

*Every loop at n = 12 is rigid.* Two methods agree.
- `live3_struct.c` checks all 1,145,664 loops. On every turn exactly one queue plays a packet head, and that head wins. So the winners rotate, each queue winning every third turn, and the sizes run through the rotations of (5, 4, 3).
- `live3_rigid12.c` works from the other end. It enumerates every state of rigid shape: tails 0, 1 and 2, one whole packet per queue, and any head set containing the top card 11. That is 718,502,400 states. It plays each one while the head wins. It finds 15,863,040 states on rigid loops, in 1,036,800 loops of length 9 and 108,864 of length 60. These are exactly the census totals, so every loop at 12 cards is rigid.
- PP283 §1 reported the same split from a third enumerator.
- By head set, {9, 10, 11} carries 725,760 loops of length 9 and all 108,864 of length 60. The head sets {8, 10, 11}, {7, 10, 11} and {6, 10, 11} carry 241,920, 60,480 and 8,640 loops of length 9. So the length-60 loops occur only when the heads are the three top cards (PP287 §3).

**Theorem (PROVED).** On a rigid three-live loop the three sizes are never pairwise congruent mod 3. So no equal deal reaches such a loop, for any n.

*Proof.* Over one period of length L, each queue plays one packet head every three turns, so there are L head plays in all. There are also L wins, and each is by a head, so every head that is played wins. Two heads played on the same turn cannot both win, so exactly one head is played on each turn. By the phase lemma the residues are then pairwise distinct. An equal deal starts with congruent sizes, and congruence is invariant (the mod-3 clock). ∎

- The winners of a rigid loop rotate. The queue playing the head has size ≡ 0 before its win and ≡ 2 after it, while the other two step down to ≡ 0 and ≡ 1. So queue i wins every third turn, and its sizes cycle xᵢ + 2, xᵢ + 1, xᵢ, where each xᵢ ≡ 0 (mod 3) and xᵢ ≥ 3. Hence n = x_A + x_B + x_C + 3 is divisible by 3, and n ≥ 12.
- PP283 §3 derived 3 | n for every loop in which each queue wins every third turn. That assumed equal post-win sizes, and PP284 withdrew it. In general Σ(post-win size) = n + 3, which constrains nothing mod 3. So n = 13 was a genuine candidate, and the complete census above excludes it.

**Two theorems, one union (PP285 §1).** PP284 proves a companion statement that does not ask heads to win. If the gaps are uniform and the post-win sizes are equal to a, the sizes are a, a − 1 and a − 2: three consecutive integers, never congruent.

| | hypothesis | conclusion |
| --- | --- | --- |
| rigidity theorem | the winning card is always a packet head | sizes never congruent, so no equal deal reaches the loop, at any n |
| PP284 | uniform gaps and equal post-win sizes | the same |

Neither contains the other.
- At n = 12 every loop satisfies both, with a = 5.
- At n = 51 they part. Equal post-win sizes would give (18, 17, 16), which is not rigid, because the queue that wins at 16 cards plays a member. Rigid loops there have unequal post-win sizes 3kᵢ + 2.
- The case neither theorem reaches is a loop that is not rigid and does not have uniform gaps with equal post-win sizes.

**Theorem (rigid loops exist exactly when 3 | n and n ≥ 12; PROVED).** Write n = 3K + 3. Call a state *top-headed* when:
- it is in packet form;
- its three partial tails have lengths 0, 1 and 2;
- each queue holds at least one whole packet;
- the packet heads are exactly the K largest cards.

Then every top-headed state lies on a loop that keeps three queues live, and every state of that loop is top-headed.

*Proof.*
1. *The turn keeps the set.* The queue with tail 0 plays a head, and the other two play members. Heads beat members, so the head wins. The winner appends its head and the two members, which is a packet led by its largest card. The winner's tail becomes 2, and its packet count is unchanged: one packet opened, one appended. The other tails go 1 → 0 and 2 → 1. So the next state is top-headed, and all three queues stay live.
2. *The turn can be undone inside the set.* In the next state the winner is the one queue with tail 2. Its last three cards are the packet just appended: its own head, then the fronts of the next two seats in order. Remove that packet and put the three cards back at the three fronts, and the state is recovered. So a top-headed state has at most one top-headed predecessor.
3. The set is finite, and the turn maps it into itself one-to-one, so the turn permutes it. Every orbit of a permutation of a finite set is a cycle. ∎

- **Existence.** Top-headed states exist exactly when K ≥ 3. Together with the rigidity theorem this is an exact answer: *a rigid three-live loop exists if and only if n ≡ 0 (mod 3) and n ≥ 12.* So 3, 6 and 9 cards have none, and 12, 15, 18, …, 51 all have them.
- **Other sizes.** For n not divisible by 3, a three-live loop would have to be non-rigid. The complete census finds none at 13. Sizes 14, 16, 17 and the other non-multiples of 3 above 13 are untested.
- **Count.** There are 3!·C(K − 1, 2)·K!·(2K + 3)! top-headed states. At n = 12 that is 13,063,680 of the 15,863,040 loop states, the head set {9, 10, 11} above.
- **Checks.** `independent/live3_construct.py` plays random top-headed states for n = 12 to 51. On every turn it checks the four properties and the undo step, and every state returns.
- **Replay with the site's engine.** `live3_construct_check.cjs` replays two witnesses with the site's own engine, `sedaps-core-v0-2.js`. One is a 15-card state with period 36. The other is a 51-card state on the shipped deck, with whole-packet counts 2, 2 and 12. It returns after 180 turns with three queues live throughout.

**Theorem (the period of a rigid loop; PROVED).** Let a rigid loop have whole-packet counts k_A, k_B, k_C in the queues whose tails are 0, 1, 2, and K = k_A + k_B + k_C. Suppose the tail-1 queue sits one seat after the tail-0 queue (o = +1). Then

  **L = 3 · lcm(k_A, k_B, k_C, k_A + k_B + 1, k_B + k_C + 1, k_C + k_A + 1).**

If it sits one seat before (o = −1), then

  **L = 3 · lcm(k_A, k_B, k_C, K + 1, K + 2).**

*Proof.* On a rigid loop the winner of every turn is the queue with tail 0, whatever the card values. The counts and the orientation never change. So every card moves by one fixed permutation of positions, and the period is 3·ord(σ) for the three-turn map σ, since the phases return only every third turn.
- *Where σ sends a card.* Over three turns the queue with tail t wins on turn t + 1. Each queue plays its first three cards and appends one packet. So a card at position j ≥ 3 moves to j − 3. The card at position t ∈ {0, 1, 2} of queue i goes to the winner w of turn t + 1, at position size(w) − 3 + d, where d is i's seat distance after w.
- *Front slots.* Follow each card from front slot to front slot, writing (a, r) for position r of the queue with tail a. The card there reaches the front slot (r, a) when o = +1, and (r, 2r − a) when o = −1. The trip takes k_r or k_r + 1 applications of σ.
- *o = +1.* The nine slots form three fixed points and three pairs. So σ has cycles of lengths k_A, k_B and k_C, and k_A + k_B + 1, k_B + k_C + 1 and k_C + k_A + 1.
- *o = −1.* The slots form three fixed points and two 3-cycles, giving cycles of lengths k_A, k_B, k_C, K + 1 and K + 2.
- In both cases the cycle lengths sum to n. Distinct cards fill all n positions, so the state recurs after 3m turns exactly when σᵐ is the identity. ∎

**Checks.** `independent/live3_rigid_period.py` builds σ position by position for every composition of K at every n from 12 to 51, and compares its order with the formula. It then plays a top-headed game of each shape wherever the period is short enough: every shape up to n = 30, and 204 at n = 51. All agree. The formula reproduces 9 and 60 at n = 12, 36 and 90 at 15, and 45, 60 and 126 at 18. It applies to every rigid loop, whatever its head set, because the proof never used the card values.

**At 51 cards.** Here K = 16, so the two formulas read 3·lcm(kᵢ, 17 − kᵢ over the three queues) and 3·lcm(k_A, k_B, k_C, 17, 18). They are the three-queue analogues of 2·lcm(a, 26, 25 − a). They give exactly 29 periods:

  180, 630, 918, 1,008, 1,080, 1,836, 1,980, 2,808, 3,672, 4,590, 4,752, 5,040, 5,148, 6,426, 6,930, 7,560, 9,180, 9,360, 10,098, 11,880, 11,934, 15,120, 16,380, 18,360, 19,656, 20,196, 20,592, 25,704, 64,260.

- **Only 6 are multiples of 52:** 2,808, 5,148, 9,360, 16,380, 19,656 and 20,592.
  - The multiple-of-52 law is a law of two-queue loops. It fails for 23 of the 29 rigid periods, starting with 180 (counts 2, 2, 12) and 1,008 (counts 1, 1, 14) (PP287).
  - All 19 periods PP287 collected from sampling are on this list, and the formula adds the 10 it had not met.
- **All 29 are multiples of 18, and this is proved.**
  - With o = −1, 18 divides 3·lcm(17, 18).
  - With o = +1, one of kᵢ and 17 − kᵢ is even, because they sum to 17.
  - Not every kᵢ is ≡ 1 (mod 3), because the three sum to 16 ≡ 1. So some kᵢ or 17 − kᵢ is divisible by 3.
- **18 is a fact about 51, not a law.** The gcd is 3 at n = 12 (periods 9 and 60), so 18 must not become the new 52 (PP287 §4). For loops that are not rigid, only 3 | L is known.

**Two questions, kept apart (PP285 §3).**
- **Q2, existence: does a three-live loop exist at n cards?**
  - Yes for every n ≡ 0 (mod 3) with n ≥ 12, including 15 and 51, by the construction.
  - No for n ≤ 11 and for n = 13, by complete censuses.
  - Untested for 14, 16, 17 and the other non-multiples of 3 above 13, where any loop would have to be non-rigid.
- **Q1, what the game needs: can a fair deal reach a three-live loop?**
  - Never a rigid loop, and never a PP284 loop.
  - An equal deal keeps the three sizes congruent, so the only loops it could reach are synchronised ones, on which all three queues play heads on the same turns. On such a loop the other two turns of every three are member turns, and a member wins each of them.

*Why the whole-packet search is complete for Q1 (PP285 §2).*
1. Every loop state is in packet form (lemma above).
2. On a congruent-size loop the common residue runs through 0, 1 and 2. So the loop passes through a state with all three sizes ≡ 0 (mod 3).
3. In packet form such a state has no partial tails: it is whole packets only.

So walking every whole-packet state is a complete search for the loops an equal deal could reach. With seat rotation fixing the global maximum in the first queue, `independent/live3_sync.c` does that:
- n = 9: 4,480 states;
- n = 12: 5,913,600 states;
- n = 15 (5–5–5): 10,762,752,000 states, every one of which loses a queue within 27 turns.

**No equal deal of 9, 12 or 15 cards ever reaches a loop that keeps three queues live.** This is PROVED by exhaustive computation. It does not say that no three-live loop exists at 15: the construction gives rigid ones there, of periods 36 and 90.

PP285 §4 rebuilt the enumeration independently and reproduced 4,480 and 5,913,600. Its first 15-card pattern (3–3–9) returned 1,076,275,200 states with no survivor, matching ours. The six patterns weigh 10 times that, which is 10,762,752,000.

- **Toward the conjecture (PP285 §5).** The global maximum M always leads its packet, and a partial tail holds only members of an opened packet. So whenever M reaches the front, its queue has no tail: every turn on which M is played is rigid. M's queue wins L/3 turns per period, so up to a third of any loop's turns are rigid for free.
  - The conjecture is that every three-live loop is rigid. It would settle Q1 at every n, and it is OPEN.
- **Sampling at 51 (C).** `independent/live3_probe51.py` plays 3,000 random synchronised states and 3,000 random 17–17–17 deals. All of them lose a queue:
  - the synchronised states after a median of 18 turns, at most 222;
  - the deals after a median of 53 turns, at most 197.
  - If loop-entering states made up a fraction f of the sampled space, 3,000 draws would all miss them with probability (1 − f)³⁰⁰⁰, which is 5% at f ≈ 0.1%. So the probe excludes a density above about 0.1% at about 95% confidence, and nothing smaller (PP285 §6).
  - At n = 12, loop-entering states were 1.25% of the three-live space. The probe stays C.

It is OPEN at 51 whether a synchronised loop exists, and so whether any fair deal reaches a three-live loop.

**Census bookkeeping.** At n = 12, the 15,863,040 packet-form states that lie on loops are exactly 9 × 1,036,800 + 60 × 108,864, so the loop count balances. Each loop is counted once, at its lexicographically smallest state. The program classifies every state as losing a queue, lying on a loop, or entering one, using Brent's cycle detection (`independent/live3_loops.c`).
- **Independent returns.** PP281 ran an unrestricted census of every three-live state with the global maximum in queue 0. That is an exact one-third reduction by seat rotation, and it uses no shape assumption.
  - It covers n ≤ 11 (1,796,256,000 states at n = 11) and finds no loop.
  - Its worst exit times are 2, 4, 5, 10, 11, 15 and 19 for n = 5 to 11.
  - It also reproduces the packet-form counts above for n ≤ 8 from its own shape predicate.
  - The complete census of `census2.c` (every state, three queues, n ≤ 11) is a third method.
- PP281 §3 read the lemma as needing reachability from a fair deal. The distinct-card argument in step 1 shows it does not: the census result holds on the whole state graph.
- **A finite search is not an all-n theorem.** A census that finds nothing constrains nothing beyond its range, and n = 12 shows why that matters: the pattern of n ≤ 11 does not continue. Three-live loops exist at 12 and at every multiple of 3 above it.

Three exact facts narrow any three-live loop.

1. **Balanced winners** (PP273). On a three-live turn each length changes by −1, and by +2 for the winner. Closing a loop of length L forces each queue to win exactly L/3 turns, so 3 | L. PROVED.
2. **Queue maxima never lose** (Team B; this strengthens PP273's "the top card never changes queue").
   - A queue receives cards only on turns it wins. Every card in that pot is below the winning card, which was already in the queue. So a queue's maximum card can never increase, and it drops only when that card loses.
   - On a loop the maximum is periodic and non-increasing, hence constant. So **in every loop, each live queue's maximum card wins whenever it is played**. PROVED.
   - In a three-live loop, the three queue maxima are therefore never played on the same turn. In two-queue War this is the "cards that never lose" half of Spivey's description.
3. **Fair-deal loops** (PP273, via the clock). A three-live loop reachable from a 17–17–17 deal has three lengths congruent mod 3. Its queues are then synchronised: all three play packet heads on the same turns. PROVED.

"No three-live loop exists" and "no three-live loop is reachable from a fair deal" are different claims. The first is false at 51; the second is the one the game needs, and it is open.

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
| `independent/live3_construct.py`, `live3_construct_check.cjs` | the construction of rigid loops for every n = 3K + 3, K ≥ 3; witnesses at 15 and 51 replayed with the site's engine (§2) |
| `independent/live3_rigid_period.py` | the rigid-loop period formula, checked against σ and against play; complete spectra for n = 12 to 51 (§2) |
| `independent/live3_rigid12.c` | every rigid loop at n = 12, by head set; reproduces the census totals (§2) |
| `independent/live3_probe51.py` | the sampling probe at 51 cards (§2, status C) |

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
| No loop in the state graph keeps three queues live | COMPUTED for n ≤ 11 (two methods; PP281 second seat) and for n = 13; **false at n = 12** (CERT: 1,145,664 loops, of lengths 9 and 60; PP282 witness); **false at every n ≡ 0 (mod 3) with n ≥ 12, 51 included** (PROVED, construction; 180-turn witness at 51 replayed with the shipped engine); untested for 14, 16, 17 and the other non-multiples of 3 above 13 |
| A rigid three-live loop exists if and only if 3 \| n and n ≥ 12 | PROVED (§2) |
| A rigid loop's period is 3·lcm(k_A, k_B, k_C, k_A+k_B+1, k_B+k_C+1, k_C+k_A+1) or 3·lcm(k_A, k_B, k_C, K+1, K+2), by orientation | PROVED (§2); checked for every shape, n = 12 to 51 |
| At 51 cards the rigid periods are exactly 29 values, all multiples of 18, and 6 of them multiples of 52 | PROVED (§2) |
| Every loop length is a multiple of 52 | **false** for three-live loops at 51 (PP287); PROVED for two-queue loops |
| Every three-live loop length is a multiple of 18 | false in general (9 and 60 at n = 12); PROVED for rigid loops at 51; OPEN for non-rigid loops |
| Pairwise congruence of the three sizes mod 3 is invariant while three are live | PROVED |
| No three-live loop is reachable from an equal deal | COMPUTED for n = 9, 12, 15 (whole-packet search, complete by PP285 §2; second seat at 9 and 12, and on the first 15-card pattern); OPEN at 51 |
| A 51-card sample finds no loop-entering state | C: 3,000 synchronised states and 3,000 deals; excludes a density above about 0.1% at about 95% |
| Every turn on which the global maximum is played is rigid | PROVED (PP285 §5) |
| Every three-live loop is rigid | OPEN; true at n = 12; it would settle the fair-deal question at every n |
| A three-live loop on which the winning card is always a packet head is never reachable from an equal deal, for any n | PROVED |
| Every loop at n = 12 is rigid (one head per turn, and it wins) | COMPUTED (all 1,145,664; confirmed by the rigid enumeration `live3_rigid12.c`) |
| At n = 12 the length-60 loops occur only with heads {9, 10, 11} | COMPUTED (`live3_rigid12.c`) |
| Four-player rules; the count \|H_t(x)\| | OPEN |

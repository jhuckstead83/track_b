# 51 SEDAPS
## Recoverable history in a deterministic 51-card rule

**Working note v0.1 — 26 September 2026**  
Jeffery Lyn Huckstead · Cerebral Graphix · Area 51

**Status.** Finite card result only. The four-player Spades adapter is open. RH remains open.

## Abstract

A deterministic forward rule need not have a single-valued inverse. This note isolates that distinction in the published three-queue 51-card capture rule used by the Line Game sidecar. Every current state has at most four legal one-turn predecessors, and an explicit legal 51-card state attains all four. Consequently, when the endpoint, transition convention, predecessor ordering, and move count are shared, at most two fixed-width branch bits per played move suffice to reconstruct a trajectory. The two-bit statement is a worst-case address bound, not a claim that each move intrinsically contains two bits. The companion HTML demo turns the four-way predecessor fiber into a playable backward-read puzzle. Reachability of the sharp witness from the original 17–17–17 initial class remains open. A four-seat Spades table is retained only as an interface for later rule development; no predecessor theorem is transferred to it.

## 1. Fixed object and rule

Use the 51 active faces of an ordinary deck with **2♣ held outside as marker Ⅰ**. Give each active face the published strength address

\[
q=4(v-1)+s,
\]

where rank value \(v\in\{1,\ldots,13\}\) and suit residues are \(S,H,D,C=0,1,2,3\). Address \(7\), the 2♣, is excluded.

A state is

\[
X=(H_0,H_1,H_2),
\]

where the three labeled ordered queues partition the 51 active cards. On a played turn every nonempty queue removes its first card. The greatest exposed address wins. The winner appends its own exposed card first, then the other exposed cards in clockwise player order. Let \(F\) denote this played-turn map on states with at least two live queues. Terminal self-loops and the optional forgiveness/escrow rule are outside the predecessor theorem below.

## 2. Four is the maximum predecessor multiplicity

For a current state \(X\), write

\[
\operatorname{Pre}_F(X)=\{Y:F(Y)=X\}.
\]

### Proposition

For every legal state \(X\),

\[
\boxed{|\operatorname{Pre}_F(X)|\le 4.}
\]

The bound is attained in the legal 51-card state space.

### Proof

Let \(B\) be the set of players whose queues are nonempty in the current state and let \(b=|B|\). A possible previous live-player set \(A\) must contain \(B\), have size two or three, and have a winner \(w\in B\).

Fix \((A,w)\). In the current state, the last \(|A|\) cards of \(H_w\) must be the returned pot from the previous turn. Their order uniquely identifies the card drawn by each previous live player: the first card of the suffix is the winner's exposed card, and the remaining cards follow clockwise player order. Remove that suffix and prepend the identified draws to their corresponding queues. This produces at most one predecessor for the fixed pair \((A,w)\). It is accepted only if the reconstructed winner card is greatest and a forward replay returns exactly to \(X\).

The number of possible \((A,w)\) pairs depends only on \(b\):

| Current live players | Previous live sets | Candidate predecessors at most |
|---|---|---:|
| 3 | \(A=B\) | 3 |
| 2 | \(A=B\) or all three players | 4 |
| 1 | either two-player set containing \(B\), or all three players | 3 |

Thus four is a global upper bound. The explicit witness in the next section attains it. ∎

## 3. Sharp 51-card witness

Start with the six low addresses \(0,1,2,3,4,5\), corresponding to A♠, A♥, A♦, A♣, 2♠, 2♥. Let

\[
U=(6,8,9,\ldots,51),
\]

so \(U\) is the increasing list of the other 45 active addresses and still excludes marker address 7.

The common endpoint is

\[
X_*=\bigl(U\Vert(5,3,1),\ (4,2,0),\ ()\bigr),
\]

with queue sizes \((48,3,0)\).

Four legal predecessor states replay to \(X_*\) in one move:

| Branch | \(H_0\) | \(H_1\) | \(H_2\) |
|---|---|---|---|
| 00 | \((0)\Vert U\Vert(5,3,1)\) | \((2,4)\) | \(()\) |
| 01 | \((0)\Vert U\Vert(5,3,1)\) | \((4)\) | \((2)\) |
| 10 | \((3)\Vert U\Vert(5)\) | \((1,4,2,0)\) | \(()\) |
| 11 | \((5)\Vert U\) | \((3,4,2,0)\) | \((1)\) |

The branch labels are a declared two-bit address for the four predecessor states. They are not part of the card rule itself.

**Open reachability question.** These four rows are legal states of the rule. It has not yet been proved that this sharp endpoint is reachable from the original 17–17–17 initial class. The upper bound remains valid on every reachable subset; sharpness on that restricted subset is open.

## 4. How much extra ledger recovers the past?

Order the legal predecessors by a fixed public convention. At a state with four predecessors, the chosen predecessor index lies in \(\{0,1,2,3\}\), so two fixed-width bits select it. Starting from a known endpoint, repeat the process backward for a known number of moves.

The resulting statement is deliberately conditional:

\[
\boxed{\text{endpoint + fixed conventions + move count + at most 2 branch bits/move}\Rightarrow\text{trajectory recovery}.}
\]

The endpoint, transition rule, predecessor ordering, and log length are shared side information and are not included in the two-bit figure. When a state has fewer than four predecessors, an adaptive code can use less than two bits. Two bits are necessary only as the worst-case fixed-width one-step budget when all four branches are admissible.

The witness also separates nearby observations. Endpoint plus previous winner is insufficient: each of the two possible winners still has two compatible predecessors. Endpoint plus previous live-player mask is also insufficient. Endpoint plus both winner and previous live-player mask is sufficient for this witness, while the branch index packs the required distinction into two bits.

## 5. Mirror is not inverse

A representation reversal can be defined independently of dynamical inversion. For example,

\[
R(H_0,H_1,H_2)=\bigl(\operatorname{rev}H_2,\operatorname{rev}H_1,\operatorname{rev}H_0\bigr).
\]

Define the conjugate rule

\[
F^R=RFR.
\]

Then

\[
RF=F^R R
\]

by construction. This is a commuting representation change. It does **not** imply \(RF=FR\), and it does not produce \(F^{-1}\). The four-way predecessor collision proves that no single-valued state-only inverse exists on this domain. The branch ledger restores backward recoverability by augmenting the state history.

This is why the title admits two reads. Literal string reversal gives `SPADES 51 → 15 SEDAPS`; reversal of a 51-object block preserves its cardinality, hence the game title **51 SEDAPS**.

## 6. HTML demo

The public demo fixes the exact four-way witness in code and verifies all four forward replays at page load. The backward interaction is intentionally minimal:

1. display the shared endpoint;
2. deal one of the four predecessor branches secretly;
3. reveal one branch bit, reducing four candidates to two;
4. reveal the second bit, recovering one predecessor;
5. replay it forward and verify the common endpoint.

A failure of the embedded witness assertion is rendered as an implementation failure rather than silently continuing.

The page also includes a four-seat North/East/South/West table frame for the future Spades adapter. That frame is presentation only. It does not change the three-queue theorem or transfer the four-predecessor bound into four-player Spades.

## 7. Open development questions

The next work should stay finite and rule-explicit.

- Is a four-way predecessor state reachable from the original 17–17–17 deal class?
- Once the intended four-player Spades convention is supplied, what is its exact state space and transition map?
- Under that four-player rule, what are the predecessor fiber sizes, and are any bounds sharp on reachable states?
- Which observations of a current state are sufficient to recover the immediately previous state?
- Can the predecessor index be encoded adaptively from the local fiber size without carrying redundant branch bits?
- Which reversal operations are mere conjugacies, and which change the dynamics?

These are questions about a finite game and its ledgers. No zero data or RH claim is needed to answer them.

## 8. Files in the website sidecar

The `/area-51/sedaps-51/` folder contains the runnable HTML demo, local CSS/JS, a pure witness verifier, the Astra implementation handoff, this Markdown source, LaTeX source, and PDF.

**RH STATUS: OPEN.**

# ASTRA PASS — 51 SEDAPS HTML demo

Use this as an implementation handoff, not a paper task.

## Goal

Build the next public Area 51 game page as a working HTML demo using the existing Blackjack 51 page as the visual/code reference. Start from the supplied `index.html` / `blackjack-v2-5.css` conventions, but make a **separate 51 SEDAPS page**. Do not rewrite Blackjack 51.

Deliver a complete runnable HTML demo first. Minimal prose. No paper, no essay, no RH narrative.

## Existing site framework to preserve

- Area 51 dark green/gold visual language.
- Existing game header / Games dropdown style.
- Card rendering conventions and 51-card alphabet where useful.
- Mobile-first behavior and accessible buttons / status text.
- `2C` / 2♣ remains the outside marker `I` in the 51-card realization.
- Do not wire wallet/jbits unless the demo genuinely needs them. This pass is structural, not economic.

## Name

Main game/page title: **51 SEDAPS**.

Keep the literal text mirror as a small secondary affordance only:

`SPADES 51` → `15 SEDAPS`

Do not confuse literal string reversal with reversal of a 51-object block.

## Hard mathematical payload already established

Under the published ordinary **three-queue capture rule** used by the Line Game sidecar:

- State: three labeled ordered queues partitioning the 51 active cards.
- On a played turn, every nonempty queue reveals/removes its first card.
- Highest published strength address wins.
- Winner appends its own exposed card first, then the other exposed cards in clockwise player order.
- Every current state has at most **four** legal one-turn predecessors.
- The bound is sharp in the legal 51-card state space.
- Therefore the endpoint + fixed conventions + known move count + at most **2 fixed-width branch bits per move** can reconstruct a trajectory.
- This is a worst-case fixed-width statement. Do not say every move intrinsically contains 2 bits.
- Reachability of the sharp four-way witness from the original 17–17–17 initial class remains open.

### Exact 51-card witness

Strength address is `q = 4(v-1)+s`, suits S,H,D,C = 0,1,2,3. Address 7 = 2C is excluded as marker I.

Let

`U = [6, 8, 9, ..., 51]` (all active addresses other than 0..5 and 7).

Common endpoint:

- H0 = `U || [5,3,1]`
- H1 = `[4,2,0]`
- H2 = `[]`

Four legal predecessors, ordered as branch labels `00,01,10,11`:

- `00`: H0=`[0]||U||[5,3,1]`, H1=`[2,4]`, H2=`[]`
- `01`: H0=`[0]||U||[5,3,1]`, H1=`[4]`, H2=`[2]`
- `10`: H0=`[3]||U||[5]`, H1=`[1,4,2,0]`, H2=`[]`
- `11`: H0=`[5]||U`, H1=`[3,4,2,0]`, H2=`[1]`

All four replay in one published-rule move to the same endpoint. Keep an internal assertion that verifies this on page load. If it fails, render an implementation failure instead of the demo.

## Demo interaction to implement

### A. Backward mode — main screen

Put the **present state in the center**.

Around it show four candidate pasts, each with a two-bit branch label:

- 00
- 01
- 10
- 11

The four surrounding panels are **possible predecessor branches**, not a claim that the theorem comes from four-player Spades.

Controls:

1. `Deal hidden past`
   - choose one of the four witness branches locally/randomly;
   - keep the chosen branch hidden.

2. `Reveal first bit`
   - eliminate two branches.

3. `Reveal second bit`
   - leave one branch.

4. `Replay forward`
   - execute the published three-queue rule from that predecessor;
   - verify it reaches the center endpoint exactly.

5. `Reset`

Show simple status counts: `4 possible → 2 possible → 1 recovered`.

### B. Forward / backward toggle

Forward view:

`complete state → one next state`

Backward view:

`one endpoint ← up to four legal past states`

Do not claim that deterministic forward implies invertible backward.

### C. Four-player Spades frame — framework only

Add a second panel that visually uses the conventional four-seat table geometry (North / East / South / West is fine as a placeholder), because the intended public Spades experience is four-player.

But **do not invent the user’s Spades rules yet**.

This panel should say only, in UI-level language:

- `4-player rules adapter`
- `waiting for table convention`
- `no predecessor theorem transferred yet`

Make it easy to replace with the user's actual Spades conventions in the next pass.

Do not alter the proven three-queue witness to force a four-player result.

## Design rule

The page should demonstrate a fact before explaining it.

Desired first experience:

1. Reader sees one present state.
2. Reader is asked: `What happened one move ago?`
3. Four legal answers appear.
4. One bit cuts the set to two.
5. Second bit identifies the past.
6. Replay confirms all four candidates genuinely lead to the same present.

Keep text short.

## Important separations

Do not merge these:

- four predecessor branches;
- four future offsets in the Forge zero-gap experiment;
- four suits;
- arithmetic mod 4;
- four-player Spades.

They may later connect, but this HTML pass must not assume a connection.

Do not mention the historical 15 terminating card runs in relation to `15 SEDAPS`.

## Current empirical Forge work

Treat Forge 51 as separate. This SEDAPS page is a sidecar / finite control. Do not import zero data, Odlyzko heights, `3.5`, W4, or RH scoring into this page.

## Source files supplied

Use these as implementation references:

- `index.html` — current Blackjack 51 page and card UI conventions.
- `blackjack-v2-5.css` — current Blackjack action-row patch.
- wallet adapter files — reference only; omit wallet from SEDAPS unless there is a concrete reason to use it.
- `Forge_51_v0_2_RESEARCH_PACKAGE` / research board — exact predecessor theorem and witness.
- `sedaps-51-demo-v0_1.html` — starter scaffold from ChatGPT. Audit it; do not trust it blindly.

## What to improve over the starter scaffold

Use your remaining pass for implementation/math feedback, not prose polishing:

- verify the exact predecessor witness independently in JS;
- make the table geometry feel like the Area 51 site;
- make the branch-bit reveal visually obvious;
- keep mobile layout good;
- preserve accessibility;
- isolate the future four-player Spades adapter cleanly;
- if you find a bug or a sharper invariant, fix/record it in the HTML source comments;
- do not broaden scope.

## Deliverable

Return a complete standalone/public-ready HTML demo plus any small CSS/JS files only if separation materially improves maintainability.

Also return a tiny implementation ledger at the bottom of your response:

- exact witness check: PASS/FAIL
- four branches replay to endpoint: PASS/FAIL
- first-bit filter: PASS/FAIL
- second-bit recovery: PASS/FAIL
- mobile smoke check: PASS/FAIL
- four-player adapter status: OPEN / IMPLEMENTED

No paper.
No high-height compute.
No new empirical claims.

`RH STATUS: OPEN`

# 51 SEDAPS v0.4.1

Current UI: `index.html`, `sedaps-v0-4.js`, `sedaps-lemma-v0-4.js`, `sedaps-v0-3.css`. Frozen rule engine: `sedaps-core-v0-2.js`.

Read [RESEARCH_UPDATE_v0_4_1.md](RESEARCH_UPDATE_v0_4_1.md) (turn-indexed reachability, the proof that the search is complete, exact history counts, the War period theorem, independent replays), then [RESEARCH_UPDATE_v0_4.md](RESEARCH_UPDATE_v0_4.md). Verify with `node verify-sedaps-v0-4.cjs --decks`, `node verify-past10-v0-4-1.cjs` and `node count-histories-v0-4-1.cjs --brute`; independent replays are in `independent/`.

---

# 51 SEDAPS v0.3

Read [RESEARCH_UPDATE_v0_3.md](RESEARCH_UPDATE_v0_3.md) for the equal-deal obstruction and the reached turn-85 case. The page verifies both cases before enabling play. The supplied v0.2 review is merged, with historical sources below preserved.

---

# 51 SEDAPS · demo v0.2

Public route: /area-51/sedaps-51/. This folder is a drop-in update for the supplied v2.6.1 site.

Open index.html to run the local demo. The separately supplied standalone HTML has its styles and scripts embedded. No wallet or network service is needed for play.

- sedaps-core-v0-2.js: exact alphabet, played-turn transition, predecessor enumeration and witness assertion.
- sedaps-v0-2.js: hidden branch, first/second bit reveals, forward state selection and visible replay.
- sedaps-v0-1.css plus sedaps-v0-2.css: Area 51 styling and responsive layout.
- verify-witness-v0-2.cjs: dependency-free Node verifier. Run node verify-witness-v0-2.cjs in this folder.

The startup assertion validates the complete active alphabet, exact branch ordering, all four forward replays and the complete predecessor fiber. Failure blocks the demo. Terminal states have no played turn; artificial terminal self-loops are excluded.

Independent validation: all 20,160 six-card states and 18,000 played transitions agree with brute-force predecessor enumeration. The supplied Invariant engine also replays all four 51-card branches to the endpoint.

The branch order is explicitly 00, 01, 10, 11. In this witness the first bit selects winner H1/H0; the second says whether H2 participated. This interpretation is specific to this witness. Two bits are a worst-case fixed-width address budget, given the shared endpoint, conventions and move count.

The four-player adapter remains OPEN, awaiting the user's actual table convention. Reachability of the sharp witness from the 17–17–17 initial class remains OPEN.

The supplied working note, research board and original handoff are retained unchanged.

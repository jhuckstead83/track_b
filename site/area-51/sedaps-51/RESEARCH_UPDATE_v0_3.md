# Forge 51 / 51 SEDAPS v0.3

September 27, 2026. Exact three-queue card model. RH remains OPEN.

The returned Colab v0.2 output reproduces the original disclosed pilot and structural audit. The two supplied output ZIPs are byte-identical and count as one replay. The rounded-observation counterexample is unchanged; no new prediction evidence is claimed.

## A starting condition really excludes histories

The original 51-card constructed witness is **unreachable from every 17–17–17 deal** under the frozen played-turn rule. Its four legal predecessors still exist. Legality and reachability are different questions.

Let a capture packet be two or three distinct cards with its greatest card first. For a queue initially containing at most m cards, where m ≥ 2, every later queue has the form

    P C1 C2 ... Ck

where P has length at most m and each Ci is a capture packet. Initially P is the whole queue. Removing the front either shortens P or removes the leading card of the first packet, leaving at most two cards as the new prefix. Appending a won packet preserves the form. These are the only queue operations in a played turn, so the language is forward invariant. The test uses only the greatest-first property; it relaxes the stricter clockwise return order and is therefore necessary, not sufficient.

The prefix-floor algorithm enumerates all ways of stripping legal length-two or length-three suffix packets. Its least remaining prefix length is the minimum initial-hand bound admitted by this language. For the constructed endpoint's H0, the possible lengths are **44, 45, 46 and 48**. All exceed 17. This proves the obstruction; it is not a failed search argument.

An exhaustive six-card check visited all 20,160 states. Of these, 12,588 pass the m=2 prefix test, and all 11,472 played transitions from those states preserve it. This finite audit supports the implementation; the argument above proves the general invariant.

## An endpoint reached after 85 turns

One frozen trajectory used seed 510053, the existing 51-card alphabet (address 7 outside), a round-robin 17–17–17 deal, and a 2,048-turn / 60-second cap. It stopped at the first endpoint with four legal predecessors, **turn 85**, with queue lengths **35, 16, 0**. Every transition and inverse index is included in `reachable-certificate-v0-3.json` and replayed by both Python and JavaScript.

Predecessors are ordered lexicographically by the complete three-queue state:

| Bits | Previous hand sizes | Queue prefix floors | Reachability from 17–17–17 |
| --- | --- | --- | --- |
| 00 | 36, 15, 0 | 2, 0, 0 | Certified by the recorded trajectory |
| 01 | 36, 14, 1 | 2, 0, 1 | Not ruled out; not certified |
| 10 | 34, 17, 0 | 0, 0, 0 | Not ruled out; not certified |
| 11 | 33, 17, 1 | 33, 0, 1 | Impossible from 17–17–17 |

The game can apply the starting-condition filter, reducing four legal candidates to three candidates not yet ruled out. The two recorded history bits then recover the actual predecessor. A past displayed as “not ruled out” is not being advertised as reachable.

This is **not** a proof that the four-predecessor maximum is sharp within the equal-deal reachable class. That question, and reachability of branches 01 and 10, remain open. A legal endpoint reached from an equal deal need not have all its legal predecessors in that same reachable class.

## Interface and conventions

The v0.2 rule engine and the historical v0.1 notes remain preserved. v0.3 adds the reached case, equal-start filter, complete trajectory inspector, slower reveal transitions and Beta label. The original constructed case remains selectable.

East/right/+x is the four-seat display convention and East receives the first card in the proposed display. This does not relabel H0/H1/H2, change strengths or alter the three-queue transition. Four-player play/capture rules are still unspecified, and no three-queue theorem transfers automatically.

## Research ledgers

- Structural: prefix invariant proved; constructed witness equal-deal reachability NO-GO; one reached endpoint exactly certified.
- Prediction/surprise: N/A for this exact structural exploration. The Colab return is a disclosed replay, not a second holdout.
- Source-to-zero transport and high-height zero computation: not tested here.
- RH: OPEN. No literature-wide novelty claim is made.

The original review's stochastic card-decay comparison is retained separately in the review bundle. Its human visual preference is not a statistical optimum and does not change this card rule.

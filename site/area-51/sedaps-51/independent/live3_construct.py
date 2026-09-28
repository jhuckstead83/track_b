#!/usr/bin/env python3
"""Three-live loops for every n = 3K + 3 with K >= 3 (RESEARCH_UPDATE_v0_4_1.md section 2, construction).

A state is *top-headed* when it is in packet form, its three partial tails have lengths 0, 1 and 2,
every queue holds at least one whole packet, and the packet heads are exactly the K largest cards.
The theorem says the turn map sends a top-headed state to a top-headed state, and that the step
can be undone uniquely inside that set, so every top-headed state lies on a loop that keeps three
queues live.

This script builds random top-headed states and plays each one until it returns. On every turn
it checks the invariants and undoes the step to confirm the predecessor is unique. It writes
live3_construct_receipt.json, with witnesses at n = 15 and n = 51 that
live3_construct_check.cjs replays with the site's own engine (sedaps-core-v0-2.js).

Run: python3 live3_construct.py   (about a minute)
"""
import json, math, random

def step(q):
    """The shipped three-queue rule: the highest front card wins, and the winner appends the
    played cards in seat order starting from itself."""
    f = [x[0] for x in q]
    w = max(range(3), key=lambda i: f[i])
    q = [x[1:] for x in q]
    q[w] = q[w] + [f[(w + o) % 3] for o in range(3)]
    return q, w

def top_headed(q, heads):
    """(tail lengths, whole-packet counts) if q is top-headed for this head set, else None."""
    tails, packs = [], []
    for x in q:
        p = len(x) % 3
        if any(c in heads for c in x[:p]): return None
        body = x[p:]
        for j in range(0, len(body), 3):
            if body[j] not in heads or body[j + 1] in heads or body[j + 2] in heads: return None
        tails.append(p); packs.append(len(body) // 3)
    if sorted(tails) != [0, 1, 2] or min(packs) < 1: return None
    return tails, packs

def undo(q):
    """The unique top-headed predecessor: the queue with tail 2 won; its last packet goes back."""
    w = [len(x) % 3 for x in q].index(2)
    h, a, b = q[w][-3:]
    r = [list(x) for x in q]
    r[w] = r[w][:-3]
    back = {w: h, (w + 1) % 3: a, (w + 2) % 3: b}
    return [[back[i]] + r[i] for i in range(3)]

def build(n, ks, rng):
    K = sum(ks)
    assert 3 * K + 3 == n and min(ks) >= 1
    heads = list(range(n - K, n)); members = list(range(n - K))
    rng.shuffle(heads); rng.shuffle(members)
    seats = [0, 1, 2]; rng.shuffle(seats)          # seats[p] holds the tail of length p
    q = [None] * 3
    for p, seat in enumerate(seats):
        body = []
        for _ in range(ks[seat]): body += [heads.pop(), members.pop(), members.pop()]
        q[seat] = [members.pop() for _ in range(p)] + body
    return q

def run(q0, n, cap=10 ** 6):
    K = (n - 3) // 3
    heads = set(range(n - K, n))
    q, winners, prev = q0, [], None
    packs0 = top_headed(q0, heads)[1]
    for t in range(1, cap + 1):
        tails = top_headed(q, heads)[0]
        nq, w = step(q)
        assert w == tails.index(0), 'the head must win'            # rigid: the head beats both members
        chk = top_headed(nq, heads)
        assert chk is not None, 'top-headed states map to top-headed states'
        assert chk[1] == packs0, 'each queue keeps its number of whole packets'
        assert undo(nq) == q, 'the step is undone uniquely'
        winners.append(w); q = nq
        if q == q0: return t, winners
    return None, winners

def count_states(n):
    """|S| = 3! * C(K-1, 2) * K! * (2K + 3)!: seats for the tails, packet counts, heads, members."""
    K = (n - 3) // 3
    return math.factorial(3) * math.comb(K - 1, 2) * math.factorial(K) * math.factorial(2 * K + 3)

def compositions(K):
    return [(a, b, K - a - b) for a in range(1, K) for b in range(1, K - a)]

def main():
    rng = random.Random(51)
    plan = {12: 200, 15: 200, 18: 200, 21: 200, 24: 100, 30: 60, 51: 24}
    rows, witnesses = [], {}
    for n, trials in plan.items():
        K = (n - 3) // 3
        comps = compositions(K)
        lengths, rotate = {}, True
        for i in range(trials):
            ks = comps[i % len(comps)]
            q0 = build(n, ks, rng)
            L, winners = run(q0, n)
            assert L is not None and L % 3 == 0
            lengths[L] = lengths.get(L, 0) + 1
            rotate &= all(winners[j] != winners[j + 1] and winners[j] == winners[j + 3]
                          for j in range(len(winners) - 3))
            if n in (15, 51) and (n not in witnesses or L < witnesses[n]['period']):
                witnesses[n] = {'n': n, 'wholePackets': list(ks), 'period': L,
                                'state': q0, 'winnersFirst9': winners[:9]}
        rows.append({'n': n, 'K': K, 'topHeadedStates': str(count_states(n)), 'trials': trials,
                     'allLooped': True, 'winnersRotate': rotate,
                     'loopLengths': {str(k): v for k, v in sorted(lengths.items())}})
        print(n, K, sorted(lengths))
    receipt = {
        'program': 'live3_construct.py',
        'rule': 'three queues; highest front card wins; winner appends the played cards in seat order starting from itself',
        'cards': 'ranks 0..n-1; live3_construct_check.cjs maps rank r to the r-th card of the shipped 51-card deck',
        'theorem': 'every top-headed state lies on a three-live loop, for every n = 3K + 3 with K >= 3 (RESEARCH_UPDATE_v0_4_1.md section 2)',
        'checkedEveryTurn': ['the head wins', 'the next state is top-headed', 'whole-packet counts are fixed',
                             'undo() recovers the previous state'],
        'results': rows,
        'witnesses': [witnesses[15], witnesses[51]],
    }
    json.dump(receipt, open('live3_construct_receipt.json', 'w'), indent=1)
    print('wrote live3_construct_receipt.json')

if __name__ == '__main__':
    main()

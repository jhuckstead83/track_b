#!/usr/bin/env python3
"""Periods of rigid three-live loops (RESEARCH_UPDATE_v0_4_1.md section 2, period theorem for rigid loops).

On a rigid loop the winning card is always a packet head, so the winner on each turn is the queue
whose partial tail is empty, whatever the card values. Every card therefore moves by one fixed
permutation of positions, and the period is 3 * ord(sigma), where sigma is the three-turn map. It
depends only on the whole-packet counts (kA, kB, kC) of the queues whose tails are 0, 1, 2, and on
the seating orientation o (the tail-1 queue sits one seat after the tail-0 queue, o = +1, or one
seat before it, o = -1). With K = kA + kB + kC:

    o = +1:  L = 3 * lcm(kA, kB, kC, kA + kB + 1, kB + kC + 1, kC + kA + 1)
    o = -1:  L = 3 * lcm(kA, kB, kC, K + 1, K + 2)

This script checks the formula three ways for every composition of K at every n = 3K + 3 from
12 to 51: against the order of sigma built position by position, and against a played game from a
top-headed state (heads = the K largest cards) with that shape. It then lists the complete
spectrum of rigid-loop periods at each n and flags the multiples of n + 1.

Run: python3 live3_rigid_period.py   (about a minute; writes live3_rigid_period_receipt.json)
"""
import json, math, random
from functools import reduce

lcm = lambda *xs: reduce(lambda a, b: a * b // math.gcd(a, b), xs)

def formula(kA, kB, kC, o):
    K = kA + kB + kC
    if o == 1: return 3 * lcm(kA, kB, kC, kA + kB + 1, kB + kC + 1, kC + kA + 1)
    return 3 * lcm(kA, kB, kC, K + 1, K + 2)

def seats(o):
    """Seat of the queue with tail 0, 1, 2 (tail-0 queue in seat 0)."""
    return [0, o % 3, (2 * o) % 3]

def sigma_order(kA, kB, kC, o):
    """Order of the three-turn position map, built from the rule's positional form."""
    ks, seat = (kA, kB, kC), seats(o)
    size = {seat[t]: t + 3 * ks[t] for t in range(3)}          # queue in seat seat[t] has tail t
    tail_of = {seat[t]: t for t in range(3)}
    pos = [(q, j) for q in range(3) for j in range(size[q])]
    index = {p: i for i, p in enumerate(pos)}
    perm = [0] * len(pos)
    for (q, j) in pos:
        if j >= 3:
            tgt = (q, j - 3)
        else:                                                   # played on turn j + 1
            w = seat[j]                                         # the queue with tail j wins that turn
            tgt = (w, size[w] - 3 + (q - w) % 3)                # seat order starting from the winner
        perm[index[(q, j)]] = index[tgt]
    assert sorted(perm) == list(range(len(pos)))
    seen, order = [False] * len(pos), 1
    for i in range(len(pos)):
        if seen[i]: continue
        c, x = 0, i
        while not seen[x]: seen[x] = True; x = perm[x]; c += 1
        order = lcm(order, c)
    return order

def step(q):
    f = [x[0] for x in q]
    w = max(range(3), key=lambda i: f[i])
    q = [x[1:] for x in q]
    q[w] = q[w] + [f[(w + i) % 3] for i in range(3)]
    return q

def played_period(kA, kB, kC, o, rng, cap=10 ** 7):
    ks, seat = (kA, kB, kC), seats(o)
    K = sum(ks); n = 3 * K + 3
    heads = list(range(n - K, n)); mem = list(range(n - K)); rng.shuffle(heads); rng.shuffle(mem)
    q = [None] * 3
    for t in range(3):
        body = []
        for _ in range(ks[t]): body += [heads.pop(), mem.pop(), mem.pop()]
        q[seat[t]] = [mem.pop() for _ in range(t)] + body
    q0, s = q, q
    for L in range(1, cap + 1):
        s = step(s)
        if s == q0: return L
    return None

def main():
    rng = random.Random(1789)
    out = []
    for n in range(12, 52, 3):
        K = (n - 3) // 3
        spectrum, checked = set(), 0
        for kA in range(1, K - 1):
            for kB in range(1, K - kA):
                kC = K - kA - kB
                for o in (1, -1):
                    L = formula(kA, kB, kC, o)
                    assert 3 * sigma_order(kA, kB, kC, o) == L, (n, kA, kB, kC, o)
                    if n <= 30 or L <= 30000:                   # play it out where that is quick
                        assert played_period(kA, kB, kC, o, rng) == L, (n, kA, kB, kC, o)
                        checked += 1
                    spectrum.add(L)
        sp = sorted(spectrum)
        out.append({'n': n, 'K': K, 'periods': sp, 'count': len(sp),
                    'multiplesOfNplus1': [L for L in sp if L % (n + 1) == 0],
                    'gcd': reduce(math.gcd, sp), 'playedOut': checked})
        print(n, len(sp), 'gcd', reduce(math.gcd, sp), 'multiples of n+1:', [L for L in sp if L % (n + 1) == 0])
    json.dump({'program': 'live3_rigid_period.py',
               'formula': {'o=+1': '3*lcm(kA,kB,kC,kA+kB+1,kB+kC+1,kC+kA+1)', 'o=-1': '3*lcm(kA,kB,kC,K+1,K+2)'},
               'checks': 'formula = 3*ord(sigma) for every composition; = played period wherever played out',
               'results': out}, open('live3_rigid_period_receipt.json', 'w'), indent=1)

if __name__ == '__main__':
    main()

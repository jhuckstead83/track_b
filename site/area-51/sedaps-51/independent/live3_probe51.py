#!/usr/bin/env python3
"""A sampling probe at 51 cards (RESEARCH_UPDATE_v0_4_1.md section 2, status C).

Plays 3,000 random synchronised states (whole packets in every queue, each led by its largest
card) and 3,000 random 17-17-17 deals until a queue empties, and records how long three queues
stayed live. It is a sample, not a search: if loop-entering states made up a fraction f of the
sampled space, all 3,000 draws would miss them with probability (1 - f)^3000, which is 5% at
f = 0.1%. So a clean run excludes a density above about 0.1% at about 95% confidence, and nothing
smaller (PP285 section 6).

Run: python3 live3_probe51.py   (under a minute; writes live3_probe51_receipt.json)
"""
import json, random

def step(q):
    f = [x[0] for x in q]
    w = max(range(3), key=lambda i: f[i])
    q = [x[1:] for x in q]
    q[w] = q[w] + [f[(w + o) % 3] for o in range(3)]
    return q

def rand_sync(n, rng):
    K = n // 3
    while True:
        a, b = sorted(rng.sample(range(1, K), 2)); ks = [a, b - a, K - b]
        if min(ks) >= 1: break
    cards = list(range(n)); rng.shuffle(cards); q, pos = [[], [], []], 0
    for i, k in enumerate(ks):
        for _ in range(k):
            pk = sorted(cards[pos:pos + 3], reverse=True); pos += 3
            rest = pk[1:]; rng.shuffle(rest); q[i] += [pk[0]] + rest
    return q

def equal_deal(n, rng):
    cards = list(range(n)); rng.shuffle(cards); m = n // 3
    return [cards[:m], cards[m:2 * m], cards[2 * m:]]

def main(n=51, N=3000, cap=10 ** 5):
    rng, out = random.Random(51), {}
    for kind, make in (('synchronised', rand_sync), ('17-17-17 deal', equal_deal)):
        ts, alive = [], 0
        for _ in range(N):
            q, t = make(n, rng), 0
            while all(q) and t < cap: q = step(q); t += 1
            alive += all(q); ts.append(t)
        ts.sort()
        out[kind] = {'samples': N, 'medianTurnsThreeLive': ts[N // 2], 'maxTurnsThreeLive': ts[-1],
                     'stillThreeLiveAtCap': alive, 'cap': cap}
        print(kind, out[kind])
    json.dump({'program': 'live3_probe51.py', 'n': n, 'status': 'C (a sample, not a search)',
               'exclusion': 'a loop-entering density above about 0.1% at about 95% confidence', 'results': out},
              open('live3_probe51_receipt.json', 'w'), indent=1)

if __name__ == '__main__':
    main()

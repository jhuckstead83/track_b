#!/usr/bin/env python3
"""Independent Python replay of the 51 SEDAPS v0.4 results (Team B, 27 September 2026).

Written from the rule's statement, not translated from the shipped JavaScript. It reads only
the shipped certificate JSON files. Checks:
  1. the v0.3 certificate: its recorded 17-17-17 deal replays to the turn-85 present;
  2. the five four-for-four presents: all 20 deals replay to their stated predecessors and
     endpoints, and those four predecessors are exactly the legal predecessor set;
  3. the turn-85 exclusions: 01 and 11 fail the mod-3 clock at every elapsed turn, and
     10 is unreachable from a 17-17-17 deal at turn 84, but reachable at elapsed turns 24, 27, 30, 33;
  4. the forward fates and the periodic remnant (same seeds as the JavaScript verifier).
Usage: python3 sedaps_independent.py [path/to/area-51/sedaps-51] [--json out.json]   (default: the parent folder)
"""
import json, math, sys, os
from collections import Counter

HERE = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
CARDS = [q for q in range(52) if q != 7]          # 51 active cards; 7 is the marker

def live(state):
    return [i for i in range(3) if state[i]]

def forward(state):
    """One played turn. Returns the next state, or None for a terminal state."""
    L = live(state)
    if len(L) < 2:
        return None
    played = {i: state[i][0] for i in L}
    w = max(L, key=lambda i: played[i])
    nxt = [list(q[1:]) if i in L else list(q) for i, q in enumerate(state)]
    nxt[w].extend(played[(w + k) % 3] for k in range(3) if (w + k) % 3 in played)
    return tuple(tuple(q) for q in nxt)

def T(state):
    return tuple(tuple(q) for q in state)

def legal_predecessors(y):
    """All states x with forward(x) == y, by inverting the capture:
    choose the previous live set A (containing every live queue of y, |A| >= 2) and a winner
    w among y's live queues; the last |A| cards of queue w are the capture, winner first."""
    B = set(live(y)); out = set()
    for mask in range(1, 8):
        A = [i for i in range(3) if mask >> i & 1]
        if len(A) < 2 or not B <= set(A):
            continue
        for w in B:
            k = len(A)
            if len(y[w]) < k:
                continue
            cap = y[w][-k:]
            seats = [(w + j) % 3 for j in range(3) if (w + j) % 3 in A]
            x = [list(q) for q in y]
            x[w] = x[w][:-k]
            for seat, card in zip(seats, cap):
                x[seat].insert(0, card)
            x = T(x)
            if forward(x) == T(y):
                out.add(x)
    return out

def is_partition(state, deck=CARDS):
    flat = [c for q in state for c in q]
    return sorted(flat) == sorted(deck)

# ---- time-aware shape lemma (RESEARCH_UPDATE_v0_4 §2), restated from its text
def led(q, a, k):
    """cards q[a..a+k-1] form a packet led by its largest card"""
    return all(q[a] > q[j] for j in range(a + 1, a + k))

def shape_ok(y, s):
    L = live(y)
    if len(L) == 3:
        p = 17 - s if s < 17 else (17 - s) % 3
        for q in y:
            n = len(q)
            if n < p or (n - p) % 3:
                return False
            if not all(led(q, a, 3) for a in range(p, n, 3)):
                return False
        return True
    if len(L) != 2 or s < 17:
        return False
    for i in L:
        q = y[i]; n = len(q); ok = False
        # q = front (<= 2 cards) + 3-packets + 2-packets, each packet led by its largest
        for b in range(n, -1, -2):                      # b = start of the 2-packet tail
            if not all(led(q, a, 2) for a in range(b, n, 2)):
                continue
            for a in range(b, -1, -3):                  # a = start of the 3-packet block
                if not all(led(q, c, 3) for c in range(a, b, 3)):
                    break
                if a <= 2:
                    ok = True; break
            if ok:
                break
        if not ok:
            return False
    return True

def backward(y, s, limit=10**6):
    """Every backward history of y at turn s allowed by the shape lemma.
    Returns (reaches a 17-17-17 deal, lowest turn reached, distinct (state, turn) pairs expanded)."""
    seen = set(); low = s; found = False; stack = [(y, s)]
    while stack:
        z, t = stack.pop()
        if not shape_ok(z, t):
            continue
        low = min(low, t)
        if t == 0:
            found = found or all(len(q) == 17 for q in z)
            continue
        if (z, t) in seen:
            continue
        seen.add((z, t))
        if len(seen) > limit:
            raise RuntimeError('search budget exceeded')
        for x in legal_predecessors(z):
            stack.append((x, t - 1))
    return found, low, len(seen)

def first_deal(y, s):
    """Depth-first backward search under the shape lemma that stops at the first 17-17-17 deal.
    Returns (path from the deal up to y, or None; states expanded; lowest turn checked)."""
    seen = set(); low_checked = s
    if not shape_ok(y, s):
        return None, 0, s
    stack = [(y, s, iter(legal_predecessors(y)))]; seen.add((y, s))
    while stack:
        z, t, it = stack[-1]
        nxt = next(it, None)
        if nxt is None:
            stack.pop(); continue
        low_checked = min(low_checked, t - 1)
        if not shape_ok(nxt, t - 1):
            continue
        if t - 1 == 0:
            if all(len(q) == 17 for q in nxt):
                return [nxt] + [e[0] for e in reversed(stack)], len(seen), low_checked
            continue
        if (nxt, t - 1) in seen:
            continue
        seen.add((nxt, t - 1)); stack.append((nxt, t - 1, iter(legal_predecessors(nxt))))
    return None, len(seen), low_checked

def mulberry32(a):
    """The seeded generator used by the JavaScript verifiers, in 32-bit arithmetic."""
    a &= 0xFFFFFFFF
    def rnd2():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = imul(a ^ (a >> 15), 1 | a)
        t = ((t + imul(t ^ (t >> 7), 61 | t)) & 0xFFFFFFFF) ^ t
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return rnd2

def imul(x, y):
    return (x & 0xFFFFFFFF) * (y & 0xFFFFFFFF) & 0xFFFFFFFF

def seeded_deal(seed, deck=CARDS):
    r = mulberry32(seed); d = list(deck)
    for i in range(len(d) - 1, 0, -1):
        j = math.floor(r() * (i + 1)); d[i], d[j] = d[j], d[i]
    y = [[], [], []]
    for i, c in enumerate(d):
        y[i % 3].append(c)
    return T(y)

def fate(y, t):
    seen = {}
    while True:
        if len(live(y)) < 2:
            return ('end', t, None)
        if y in seen:
            return ('cycle', seen[y], t - seen[y])
        seen[y] = t; y = forward(y); t += 1

def main():
    report = {'script': 'sedaps_independent.py', 'rule': 'restated from RESEARCH_UPDATE_v0_4.md and the v0.1 note', 'checks': []}
    def ok(name, **detail):
        report['checks'].append({'name': name, 'pass': True, **detail}); print('PASS', name, json.dumps(detail)[:300])
    cert = json.load(open(os.path.join(HERE, 'reachable-certificate-v0-3.json')))
    c4 = json.load(open(os.path.join(HERE, 'dstart4-certificates-v0-4.json')))['certificates']

    # 1. v0.3 certificate
    states = [T(s) for s in cert['states']]
    assert all(len(q) == 17 for q in states[0]) and is_partition(states[0])
    for i in range(cert['turns']):
        assert forward(states[i]) == states[i + 1], i
    x85 = states[85]
    pre = sorted(legal_predecessors(x85), key=lambda s: [list(q) for q in s])
    assert len(pre) == 4 and states[84] in pre
    ok('v0.3 certificate: the recorded 17-17-17 deal reaches the turn-85 present', seed=cert.get('seed'), sizes=[len(q) for q in x85])

    # 2. four-for-four certificates: 5 presents x 4 deals
    deals = 0
    for c in c4:
        y = T(c['endpoint']); P = legal_predecessors(y)
        assert len(P) == 4
        stated = {T(b['predecessor']) for b in c['branches']}
        assert stated == P, 'stated predecessors are the full legal set'
        for b in c['branches']:
            d = T(b['deal']); assert all(len(q) == 17 for q in d) and is_partition(d)
            z = d
            for _ in range(c['t'] - 1):
                z = forward(z)
            assert z == T(b['predecessor']) and forward(z) == y
            deals += 1
    assert deals == 20
    ok('four-for-four: all 20 deals replay to their predecessors and presents', turns=[c['t'] for c in c4], deals=deals)

    # 3. turn-85 exclusions
    by_sizes = {tuple(len(q) for q in x): x for x in pre}
    x00 = states[84]
    x01 = by_sizes[(36, 14, 1)]; x11 = by_sizes[(33, 17, 1)]; x10 = by_sizes[(34, 17, 0)]
    assert tuple(len(q) for q in x00) == (36, 15, 0)
    # 01 and 11: three live queues whose lengths are not congruent mod 3. While three queues
    # are live, every length is congruent to 17 - s (mod 3), so no elapsed turn s works.
    for x in (x01, x11):
        res = {len(q) % 3 for q in x}
        assert len(live(x)) == 3 and len(res) > 1
    ok('01 and 11 fail the mod-3 clock at every elapsed turn (lengths 36,14,1 and 33,17,1 have three residues)')
    found, low, nodes = backward(x10, 84)
    assert not found and low == 66
    ok('10 at turn 84: no backward history reaches a 17-17-17 deal', lowestTurn=low, statesExpanded=nodes)
    # Every elapsed turn. x10 has two live queues, so its turn s satisfies s >= 17. At turns
    # t >= 17 the lemma depends on t only through t mod 3, so if a complete search from turn s
    # checks no state below turn 17, the search from s + 3 is the same tree shifted by 3 turns,
    # with the same verdict and again no check below 17. Searching 17..84 and closing at 82-84
    # therefore covers every elapsed turn.
    found_at = []; rows = []
    for s in range(17, 85):
        path, nodes, lowc = first_deal(x10, s)
        rows.append([s, path is not None, nodes, lowc])
        if path:
            z = path[0]
            for _ in range(s):
                z = forward(z)
            assert z == x10 and forward(z) == x85 and all(len(q) == 17 for q in path[0])
            found_at.append(s)
    assert found_at == [24, 27, 30, 33], found_at
    assert all(r[3] >= 17 and not r[1] for r in rows if r[0] in (82, 83, 84))
    ok('10 is reached from 17-17-17 deals exactly at elapsed turns 24, 27, 30, 33 (every turn searched; 3-periodic from turn 82)',
       turns=found_at, closure=[r for r in rows if r[0] >= 82])
    report['turn85_elapsed_turn_scan'] = rows

    # 4. forward fates and the periodic remnant
    f85 = fate(x85, 85); assert f85 == ('cycle', 356, 3744)
    fates = [[c['t'], *fate(T(c['endpoint']), c['t'])] for c in c4]
    ok('forward fates', turn85=f85, fourForFour=fates)
    periods = Counter(); ends = 0; g = 0
    for seed in range(1, 2001):
        k, a, p = fate(seeded_deal(seed), 0)
        if k == 'end':
            ends += 1
        else:
            periods[p] += 1; g = math.gcd(g, p)
    assert g == 52 and sum(periods.values()) == 1652 and ends == 348
    ok('periodic remnant, 2,000 seeded deals (same generator as the JS verifier)', ends=ends, cycles=sum(periods.values()), gcd=g, periods=sorted(periods.items()))
    report['status'] = 'PASS'
    if '--json' in sys.argv:
        json.dump(report, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)

if __name__ == '__main__':
    main()

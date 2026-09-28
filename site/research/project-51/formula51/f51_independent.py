#!/usr/bin/env python3
"""Independent recomputation of the Formula 51 band and deduction (Team B, 27 Sep 2026).

Does not import derive51.py and does not use unicodedata: syllable index d splits as
L = d // 588, V = (d % 588) // 28, T = d % 28 (T = 0 means no trailing consonant).
Each component's exact weight is the product of its conditional ratios (parent/child count),
kept as an exact Fraction; weight classes are equal products, ordered by decreasing product,
members by code point (L < V < T). Checks:
  1. every radix N = 1..11172: component count; the band with 51 components; self-describing radices;
  2. all 588 band tables against f51_band.json (class sizes, arrangements, collision pairs,
     (class, polar, colour) sector, complete contexts, lowest class);
  3. the repaired proof of Section 3 (bracket 21(L-1) <= floor(N/28) <= 21L) on every N;
  4. PP270 §4.1 (second seat): the exact edge inequalities and the 257-radix trailing-minimum window;
  5. PP270 §4.2 (second seat): polar fibres, 30 labels, 50 164 531 200 lifts, J = (W,P) with 8 lifts,
     sharp sectors 15 / 23 / 45 by the rule k_max = M - mu_f.
Usage: python3 f51_independent.py path/to/f51_band.json [--json out.json]
"""
import json, math, sys
from fractions import Fraction
from collections import Counter, defaultdict

def components(N):
    nL = Counter(); nLV = Counter()
    for d in range(N):
        L, V = d // 588, (d % 588) // 28
        nL[L] += 1; nLV[(L, V)] += 1
    prod = defaultdict(lambda: Fraction(1))
    for L, c in nL.items():
        prod[('L', L)] = Fraction(N, c) ** c
    for (L, V), c in nLV.items():
        prod[('V', V)] *= Fraction(nL[L], c) ** c
        for T in range(1, c):            # trailing consonants present in this (L, V) context
            prod[('T', T)] *= c
    return prod

CODE = {'L': 0x1100, 'V': 0x1161, 'T': 0x11A7}
def name(c): return c[0] + str(c[1])

def classes(N):
    prod = components(N)
    groups = defaultdict(list)
    for c, p in prod.items(): groups[p].append(c)
    order = sorted(groups, reverse=True)
    members = [sorted(groups[p], key=lambda c: CODE[c[0]] + c[1]) for p in order]
    return members

CARDS = [r + s for r in ['A','2','3','4','5','6','7','8','9','10','J','Q','K'] for s in 'SHDC' if r + s != '2C']
def polar(m):
    n = 1
    while n * (n + 1) // 2 < m: n += 1
    return Fraction(m - n * (n - 1) // 2, n)
POLAR = [polar(m) for m in range(1, 52)]
COLOR = [int(c[-1] in 'HD') for c in CARDS]

def sector(labels):
    return max(k for k in range(1, 52) if len(set(labels[51 - k:])) == k)

def main():
    band_ref = {r['N']: r for r in json.load(open(sys.argv[1]))}
    report = {'script': 'f51_independent.py', 'checks': []}
    def ok(name, **d): report['checks'].append({'name': name, 'pass': True, **d}); print('PASS', name, json.dumps(d)[:240], flush=True)
    counts = {}
    for N in range(1, 11173):
        counts[N] = len(components(N))
    band = [N for N in counts if counts[N] == 51]
    assert band == list(range(1177, 1765))
    selfdesc = [N for N in counts if counts[N] == N // 28]
    assert selfdesc == list(range(1428, 1456))
    ok('component counts for N = 1..11172; band and self-describing radices', band=[band[0], band[-1], len(band)], selfDescribing=[selfdesc[0], selfdesc[-1], len(selfdesc)])
    # repaired proof: L = ceil(N/588) leading consonants; 21(L-1) <= floor(N/28) <= 21L; count = L + 48 for N >= 588
    for N in range(588, 11173):
        L = -(-N // 588); c = N // 28
        assert 21 * (L - 1) <= c <= 21 * L and counts[N] == L + 48
    for N in range(1, 588):
        assert counts[N] > N // 28
    bad_ceiling = [N for N in range(588, 11173) if -(-N // 588) != -(-(N // 28) // 21)]
    ok('Section 3 repaired: bracket holds for every N; the old step ceil(N/588) = ceil(floor(N/28)/21) fails', failuresOfOldStep=len(bad_ceiling), firstFailures=bad_ceiling[:3])
    # 588 band tables
    mism = 0; tables = {}
    for N in band:
        mem = classes(N)
        sizes = [len(m) for m in mem]
        cls = [j for j, m in enumerate(mem, 1) for _ in m]
        joint = Counter(zip(cls, POLAR))
        arr = math.prod(math.factorial(v) for v in joint.values())
        pairs = sum(v * (v - 1) // 2 for v in joint.values())
        safe = sector(list(zip(cls, POLAR, COLOR)))
        lowest = [name(c) for c in mem[-1]]
        r = band_ref[N]
        row = (sizes, arr, pairs, safe, N // 28, sorted(lowest), sizes[-1])
        ref = (r['class_sizes'], r['arrangements'], r['collision_pairs'], r['WPcolor_safe_sector'], r['complete_contexts'], sorted(r['lowest']), r['lowest_size'])
        if row != ref: mism += 1
        tables[N] = (mem, cls)
    assert mism == 0
    ok('all 588 band tables match f51_band.json', tables=len(band), mismatches=mism)
    # decoder optimum inside the self-describing window
    best = min(band_ref[N]['arrangements'] for N in selfdesc)
    top = [N for N in selfdesc if band_ref[N]['arrangements'] == best and band_ref[N]['WPcolor_safe_sector'] == max(band_ref[M]['WPcolor_safe_sector'] for M in selfdesc)]
    assert top == [1437, 1438, 1439, 1440]
    bal = [N for N in selfdesc if sum(1 for c in tables[N][0][[i for i, m in enumerate(tables[N][0]) if m[0] == ('V', 0)][0]]) == N % 28 - 1]
    assert bal == [1438]
    ok('window optimum 1437-1440; balanced partial classes (9 vowels = r - 1 trailing) only at 1438', optimum=top, balanced=bal)
    # PP270 §4.1
    assert 28**51 < 21**56 < 28**52
    assert 1218**42 < 42**42 * 28**43 and 1219**43 > 43**43 * 28**43
    trail = [N for N in band if all(c[0] == 'T' for c in tables[N][0][-1])]
    def ranges(xs):
        out = []; s = p = xs[0]
        for x in xs[1:]:
            if x != p + 1: out.append([s, p]); s = x
            p = x
        return out + [[s, p]]
    assert len(trail) == 257 and ranges(trail) == [[1219, 1455], [1745, 1764]]
    margin = 56 * math.log2(21) - 51 * math.log2(28)
    ok('PP270 4.1 replayed (second seat): edge inequalities exact; trailing class is the minimum for 257 radices', window=ranges(trail), margin1438=round(margin, 6), factor=round(21**56 / 28**51, 4))
    # PP270 §4.2
    M = 51
    fib = defaultdict(list)
    for m in range(1, M + 1): fib[POLAR[m - 1]].append(m)
    for p, ms in fib.items():
        s, t = p.denominator, p.numerator
        assert ms == [j * s * (j * s - 1) // 2 + j * t for j in range(1, M + 1) if j * s * (j * s - 1) // 2 + j * t <= M]
    lifts = math.prod(math.factorial(len(v)) for v in fib.values())
    assert len(fib) == 30 and lifts == 50164531200 and fib[Fraction(1)] == [1, 3, 6, 10, 15, 21, 28, 36, 45]
    W = tables[1438][1]
    J = Counter(zip(W, POLAR)); nonsingle = sorted(sorted(m for m in range(1, 52) if (W[m - 1], POLAR[m - 1]) == k) for k, v in J.items() if v > 1)
    assert len(J) == 48 and math.prod(math.factorial(v) for v in J.values()) == 8 and nonsingle == [[6, 10], [15, 21], [36, 45]]
    def mu(labels):
        last = {}
        for i, l in enumerate(labels, 1): last[l] = i
        return max(i for i, l in enumerate(labels, 1) if last[l] != i)
    ks = [M - mu(lab) for lab in (POLAR, list(zip(POLAR, COLOR)), list(zip(W, POLAR, COLOR)))]
    assert ks == [15, 23, 45] and ks == [sector(POLAR), sector(list(zip(POLAR, COLOR))), sector(list(zip(W, POLAR, COLOR)))]
    ok('PP270 4.2 replayed (second seat): polar fibre formula, 30 labels, 50 164 531 200 lifts, J has 8 lifts, sectors 15/23/45', triangularFibre=fib[Fraction(1)], Jpairs=nonsingle, sectors=ks)
    report['status'] = 'PASS'
    if '--json' in sys.argv:
        json.dump(report, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)

if __name__ == '__main__':
    main()

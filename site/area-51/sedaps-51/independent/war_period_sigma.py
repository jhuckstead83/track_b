"""War with the winning card placed first (the two-live phase of the SEDAPS rule).
Part 1: every cycle for n <= 9, found by brute force, alternates winners.
Part 2: the two-turn position permutation sigma of an alternating cycle, where alpha is A's
length before its winning turns; 2*ord(sigma) is the period. For even alpha, sigma has cycles of
lengths alpha/2, (n+1)/2 and (n-1-alpha)/2; for odd alpha it is one n-cycle (impossible in a real
cycle, since the top card would have to lose). Run: python3 war_period_sigma.py  (about 20 s)"""
import itertools, collections, math, sys
def step(A, B):
    a, b = A[0], B[0]; A, B = A[1:], B[1:]
    if a > b: return A + (a, b), B, 0
    return A, B + (b, a), 1
def all_cycles(n):
    seen = set(); out = []
    for perm in itertools.permutations(range(n)):
        for k in range(1, n):
            x = (perm[:k], perm[k:])
            if x in seen: continue
            path = []; idx = {}
            while x not in seen and x not in idx and x[0] and x[1]:
                idx[x] = len(path); path.append(x); x = step(*x)[:2]
            if x in idx and x[0] and x[1]:
                out.append(path[idx[x]:])
            seen.update(path)
    return out
def sigma(n, a):
    """two-turn position permutation when A (pre-length a) wins, then B (pre-length n-a-1) wins"""
    b = n - a - 1
    pos = [('A', i) for i in range(a)] + [('B', j) for j in range(n - a)]
    def f(p):
        q, i = p
        # turn 1: A wins, lengths (a, n-a)
        if q == 'A': q, i = ('A', a - 1) if i == 0 else ('A', i - 1)
        else: q, i = ('A', a) if i == 0 else ('B', i - 1)
        # turn 2: B wins, lengths (a+1, b)
        if q == 'B': q, i = ('B', b - 1) if i == 0 else ('B', i - 1)
        else: q, i = ('B', b) if i == 0 else ('A', i - 1)
        return (q, i)
    perm = {p: f(p) for p in pos}
    assert sorted(perm.values()) == sorted(pos)
    seen = set(); lens = []
    for p in pos:
        if p in seen: continue
        L = 0; x = p
        while x not in seen: seen.add(x); x = perm[x]; L += 1
        lens.append(L)
    return sorted(lens)
for n in range(3, 10):
    cs = all_cycles(n)
    alt = 0; winpat = collections.Counter()
    for c in cs:
        w = [step(*s)[2] for s in c]
        if all(w[i] != w[(i + 1) % len(w)] for i in range(len(w))): alt += 1
    print('n', n, 'cycles', len(cs), 'strictly alternating', alt, 'lengths', dict(collections.Counter(len(c) for c in cs)))
print()
for n in list(range(3, 14)) + [51]:
    rows = []
    for a in range(1, n - 1):
        lens = sigma(n, a); o = math.lcm(*lens)
        rows.append((a, 2 * o, (2 * o) % (n + 1) == 0))
    print('n', n, 'alpha -> 2*ord(sigma):', [(a, L) for a, L, _ in rows][:12], '...' if n > 13 else '', 'all multiples of n+1:', all(d for *_, d in rows))

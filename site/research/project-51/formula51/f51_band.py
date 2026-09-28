"""Formula 51 band search: every radix N with 51 visible components, scored by the Project 51 decoder.
Uses the method's own derive() (inherited/derive51.py). For each N:
  - class sizes in the method's order (decreasing weight, then code point),
  - identity m -> class id, with the fixed polar address k/n of identity m and card color,
  - joint (class, polar) fibers -> number of compatible arrangements per complete profile,
  - (class, polar, color) largest injective factorial sector (last k identities with distinct labels),
  - complete leading/vowel contexts floor(N/28) and the lowest-class size.
"""
import sys, math, json
from fractions import Fraction
from collections import Counter, defaultdict
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # derive51.py ships beside this script (Project 51 v0.3 fixture)
from derive51 import derive, signature

CARDS = [r + s for r in ['A','2','3','4','5','6','7','8','9','10','J','Q','K'] for s in 'SHDC' if r + s != '2C']
def polar(m):
    n = 1
    while n * (n + 1) // 2 < m: n += 1
    return Fraction(m - n * (n - 1) // 2, n)
POLAR = [polar(m) for m in range(1, 52)]
COLOR = [int(c[-1] in 'HD') for c in CARDS]

def classes_for(N):
    d = derive(N)
    if d['components'] != 51: return None
    sizes = d['class_sizes']
    cls = [j for j, n in enumerate(sizes, 1) for _ in range(n)]
    return d, sizes, cls

def score(cls):
    joint = list(zip(cls, POLAR))
    fib = Counter(joint)
    arrangements = math.prod(math.factorial(v) for v in fib.values())
    pairs = sum(v * (v - 1) // 2 for v in fib.values())
    jpc = list(zip(cls, POLAR, COLOR))
    safe = max(k for k in range(1, 52) if len(set(jpc[51 - k:])) == k)
    return arrangements, pairs, safe

rows = []
for N in range(1, 11173):
    r = classes_for(N)
    if r is None: continue
    d, sizes, cls = r
    arr, pairs, safe = score(cls)
    rows.append({'N': N, 'class_sizes': sizes, 'n_classes': len(sizes), 'arrangements': arr, 'collision_pairs': pairs,
                 'WPcolor_safe_sector': safe, 'complete_contexts': N // 28, 'lowest': d['lowest'],
                 'lowest_size': sizes[-1]})
band = [r['N'] for r in rows]
print(f'radices with exactly 51 visible components: {len(rows)}  range [{min(band)}, {max(band)}]  contiguous: {band == list(range(min(band), max(band)+1))}')
ref = next(r for r in rows if r['N'] == 1438)
print('N=1438:', {k: ref[k] for k in ['class_sizes', 'arrangements', 'collision_pairs', 'WPcolor_safe_sector', 'complete_contexts', 'lowest_size']})
dist = Counter(r['arrangements'] for r in rows)
print('arrangements distribution over the band:', dict(sorted(dist.items())))
best = min(r['arrangements'] for r in rows)
print('best arrangements:', best, ' radices:', [r['N'] for r in rows if r['arrangements'] == best][:40])
sdist = Counter(r['WPcolor_safe_sector'] for r in rows)
print('W+P+color safe-sector distribution:', dict(sorted(sdist.items())))
selfref = [r['N'] for r in rows if r['complete_contexts'] == 51]
print('self-describing radices (components = complete contexts = 51):', selfref[0], '..', selfref[-1], f'({len(selfref)})')
for r in rows:
    if r['complete_contexts'] == 51:
        print(f"  N={r['N']}  r=N mod 28={r['N']%28:2d}  sizes={r['class_sizes']}  arrangements={r['arrangements']}  pairs={r['collision_pairs']}  WPc-sector={r['WPcolor_safe_sector']}")
json.dump(rows, open('f51_band.json', 'w'), indent=0)

"""Own first failing rung of DH zero 10 (0.5159 + 520.94i, delta = 0.0159), scanning tau only within +-3 of it
(zero 11's pair at +10.3 is kept in the sum but its own failure region is not scanned)."""
import json, math
from planted import G
Z = [json.load(open(r'dh\%s' % f)) for f in ['dh_zeros.json', 'dh_zeros_260_440.json', 'dh_zeros_440_640.json']]
on = sorted(sum((z['online'] for z in Z), [])); off = sum((z['offline'] for z in Z), [])
s0, t0 = [p for p in off if abs(p[1] - 520.94) < 0.1][0]; d = s0 - 0.5
rel = [complex(g - t0, 0) for g in on if abs(g - t0) < 40]
for s, t in off:                      # every off-line pair in range, as z and conj(z)
    if abs(t - t0) < 40: rel += [complex(t - t0, -(s - 0.5)), complex(t - t0, s - 0.5)]
def minG(k, span=3.0):
    K = k / (t0 * t0); step = min(1 / math.sqrt(K), math.pi / (K * d)) / 12
    n = int(2 * span / step); best = 9e9
    for i in range(n + 1):
        u = -span + 2 * span * i / n
        best = min(best, G(k, t0 + u, [(r - u, 1) for r in rel]))
    return best
K = 1.0; prev = K
while True:
    if minG(K * t0 * t0) < 0: break
    prev = K; K *= 1.03
lo, hi = int(prev * t0 * t0), int(K * t0 * t0) + 1
while hi - lo > 1:
    mid = (lo + hi) // 2
    if minG(mid) < 0: hi = mid
    else: lo = mid
a = min(abs(g - t0) for g in on)
law = math.pi / 2 * t0 * t0 / (a * d)
print(f'zero 10: t={t0:.4f} delta={d:.4f} a={a:.4f}  own first failing rung k* = {hi}  law (pi/2)t^2/(a d) = {law:.0f}  ratio {hi/law:.3f}')

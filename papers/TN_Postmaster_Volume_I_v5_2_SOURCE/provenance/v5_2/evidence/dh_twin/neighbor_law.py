"""Nearest-neighbour law for the first failing rung: k* ~ (pi/2) t^2 / (a delta),
a = distance from the off-line zero's height to the nearest on-line zero, delta = sigma - 1/2."""
import json, math
on = sorted(json.load(open('dh_zeros.json'))['online'] + json.load(open('dh_zeros_260_440.json'))['online'])
res = json.load(open('rungs3_T440.json'))['results']
print(' height    delta    a(nearest)  k*          law (pi/2)t^2/(a d)   ratio')
ratios = []
for r in res:
    s, t = r['rho']; d = s - 0.5
    a = min(abs(g - t) for g in on)
    law = math.pi / 2 * t * t / (a * d)
    ratios.append(r['kFirst'] / law)
    print(f"{t:8.2f}  {d:.4f}   {a:.4f}     {r['kFirst']:>9}   {law:14.0f}        {r['kFirst'] / law:.3f}")
print('ratio range', round(min(ratios), 3), '-', round(max(ratios), 3), ' vs k*theta^2 range 0.22-1.40')

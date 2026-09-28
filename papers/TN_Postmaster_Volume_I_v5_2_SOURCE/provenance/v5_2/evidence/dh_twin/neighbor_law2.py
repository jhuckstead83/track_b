"""Nearest-neighbour law on all DH off-line zeros to T=640 (rungs3_T640.json).
Excludes rows whose search window was captured by a neighbouring off-line zero's failure, and rows with an
incomplete local list."""
import json, math, statistics as st
on = sorted(sum((json.load(open(f))['online'] for f in ['dh_zeros.json', 'dh_zeros_260_440.json', 'dh_zeros_440_640.json']), []))
res = json.load(open('rungs3_T640.json'))['results']
print(' zero  height    delta    a       k*          (pi/2)t^2/(a d)   ratio   note')
ratios = []
for r in res:
    s, t = r['rho']; d = s - 0.5
    a = min(abs(g - t) for g in on)
    law = math.pi / 2 * t * t / (a * d)
    xs_t = math.sqrt(r['x'])                       # height where the failure occurred
    captured = abs(xs_t - t) > 3.0                 # failure located at another zero's height
    note = 'failure at t=%.1f (another zero) - excluded' % xs_t if captured else ('local list incomplete' if not r['localComplete'] else '')
    ratio = r['kFirst'] / law
    if not captured and r['localComplete']: ratios.append(ratio)
    print(f"{r['zero']:4d}  {t:8.2f}  {d:.4f}  {a:.4f}  {r['kFirst']:>9}   {law:14.0f}     {ratio:6.3f}   {note}")
print(f'clean zeros: {len(ratios)}  ratio median {st.median(ratios):.3f}  range {min(ratios):.3f}-{max(ratios):.3f}')

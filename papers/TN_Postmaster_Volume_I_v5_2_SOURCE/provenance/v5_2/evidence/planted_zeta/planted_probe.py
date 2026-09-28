"""Probe: is K*delta^2 = 0.0631 (low heights, delta = 0.02) real or a tau-window artifact?
Scan tau over a wide window with a fine grid at several K below the reported threshold."""
import math, json, sys
from planted import platt_window, EPS, G

zs = platt_window('zeros_14.dat', 450, 400)
ref_t0, ref_Z = zs[200]; tref = ref_t0 + ref_Z * EPS
gam = [(p[0] - ref_t0) + (p[1] - ref_Z) * EPS for p in zs]
d = 0.02
for j in [150 + i for i in range(99)]:
    gm = (gam[j] + gam[j + 1]) / 2
    if abs(tref + gm - 1027.8) < 0.1: break
base = [complex(g - gm, 0) for i, g in enumerate(gam) if i not in (j, j + 1)]
rel = [z for z in base if abs(z) < 25] + [complex(0, -d), complex(0, d)]
t = tref + gm
print('plant at t =', round(t, 3), ' nearest remaining zeros at', sorted([round(z.real, 3) for z in rel if abs(z.real) < 2 and z.imag == 0]))
for Kd2 in [0.02, 0.03, 0.04, 0.05, 0.06, 0.0625, 0.0631, 0.064, 0.07]:
    K = Kd2 / d ** 2; k = K * t * t
    best = (1e9, None)
    n = 12000
    for i in range(n + 1):
        s = -3 + 6 * i / n
        v = G(k, t + s, [(r - s, 1) for r in rel])
        if v < best[0]: best = (v, s)
    print(f'K*d^2={Kd2:<7} K={K:9.2f}  min G over tau in [-3,3] = {best[0]: .4e} at offset {best[1]: .4f}   (negative band starts at pi/(4K delta) = {math.pi/(4*K*d):.4f})')

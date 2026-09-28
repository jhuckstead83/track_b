#!/usr/bin/env python3
"""High-precision replay of the Davenport-Heilbronn twin's first rung failure (Team B, 27 Sep 2026).

Scope: the FINITE zero list dh-zeros-T260.json (169 on-line zeros and 5 off-line pairs below height 260,
double-precision ordinates). The scaled rung is
    G_k(x) = sum over folded nodes q of w_q * Re[(4xq/(x+q)^2)^k] / max_q |4xq/(x+q)^2|^k,
with q = 1/4 + gamma^2 (weight 1) for an on-line zero and q = s(1-s), s = sigma + i t (weight 2, the
conjugate folded pair) for an off-line zero. Its sign is the sign of the Widder rung W_k(x) on that list.
This checks arithmetic precision only: truncation to height 260 and the double-precision zeros are the
stated scope, not something this script removes.
Usage: python3 dh_twin_highprec.py path/to/dh-zeros-T260.json [--json out.json]
"""
import json, sys, random
import mpmath as mp

def load(path):
    Z = json.load(open(path))
    return Z['online'], Z['offline']

def nodes(online, offline):
    out = [(mp.mpf(0.25) + mp.mpf(g) ** 2, 1) for g in online]
    for s, t in offline:
        z = mp.mpc(s, t)
        out.append((z * (1 - z), 2))
    return out

def G(x, k, Q):
    x = mp.mpf(x)
    logs = []
    for q, w in Q:
        r = 4 * x * q / (x + q) ** 2
        logs.append((mp.log(r), w))
    lmax = max(mp.re(l) for l, _ in logs)
    return mp.fsum(w * mp.re(mp.exp(k * (l - lmax))) for l, w in logs)

def golden_min(f, a, b, it=80):
    g = (mp.sqrt(5) - 1) / 2
    c, d = b - g * (b - a), a + g * (b - a); fc, fd = f(c), f(d)
    for _ in range(it):
        if fc < fd: b, d, fd = d, c, fc; c = b - g * (b - a); fc = f(c)
        else: a, c, fc = c, d, fd; d = a + g * (b - a); fd = f(d)
    return (c, fc) if fc < fd else (d, fd)

def main():
    path = sys.argv[1]
    online, offline = load(path)
    report = {'script': 'dh_twin_highprec.py', 'zeroList': path.split('/')[-1], 'onLine': len(online), 'offLinePairs': len(offline),
              'scope': 'finite zero list below height 260; double-precision ordinates', 'runs': []}
    x0 = '7140.066261872734'  # the recorded minimiser of W_16589 (dh_first_failure_219_20000.json)
    for dps in (60, 100):
        mp.mp.dps = dps
        Q = nodes(online, offline)
        g16589 = G(x0, 16589, Q)
        xm, gm = golden_min(lambda x: G(x, 16588, Q), mp.mpf('7139.9'), mp.mpf('7140.2'))
        xn, gn = golden_min(lambda x: G(x, 16589, Q), mp.mpf('7139.9'), mp.mpf('7140.2'))
        run = {'dps': dps, 'G16589_at_x0': mp.nstr(g16589, 12), 'W16588_min': mp.nstr(gm, 12), 'W16588_argmin': mp.nstr(xm, 12),
               'W16589_min': mp.nstr(gn, 12), 'W16589_argmin': mp.nstr(xn, 12)}
        report['runs'].append(run); print(run, flush=True)
        assert g16589 < 0 and gm > 0 and gn < 0
    # sensitivity: move every listed ordinate by up to 1e-12 (far above double rounding) and re-evaluate at 60 digits
    mp.mp.dps = 60; random.seed(20260927); worst = [mp.inf, -mp.inf]
    for trial in range(8):
        on = [g + random.uniform(-1e-12, 1e-12) for g in online]
        off = [[s + random.uniform(-1e-12, 1e-12), t + random.uniform(-1e-12, 1e-12)] for s, t in offline]
        Q = nodes(on, off)
        a, b = G(x0, 16589, Q), G(mp.mpf('7140.0673'), 16588, Q)
        worst = [min(worst[0], b), max(worst[1], a)]
    report['perturbation'] = {'trials': 8, 'maxShift': 1e-12, 'W16588_near_min_lowest': mp.nstr(worst[0], 8), 'W16589_at_x0_highest': mp.nstr(worst[1], 8)}
    assert worst[0] > 0 and worst[1] < 0
    report['published'] = {'W16588_min': 1.7592739e-4, 'W16589': -4.6600915e-5, 'source': 'Dossier v5.2 §69A (40-digit Colab recheck)'}
    report['status'] = 'PASS'
    print(json.dumps(report['perturbation'])); 
    if '--json' in sys.argv:
        json.dump(report, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)

if __name__ == '__main__':
    main()

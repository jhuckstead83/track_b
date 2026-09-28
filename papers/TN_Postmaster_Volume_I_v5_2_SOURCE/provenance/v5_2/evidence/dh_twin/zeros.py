"""Complete zero list of the standard DH twin in [-0.45, 1.45] x (0, T].
On-line zeros: sign changes of the real function Z(t), refined by bisection+secant.
Totals: argument principle per window. Off-line zeros: excess located by |f| grid + Newton.
Writes dh_zeros.json."""
import cmath, math, json, sys
from dh import f, Z

T = float(sys.argv[1]) if len(sys.argv) > 1 else 260.0
SL, SR = -0.45, 1.45            # zero-free for sigma >= 1.3951 (and mirror <= -0.3951)

def zr(t): return Z(t).real

def refine(a, b, fa, fb):
    for _ in range(80):
        m = (a * fb - b * fa) / (fb - fa) if fb != fa else (a + b) / 2
        if not (a < m < b): m = (a + b) / 2
        fm = zr(m)
        if fm == 0: return m
        if (fa < 0) == (fm < 0): a, fa = m, fm
        else: b, fb = m, fm
        if b - a < 1e-13: break
    return (a + b) / 2

def online(t0, t1, dt=0.01):
    out = []; t = t0; ft = zr(t)
    while t < t1:
        u = min(t + dt, t1); fu = zr(u)
        if (ft < 0) != (fu < 0): out.append(refine(t, u, ft, fu))
        t, ft = u, fu
    return out

def arg_change(path_pts):
    """Sum of arg increments of f along a polyline, adaptively subdivided."""
    total = 0.0
    for p, q in zip(path_pts, path_pts[1:]):
        stack = [(p, q, f(p), f(q))]
        while stack:
            a, b, fa, fb = stack.pop()
            d = cmath.phase(fb / fa)
            if abs(d) > 0.4 and abs(b - a) > 1e-9:
                m = (a + b) / 2; fm = f(m)
                stack.append((m, b, fm, fb)); stack.append((a, m, fa, fm))
            else:
                total += d
    return total

def count(t0, t1, n=60):
    pts = []
    for i in range(n + 1): pts.append(complex(SL + (SR - SL) * i / n, t0))
    for i in range(1, n + 1): pts.append(complex(SR, t0 + (t1 - t0) * i / n))
    for i in range(1, n + 1): pts.append(complex(SR - (SR - SL) * i / n, t1))
    for i in range(1, n + 1): pts.append(complex(SL, t1 - (t1 - t0) * i / n))
    return arg_change(pts) / (2 * math.pi)

def newton(z):
    z0 = z
    for _ in range(60):
        h = 1e-6; d = (f(z + h) - f(z - h)) / (2 * h)
        if d == 0: return z0
        step = f(z) / d
        if abs(step) > 0.5: step *= 0.5 / abs(step)
        z -= step
        if abs(z - z0) > 3 or not (SL - 0.5 < z.real < SR + 0.5): return z0
        if abs(step) < 1e-14: break
    return z

def offline_search(t0, t1, want):
    """Find `want` zeros with sigma>1/2 in (t0,t1): grid local minima of |f| then Newton."""
    found = []
    ns, nt = 48, max(40, int((t1 - t0) * 25))
    grid = {}
    for i in range(ns + 1):
        s = 0.5 + 0.004 + (SR - 0.504) * i / ns
        for j in range(nt + 1):
            t = t0 + (t1 - t0) * j / nt
            grid[i, j] = abs(f(complex(s, t)))
    cands = []
    for (i, j), v in grid.items():
        nb = [grid.get((i + di, j + dj)) for di in (-1, 0, 1) for dj in (-1, 0, 1) if (di or dj)]
        if all(x is None or v <= x for x in nb):
            s = 0.5 + 0.004 + (SR - 0.504) * i / ns; t = t0 + (t1 - t0) * j / nt
            cands.append((v, complex(s, t)))
    for v, c in sorted(cands, key=lambda x: x[0]):
        z = newton(c)
        if abs(f(z)) < 1e-10 and z.real > 0.5 + 1e-8 and t0 - 1 < z.imag < t1 + 1 and all(abs(z - w) > 1e-6 for w in found):
            found.append(z)
    return found

if __name__ == '__main__':
    W = 5.0
    T0 = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
    OUT = sys.argv[3] if len(sys.argv) > 3 else 'dh_zeros.json'
    cuts = [T0 + W * i for i in range(int((T - T0) / W) + 1)] + [T]
    cuts = sorted(set(round(c, 6) for c in cuts if c <= T))
    on_all, off_all, report = [], [], []
    # bottom box (-0.5, 0.5): check f on the real segment and the small box
    nb = count(-0.5, 0.5) if T0 <= 0.5 else 0.0
    report.append({'window': [-0.5, 0.5], 'total': round(nb, 3)})
    for a, b in zip(cuts, cuts[1:]):
        tot = count(a, b)
        on = online(a, b)
        excess = round(tot) - len(on)
        off = offline_search(a, b, excess // 2) if excess > 0 else []
        off_in = [z for z in off if a <= z.imag < b]
        report.append({'window': [a, b], 'argument_count': round(tot, 4), 'online': len(on),
                       'offline_pairs_found': len(off_in), 'consistent': abs(tot - len(on) - 2 * len(off_in)) < 1e-3})
        on_all += on; off_all += off_in
        print(report[-1], flush=True)
    json.dump({'T': T, 'strip': [SL, SR], 'online': on_all,
               'offline': [[z.real, z.imag] for z in off_all], 'windows': report},
              open(OUT, 'w'), indent=1)
    print('online', len(on_all), 'offline (sigma>1/2)', len(off_all), 'all windows consistent:',
          all(r.get('consistent', True) for r in report[1:]))

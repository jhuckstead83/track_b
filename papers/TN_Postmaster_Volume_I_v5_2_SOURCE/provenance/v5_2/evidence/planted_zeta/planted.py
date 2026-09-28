"""Planted-defect calibration of the Widder rung ladder on zeta's real zeros.

Exact local form: with ordinate z (q = 1/4 + z^2; an off-line zero 1/2+delta+i*gamma has z = gamma - i*delta)
and x = 1/4 + tau^2, the normalized rung sign function is G_k(tau) = sum_rho Re exp(k L(z_rho)),
L = log(4xq/(x+q)^2) = log1p(e) - 2 log1p(e/2),  e = (z^2 - tau^2)/x   (computed from z - tau exactly).
To leading order L = -(z-tau)^2/tau^2, so k* = K* tau^2 with K* local.
Planting: merge two consecutive zeta zeros g_j, g_{j+1} into one off-line pair at their mean height
with displacement delta (preserves N(T)). First failing rung found on a geometric K grid, then bisected.
Validation: the same code on the DH twin's zero 0 must return k* = 16,589.
"""
import cmath, math, os, struct, random, json, sys

EPS = 2.0 ** -101
DATA = r'D:\Zeroes\riemann-zeta-zeros\data'

def Lfun(dz, tau):
    """dz = z - tau (complex, small relative to tau). Returns complex L."""
    x = 0.25 + tau * tau
    e = dz * (dz + 2 * tau) / x
    if abs(e) < 1e-3:
        return -e * e / 4 + e ** 3 / 4 - 7 * e ** 4 / 32 + 3 * e ** 5 / 16
    return cmath.log(1 + e) - 2 * cmath.log(1 + e / 2)

def G(k, tau, zs):
    """Scaled rung sign function; zs are (dz0, weight) with dz0 = z - tau_ref and tau = tau_ref + s."""
    Ls = [(Lfun(dz, tau), w) for dz, w in zs]
    m = max(L.real for L, w in Ls)
    tot = 0.0
    for L, w in Ls:
        a = k * (L.real - m)
        if a > -700: tot += w * math.exp(a) * math.cos(k * L.imag)
    return tot

def min_over_tau(k, tref, rel, span, K, delta=None):
    """min over tau in tref + [-span, span]; rel = list of (z - tref) complex, weights 1."""
    width = 1 / math.sqrt(K)
    if delta:                                # cover the whole first negative band of the pair
        span = max(span, 3 * math.pi / (4 * K * delta) + 2 * width)
    span = min(span, 60.0)
    reach = span + 9 * width                 # terms beyond ~9 Gaussian widths are < e^-81 relative
    rel = [r for r in rel if abs(r.real) < reach]
    step = min(width, math.pi / (K * delta)) / 12 if delta else width / 12
    n = max(200, int(2 * span / step))
    best = (float('inf'), None)
    vals = []
    for i in range(n + 1):
        s = -span + 2 * span * i / n
        zs = [(r - s, 1) for r in rel]
        vals.append((G(k, tref + s, zs), s))
    for i in range(1, n):
        if vals[i][0] < best[0]: best = (vals[i][0], vals[i][1])
        if vals[i][0] <= vals[i - 1][0] and vals[i][0] <= vals[i + 1][0] and vals[i][0] < 0.05:
            a, b = vals[i - 1][1], vals[i + 1][1]
            gr = (math.sqrt(5) - 1) / 2
            c, d = b - gr * (b - a), a + gr * (b - a)
            fc = G(k, tref + c, [(r - c, 1) for r in rel]); fd = G(k, tref + d, [(r - d, 1) for r in rel])
            for _ in range(60):
                if fc < fd: b, d, fd = d, c, fc; c = b - gr * (b - a); fc = G(k, tref + c, [(r - c, 1) for r in rel])
                else: a, c, fc = c, d, fd; d = a + gr * (b - a); fd = G(k, tref + d, [(r - d, 1) for r in rel])
            v = min(fc, fd)
            if v < best[0]: best = (v, c if fc < fd else d)
    return best

def first_failure(tref, rel, Kmin=1e-3, Kmax=1e8, delta=None):
    """rel: complex z - tref for the local zeros; an off-line pair is passed as z and conj(z)
    (the two conjugate folded nodes, together giving 2 Re)."""
    K = Kmin; prevK = K
    v0, _ = min_over_tau(K * tref * tref, tref, rel, max(3 / math.sqrt(K), 0.5), K, delta)
    if v0 < 0: return ('negative at Kmin', Kmin)
    while K < Kmax:
        k = K * tref * tref
        v, s = min_over_tau(k, tref, rel, max(3 / math.sqrt(K), 0.5), K, delta)
        if v < 0: break
        prevK = K; K *= 1.02
    else:
        return None
    lo, hi = math.floor(prevK * tref * tref), math.ceil(K * tref * tref)
    while hi - lo > 1:                                       # bisect on integer k inside the bracket
        mid = (lo + hi) // 2
        Km = mid / (tref * tref)
        v, s = min_over_tau(mid, tref, rel, max(3 / math.sqrt(Km), 0.5), Km, delta)
        if v < 0: hi = mid
        else: lo = mid
    return hi

def platt_window(name, n_before_skip, count):
    """Return `count` consecutive zeros from file `name` after skipping n_before_skip (t0, Z exact pairs)."""
    out = []; seen = 0
    with open(os.path.join(DATA, name), 'rb') as fh:
        nb = struct.unpack('<Q', fh.read(8))[0]
        for _ in range(nb):
            t0, t1, n0, n1 = struct.unpack('<ddQQ', fh.read(32))
            Z = 0
            for _ in range(n1 - n0):
                z1, z2, z3 = struct.unpack('<QIB', fh.read(13))
                Z += (z3 << 96) + (z2 << 64) + z1
                seen += 1
                if seen > n_before_skip: out.append((t0, Z))
                if len(out) == count: return out
    return out

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'validate':
        dz = json.load(open(r'dh\dh_zeros.json'))
        s0, t0 = dz['offline'][0]; delta = s0 - 0.5
        tref = t0
        rel = [complex(g - tref, 0) for g in dz['online'] if abs(g - tref) < 12]
        rel += [complex(0, -delta), complex(0, delta)]        # pair z = t0 -/+ i delta  (q and conj q)
        k = first_failure(tref, rel, Kmin=0.05, Kmax=50, delta=delta)
        near = sorted(abs(z.real) for z in rel if z.imag == 0)[0]
        print('DH twin zero 0: first failing rung from the local exact form =', k, ' (rungs3: 16589);',
              ' law (pi/2) t^2/(a delta) =', round(math.pi / 2 * tref * tref / (near * delta)), ' a =', round(near, 4))
    else:
        name, skip, deltas, nplants = sys.argv[2], int(sys.argv[3]), [float(d) for d in sys.argv[4].split(',')], int(sys.argv[5])
        W = 2000
        zs = platt_window(name, skip, W)
        # exact differences relative to a reference zero in the middle
        ref_t0, ref_Z = zs[W // 2]
        tref = ref_t0 + ref_Z * EPS
        def rel_of(p): return ((p[0] - ref_t0) + (p[1] - ref_Z) * EPS) if p[0] != ref_t0 else (p[1] - ref_Z) * EPS
        gam = [rel_of(p) for p in zs]                            # ordinates relative to tref
        random.seed(51)
        out = []
        for d in deltas:
            for _ in range(nplants):
                j = random.randrange(W // 2 - 50, W // 2 + 49)
                gm = (gam[j] + gam[j + 1]) / 2
                base = [complex(g, 0) for i, g in enumerate(gam) if i not in (j, j + 1)]
                shift = gm                                           # re-centre on the planted height
                rel = [z - shift for z in base if abs(z - shift) < 200] + [complex(0, -d), complex(0, d)]
                t_here = tref + shift
                k = first_failure(t_here, rel, Kmin=1e-4 / (d * d), Kmax=50 / (d * d), delta=d)
                a = min(abs(z.real) for z in rel if z.imag == 0)
                theta = math.atan2(2 * d * t_here, t_here * t_here + 0.25 - d * d)
                ok = isinstance(k, int)
                out.append({'height': t_here, 'delta': d, 'merged_gap': gam[j + 1] - gam[j], 'nearest_a': a, 'kFirst': k if ok else str(k),
                            'Kstar': k / (t_here * t_here) if ok else None, 'Kdelta2': (k / (t_here * t_here)) * d * d if ok else None,
                            'kTheta2': k * theta * theta if ok else None,
                            'law_ratio': (k / (math.pi / 2 * t_here * t_here / (a * d))) if ok else None})
                print(json.dumps(out[-1]), flush=True)
        json.dump(out, open(f'planted_{name[:-4]}.json', 'w'), indent=1)
